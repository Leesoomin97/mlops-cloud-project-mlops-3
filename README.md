# 프로젝트 이름
MLOps_game_recommendation_project
<br>

## 💻 프로젝트 소개
### <프로젝트 소개>
- 이 프로젝트는 게임 추천 시스템을 설계하고, 이를 MLOps 파이프라인으로 자동화하는 것을 목표로 진행되었습니다.
단순히 추천 모델을 구현하는 것에서 그치지 않고, 실제 서비스 환경에서 운영 가능한 수준으로 발전시키는 과정을 경험했습니다.

🎯 목표

-사용자의 게임 플레이 데이터를 기반으로 취향에 맞는 새로운 게임을 추천하는 시스템 구축.

-데이터 수집부터 모델 학습, 추론, 모니터링, 알림, CI/CD까지 이어지는 엔드 투 엔드(End-to-End) MLOps 파이프라인 구현.

🔧 기술적 특징

1. 데이터 수집: RAWG API를 통해 게임 데이터(장르, 평점, 플레이타임 등) 자동 수집.

2. 모델링: Item-based Collaborative Filtering을 활용한 추천 모델 구현.

3. 환경 일관성: Docker를 통한 컨테이너 기반 학습 및 추론 환경 구성.

4. 파이프라인 관리: Airflow를 활용하여 DAG 단위로 데이터 검증 → 학습 → 추론 → 알림 자동화.

5. 실험 관리: W&B(Weights & Biases)로 모델 학습 기록 및 성능 추적.

6. CI/CD: GitHub Actions + Docker Hub를 이용한 빌드 및 배포 자동화.



### <작품 소개>
- 이 작품은 게임 추천 서비스 프로토타입으로, 특정 유저 ID를 기준으로 새로운 게임을 추천해줍니다.
최종 결과물은 운영 환경을 고려한 MLOps 파이프라인과 함께 제공됩니다.

💡 사용자 관점에서 할 수 있는 것

-user_id(1~100)를 입력하면, 해당 사용자가 플레이한 게임과 유사한 게임 목록을 추천받을 수 있음.

-추천 결과는 Airflow DAG 실행 후 자동으로 생성되며, Slack 알림으로 결과 확인 가능.

-Docker 이미지를 통해 어디서든 동일한 환경에서 실행 가능.


📊 산출물

-추천 모델 결과: 유사 게임 Top-N 리스트

-Airflow DAG: 데이터 수집 → 모델 학습 → 추천 추론 → 알림까지의 워크플로우

-로그 & 알림: DAG 실행 결과가 Slack으로 전송되어 모니터링 가능

-CI/CD 환경: GitHub Actions를 통한 Docker 이미지 자동 빌드 및 업로드

<br>


## 👨‍👩‍👦‍👦 팀 구성원

| ![권문진](https://avatars.githubusercontent.com/u/156163982?v=4) | ![고민서](https://avatars.githubusercontent.com/u/156163982?v=4) | ![김동근](https://avatars.githubusercontent.com/u/156163982?v=4) | ![이수민](https://avatars.githubusercontent.com/u/156163982?v=4) | ![오패캠](https://avatars.githubusercontent.com/u/156163982?v=4) |
| :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------: |
|            [권문진](https://github.com/UpstageAILab)             |            [고민서](https://github.com/UpstageAILab)             |            [김동근](https://github.com/UpstageAILab)             |            [이수민](https://github.com/UpstageAILab)             |            [허예경](https://github.com/UpstageAILab)             |
|                            팀장, 담당 역할                             |                            담당 역할                             |                            담당 역할                             |                            담당 역할                             |                            담당 역할                             |

<br>

## 🔨 개발 환경 및 기술 스택
⚙️ 개발환경

-OS: Windows 10 + WSL2 (Ubuntu 20.04)

-IDE/Editor: VS Code, Jupyter Notebook

-패키지 관리: Conda / pip

-컨테이너 환경: Docker Desktop (Windows), Docker Compose

-워크플로우 관리: Apache Airflow (Docker 기반)

-형상 관리: Git, GitHub


🔧 기술 스택

-주언어: Python 3.9

-데이터 처리 & 분석: pandas, numpy, scikit-learn

-모델링: Item-based Collaborative Filtering (콘텐츠 기반 추천)

-실험 관리: Weights & Biases (W&B)

-MLOps/인프라:Docker (환경 일관성 보장), Airflow (데이터 파이프라인 자동화), Slack Webhook (Airflow Operator 활용 알림), GitHub Actions (CI/CD 자동화), AWS (향후 배포 고려)


🤝 협업 & 이슈 관리

-이슈 관리: GitHub Issues & Projects

-협업 툴: Notion (작업 분배, 문서화) + GitHub (버전 관리, 코드 리뷰)

-버전 관리 전략: Git Flow 일부 적용 (메인 브랜치 + 기능별 브랜치)

<br>

## 📁 프로젝트 구조
```
.
├── dags/                           # Airflow DAGs (v1 ~ v6)
│   ├── game_recommend_mlops_v1.py  # 초기 데이터 수집 + 학습
│   ├── game_recommend_mlops_v2.py  # 데이터 검증 단계 추가
│   ├── game_recommend_mlops_v3.py  # 리소스 최적화
│   ├── game_recommend_mlops_v4.py  # 자동 스케줄링 및 slack 알림 연동
│   ├── game_recommend_mlops_v5.py  # 검증 + 모니터링 강화
│   ├── game_recommend_mlops_v6.py  # CI/CD 반영
│   └── ci-cd.yml                   # Airflow 관련 YAML 설정
│
├── mlops/
│   └── src/
│       ├── models/                 # 추천 모델 코드
│       ├── data/                   # 데이터 수집 및 전처리 코드
│       ├── preprocessing.py        # 데이터 전처리 로직
│       └── main.py                 # 파이프라인 실행 진입점
│
├── .github/workflows/
│   └── ci-cd.yml                   # GitHub Actions 워크플로우
│
├── tests/                          # 유닛 테스트 코드
├── requirements.txt                # 의존성 패키지 목록
├── .gitignore                      # GitHub 업로드 제외 파일 설정
├── .env.example                    # 환경 변수 예시 파일
└── README.md                       # 프로젝트 설명서
```
<br>

## 💻​ 구현 기능

🔹 데이터 파이프라인

-게임 데이터 수집: RAWG API를 통해 게임 메타데이터 자동 수집 (genre, rating, playtime, owned_ratio 등).

-데이터 검증: 수집된 데이터에 대해 레코드 존재 여부 및 필드 유효성 확인.

-데이터 전처리: Label Encoding, StandardScaler, 장르 임베딩 벡터화 진행.



🔹 모델링 & 학습

-추천 모델: Item-based Collaborative Filtering (Item-CF) 기반 추천.

-학습 실행: mlops/src/main.py를 통해 모델 학습 자동화.

-실험 관리: W&B(Weights & Biases)를 활용해 실험 기록 및 성능 추적.

-결과 저장: 학습된 모델 아티팩트는 공유 디렉토리(/opt/mlops/models)에 저장.



🔹 추론 및 결과

-추천 추론: 특정 유저(user_id=12)를 입력하면 유사 게임 Top-N 추천 제공.

-Airflow 통합: DAG 실행을 통해 학습 후 자동으로 추천 결과 생성.



🔹 모니터링 & 알림

-Slack 알림: DAG 실행 성공/실패 여부를 Slack Webhook으로 전송.

-에러 핸들링: 데이터 검증 실패 또는 DockerOperator 오류 발생 시 즉시 알림.



🔹 MLOps & 자동화

-Docker 컨테이너화: 모델 학습 및 추론 환경을 Docker 이미지(moongs95/third-party-mlops:v5)로 일관성 있게 관리.

-Airflow 파이프라인: 데이터 수집 → 검증 → 학습 → 추론 → 알림을 DAG로 자동화.

-CI/CD: GitHub Actions로 Docker 이미지 자동 빌드 및 Docker Hub 푸시.

<br>

## 🚨​ 트러블 슈팅

🔹 Airflow Web UI(8080) 접속 불가

-문제: localhost:8080 접속 시 UI가 끊기거나 아예 접속 불가.

-원인: Docker Desktop 메모리 부족(3.8GB), 네트워크 브리징 충돌.

-해결: Docker 메모리 4GB 이상 할당, docker-compose 재기동.

-결과: 안정적으로 Web UI 접속 가능.



🔹 Docker Host 연결 오류

-문제: DockerOperator 실행 시 “Docker Daemon not found” 에러.

-원인: docker_url을 unix://var/run/docker.sock와 tcp://host.docker.internal:2375 혼용.

-해결: Windows 환경 맞게 tcp://host.docker.internal:2375로 통일.

-결과: DAG 내 DockerOperator 정상 실행.



🔹 DAG 알림 태스크 Skipped 혼동

-문제: DAG 성공 후에도 실패 알림 태스크가 skipped로 표시돼서 실패로 오인.

-원인: Trigger Rule(all_success, one_failed) 동작 이해 부족.

-해결: 정상 동작임을 확인하고 팀 내 공유.

-결과: 불필요한 코드 수정 방지.



🔹 RAWG API ↔ main.py CSV 의존성 불일치

-문제: Airflow는 API에서 데이터를 수집했지만, Docker 컨테이너 내부 학습 코드는 CSV(Top-40 Video Games.csv) 기반.

-해결 방향 (v6 반영 예정):DAG에서 API 응답을 CSV로 저장. 컨테이너는 해당 CSV를 읽어 학습/추론 수행.

-결과(예정): 데이터 파이프라인 일관성 확보.



🔹 Airflow 로그 출력 불가

-문제: 태스크 실행 후 Web UI에서 로그가 비어있거나 “symlink error” 경고.

-원인: Airflow 로그 디렉토리가 Windows 환경에서 심볼릭 링크를 제대로 생성하지 못함.

-해결:로그 디렉토리(./logs)를 미리 생성하고 권한 수정. AIRFLOW__CORE__BASE_LOG_FOLDER와 AIRFLOW__CORE__DAGS_FOLDER 환경 변수 경로를 절대경로로 지정.

-결과: 로그 정상 출력, 디버깅 가능해짐.

<br>

## 📌 프로젝트 회고
과거 머신러닝 프로젝트에서는 모델링 자체를 설계하고 구현하는 과정만으로도 큰 어려움이 따랐다. 데이터 전처리, 피처 엔지니어링, 모델 학습 및 평가를 반복하는 과정에서 수많은 시행착오를 겪으며, 당시에도 벅차다는 느낌을 강하게 받았다. 그러나 이번 프로젝트는 그러한 경험 위에서 다시 출발했기 때문에, 추천 모델링(Item-CF 기반) 단계까지는 이전 경험을 활용하여 상대적으로 안정적으로 수행할 수 있었다.

하지만 이번 프로젝트의 핵심은 단순한 모델링이 아니었다. Docker를 통한 컨테이너화, Airflow 기반 파이프라인 구축, CI/CD와 AWS 연계라는 새로운 과제가 뒤따랐다. 이 과정에서 기술적 난관이 이어졌다.

1.Docker: 이미지 빌드, 공유 볼륨 마운트, 환경 변수 전달 등 기본 설정조차 꼬이는 경우가 많아, 컨테이너 실행을 반복적으로 실패하며 디버깅에 많은 시간을 쏟았다.
2.Airflow: Windows/WSL 환경 특성으로 인한 로그 출력 불가, DockerOperator의 호스트 연결 문제, Slack Webhook 연동 이슈 등 복합적인 문제들이 발생했다. 특히 docker_url과 네트워크 브리징 오류는 해결에 상당한 시간이 소요되었다.
3.AWS: 클라우드 환경에서 Airflow 및 Docker를 어떻게 안정적으로 연계할지 감을 잡는 데 어려움이 있었고, 온전히 이해하기에는 시간이 부족했다.

이처럼 모델링 이후의 단계는 또 다른 거대한 장벽이었다. 기존의 경험으로는 쉽게 풀리지 않는 문제들이었고, 때로는 학습曲線(learning curve)을 감당하기 버거울 만큼 가파르게 느껴졌다.

그럼에도 불구하고 이번 프로젝트는 단순히 “모델을 만드는 경험”을 넘어, 실제 서비스 환경에서 머신러닝을 운영하기 위해 무엇이 필요한지를 직접 체험할 수 있는 소중한 기회였다. 아직 Docker, Airflow, AWS 모두 능숙하다고 말하기는 어렵지만, 적어도 문제를 정의하고 해결 방법을 탐색하며, 제한된 환경에서도 파이프라인을 끝까지 구현해낸 경험은 나의 역량을 한층 확장시켰다.

앞으로는 이 경험을 토대로 더 다양한 프로젝트를 통해 MLOps 실무 능력을 보완하고, 궁극적으로는 데이터 사이언스와 엔지니어링을 잇는 다리 역할을 수행할 수 있는 전문성을 키워가고자 한다.

<br>




