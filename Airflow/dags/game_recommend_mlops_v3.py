from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")

# 1. RAWG API 데이터 가져오기
def fetch_rawg_data(**context):
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&dates=2019-09-01,2019-09-30&platforms=18,1,7"
    res = requests.get(url)
    data = res.json()

    # 필요한 부분만 리턴 (XCom으로 전달됨)
    return json.dumps(data["results"])

# 2. DockerOperator에서 XCom 불러오기 (환경변수로 전달 예시)
def prepare_training_command(**context):
    ti = context["ti"]
    raw_data = ti.xcom_pull(task_ids="fetch_rawg_data")
    # DockerOperator에 넘길 command 생성
    return f"python mlops/src/main.py --data '{raw_data}'"

with DAG(
    dag_id="game_recommend_mlops_v3",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # 나중에 자동 실행으로 바꿀 예정
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_rawg_data",
        python_callable=fetch_rawg_data,
        provide_context=True,
    )

    run_training = DockerOperator(
        task_id="train_model",
        image="moongs95/third-party-mlops:v4",
        command="python mlops/src/main.py",  # 우선 고정, 나중에 동적으로 바꿀 수 있음
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={
            "WANDB_API_KEY": WANDB_API_KEY
        },
        mount_tmp_dir=False,
    )

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
    )

    fetch_task >> run_training >> run_recommend
