from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from docker.types import Mount
from datetime import timedelta
import pendulum, requests, json
from dotenv import load_dotenv
import os

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
TZ = pendulum.timezone("Asia/Seoul")

# Slack Connection (Airflow Connections에 등록)
SLACK_CONN_ID = "slack_default"

# 공유 경로 (호스트 ↔ 컨테이너)
SHARED_HOST_DIR = "D:/airflow_shared"
SHARED_CONTAINER_DIR = "/opt/mlops/models"

# ======================
# 함수 정의
# ======================
def fetch_rawg_data(**context):
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&dates=2019-09-01,2019-09-30&platforms=18,1,7"
    res = requests.get(url)
    data = res.json()
    return json.dumps(data["results"])

def validate_data(**context):
    ti = context["ti"]
    data = ti.xcom_pull(task_ids="fetch_rawg_data")
    records = json.loads(data)

    if not records or "name" not in records[0]:
        raise ValueError("데이터 검증 실패: 결과 없음 또는 필드 누락")
    print(f"데이터 검증 성공: {len(records)}개 게임 로드됨")

# ======================
# DAG 정의
# ======================
default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=30),
    "depends_on_past": False,
}

with DAG(
    dag_id="game_recommend_mlops_v5",
    start_date=pendulum.datetime(2025, 1, 1, tz=TZ),
    schedule="0 6 * * *",   # 매일 아침 6시
    catchup=False,
    default_args=default_args,
    max_active_runs=1,
    tags=["v5", "validation", "slack-alert"],
) as dag:

    # 1. 데이터 수집
    fetch_task = PythonOperator(
        task_id="fetch_rawg_data",
        python_callable=fetch_rawg_data,
    )

    # 2. 데이터 검증
    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
    )

    # 3. 학습 (모델을 공유 디렉토리에 저장)
    train_task = DockerOperator(
        task_id="train_model",
        image="moongs95/third-party-mlops:v5",
        command="python mlops/src/main.py",
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={"WANDB_API_KEY": WANDB_API_KEY},
        mounts=[Mount(source=SHARED_HOST_DIR, target=SHARED_CONTAINER_DIR, type="bind")],
        mount_tmp_dir=False,
        pool="heavy",
        priority_weight=10,
        sla=timedelta(minutes=15),
    )

    # 4. 추천 (공유된 모델 디렉토리 사용)
    recommend_task = DockerOperator(
        task_id="recommend",
        image="moongs95/third-party-mlops:v5",
        command="python mlops/src/main.py recommend 12",
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={"WANDB_API_KEY": WANDB_API_KEY},
        mounts=[Mount(source=SHARED_HOST_DIR, target=SHARED_CONTAINER_DIR, type="bind")],
        mount_tmp_dir=False,
        priority_weight=8,
    )

    # 5. Slack 알림 (성공 시)
    slack_success = SlackWebhookOperator(
        task_id="slack_notify_success",
        slack_webhook_conn_id=SLACK_CONN_ID,   # ← 구버전 호환
        message="대장! DAG 성공적으로 완료했어요 🐿️",
        trigger_rule="all_success",
        username="airflow-bot",
        icon_emoji=":chipmunk:",
    )

    # 6. Slack 알림 (실패 시)
    slack_failure = SlackWebhookOperator(
        task_id="slack_notify_failure",
        slack_webhook_conn_id=SLACK_CONN_ID,   # ← 구버전 호환
        message="대장 ㅠㅠ DAG 실행 중 실패 발생! 로그를 확인해줘!",
        trigger_rule="one_failed",
        username="airflow-bot",
        icon_emoji=":scream:",
    )

    # 실행 순서
    fetch_task >> validate_task >> train_task >> recommend_task
    [slack_success, slack_failure] << recommend_task
