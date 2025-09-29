from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")

# 1. RAWG API 데이터 가져오기 함수
def fetch_rawg_data():
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&dates=2019-09-01,2019-09-30&platforms=18,1,7"
    res = requests.get(url)
    data = res.json()

    results = data.get("results", [])
    df = pd.DataFrame(results)

    # 저장 위치: Docker 컨테이너와 공유되는 경로로 설정 필요
    os.makedirs("/opt/airflow/data", exist_ok=True)
    df.to_csv("/opt/airflow/data/rawg_games.csv", index=False)

with DAG(
    dag_id="game_recommend_mlops_v2",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,   # 필요시 '@daily' 같은 값으로 교체
    catchup=False,
) as dag:

    # 2. API 데이터 수집 Task
    fetch_task = PythonOperator(
        task_id="fetch_rawg_data",
        python_callable=fetch_rawg_data,
    )

    # 3. 모델 학습 Task
    run_training = DockerOperator(
        task_id="train_model",
        image="moongs95/third-party-mlops:v4",   # 팀장이 만든 이미지
        command="python mlops/src/main.py",      # 학습 실행
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={
            "WANDB_API_KEY": WANDB_API_KEY
        },
        mount_tmp_dir=False
    )

    # 4. 추천 Task
    run_recommend = DockerOperator(
        task_id="recommend",
        image="moongs95/third-party-mlops:v4",
        command="python mlops/src/main.py recommend 12",  # user_id 넣기
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={
            "WANDB_API_KEY": WANDB_API_KEY
        },
        mount_tmp_dir=False
    )

    # 실행 순서: RAWG 데이터 수집 → 학습 → 추천
    fetch_task >> run_training >> run_recommend
