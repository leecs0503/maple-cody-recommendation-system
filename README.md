# maple-cody-recommandation-system
22-2R 캡스톤디자인 AI 메이플 코디 추천 시스템

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