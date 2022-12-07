# maple-cody-recommandation-system
22-2R 캡스톤디자인 AI 메이플 코디 추천 시스템

 # 각자 작업 내용
이창수:
 - 구조 설계
 - 코드 리뷰
 - 모델 개발
 - 복호화 로직 개발
 - kserve 인프라 구축 (terraform)
 - WebServer - 리엑트 navi, 메인 컴포넌트 구현
 - Trainer 구현
 - Avatar Server 구현
 - 각 Micro Service끼리 통신 프로토콜 정의
강인구:
 - WzComparerR2Server 작성
 - 복호화 로직 개발
 - Train 환경 구축
 - 학습 데이터 관리
 - 학습 하이퍼파라메터 튜닝 및 학습 환경 관리
 - kserve 추론 서버(predictor) 구현
 - Api Server 비즈니스 로직 작성
 - Avatar Server 전반적인 부분 구현
유경환:
 - Crwaling script 작성
 - Avatar Server 테스트 코드(test_http_handler.py) 작성
 - Web Server intro box 컴포넌트 구현, fetch hook 작성

# 디렉토리 구조
```
.
├── notebook: 모델 개발에 필요한 notebook들
├── script: 서버 개발 전 프로토타입 개발을 위한 스크립트들
├── src: 서버 코드
└── tests: 각 작업의 테스트 코드
```

# 실행
docker-compose를 이용해 테스트 가능 (현재는 avatar server에 대해서만 docker-compose 구성)
## docker-compose up
> docker-compose -f docker-compose-dev.yml up
## docker-compose down
> docker-compose -f docker-compose-dev.yml down

## WzComparerR2Server
WzComparerR2Server에 해당되는 docker-compose는 해당 디렉토리 내부에 있음 (WzComparerR2Server/docker-compose.yml)

# 의존성 관리

의존성은 기본적으로 [poetry](https://python-poetry.org/)를 활용해 관리

## poetry 설치

```
# python2, 3 둘다 깔린 경우:
curl -sSL https://install.python-poetry.org | python3 -
# python 3이 python으로 적절히 설정되어 있는 경우:
curl -sSL https://install.python-poetry.org | python -
```

## poetry 의존성 가상 환경(.venv)에 설치

```
python -m poetry install
```

## poetry 의존성 추가
```
python -m poetry add {패키지}
```

## poetry 쉘 진입
```
python -m poetry shell
```

# 테스팅
[pytest](https://docs.pytest.org/en/7.1.x/)를 활용
## 테스트 방법
```
pytest .
```

# 코드 품질 관리
- feature을 추가할 때는 테스트 코드 작성 -> 테스트 실패 확인 -> 본 코드 작성 -> 테스트 성공 확인 (TDD)
- flake8, isort, pyright, black를 이용해 코드를 포메팅
- commit 전에 꼭 `bash run-check.sh`로 스타일 체크 후 커밋 (특히 PR 올리기 전에는 필수!!)
- 테스트가 실패하는 PR은 절대 리뷰 요청 금지
- 로컬 환경에서 가능하면 e2e로 integration test까지 해봐야 함

# 코드 형성 관리
- feature 추가시 issue를 먼저 등록하고 작업
- branch명 규칙: `{issue번호}-{microservice명}-{작업 내용}`
- main에 직접 commit하는 경우는 지양
- commit명의 prefix는 "feat", "docs", "refactor", "deploy"중 하나를 선택

# docker
 - 기본적으로 빌드는 build_XXXserver_docker.sh에 빌드 관련 스크립트를 작성
 - dockerfile들은 docker/Dockerfile.XXXXX, docker/Dockerfile.XXXXX.dockerignore 형식으로 작성
 - build시 export DOCKER_BUILDKIT=1로 설정해서 dockerignore이 인식되도록 처리
 - python server의 경우 requirements.txt를 뽑아내서 처리 (이후 multistage build로 변경 예정)
