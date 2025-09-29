from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")

with DAG(
    dag_id="game_recommend_mlops",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    run_training = DockerOperator(
        task_id="train_model",
        image="moongs95/third-party-mlops:v4",   # 팀장이 만든 이미지
        command="python mlops/src/main.py",     # 학습 실행
        docker_url="tcp://host.docker.internal:2375",
        auto_remove=True,
        network_mode="bridge",
        environment={
            "WANDB_API_KEY": WANDB_API_KEY
        },
        mount_tmp_dir=False
    )

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

    run_training >> run_recommend