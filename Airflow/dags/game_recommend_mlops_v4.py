from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import pendulum
from dotenv import load_dotenv
import os

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
TZ = pendulum.timezone("Asia/Seoul")

# ======================
# 함수 정의
# ======================
def fetch_rawg_data(**context):
    """RAWG API에서 게임 데이터 수집"""
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&dates=2019-09-01,2019-09-30&platforms=18,1,7"
    res = requests.get(url)
    data = res.json()
    # 필요한 부분만 리턴 (XCom 전달)
    return json.dumps(data["results"])

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
    dag_id="game_recommend_mlops_v4",
    start_date=pendulum.datetime(2025, 1, 1, tz=TZ),
    schedule="0 6 * * *",   # 매일 아침 6시 실행 (자동화)
    catchup=False,
    default_args=default_args,
    max_active_runs=1,      # DAG 동시 실행 1개만
    max_active_tasks=3,     # 태스크 동시 실행 최대 3개
    tags=["v4", "autosched", "resource-opt"],
) as dag:

    # 1. RAWG 데이터 가져오기
    fetch_task = PythonOperator(
        task_id="fetch_rawg_data",
        python_callable=fetch_rawg_data,
    )

    # 2. 학습 (DockerOperator - heavy pool)
    run_training = DockerOperator(
        task_id="train_model",
        image="moongs95/third-party-mlops:v4",
        command="python mlops/src/main.py",
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={
            "WANDB_API_KEY": WANDB_API_KEY
        },
        mount_tmp_dir=False,
        pool="heavy",              # 리소스 많이 쓰는 태스크 → heavy 풀
        priority_weight=10,
    )

    # 3. 추천 실행 (DockerOperator)
    run_recommend = DockerOperator(
        task_id="recommend",
        image="moongs95/third-party-mlops:v4",
        command="python mlops/src/main.py recommend 12",
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={
            "WANDB_API_KEY": WANDB_API_KEY
        },
        mount_tmp_dir=False,
        priority_weight=8,
    )

    # 실행 순서
    fetch_task >> run_training >> run_recommend
