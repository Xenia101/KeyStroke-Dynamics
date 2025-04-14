### Poetry 설치

```bash
# MacOS / Linux / WSL
curl -sSL https://install.python-poetry.org | python3 -

# Windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### 프로젝트 설치

```bash
# 프로젝트 클론
git clone https://github.com/username/keystroke-dynamics-auth.git
cd keystroke-dynamics-auth

# 의존성 설치
poetry install
```

## 사용 방법

### Poetry 환경에서 실행

```bash
# Poetry 쉘 활성화
poetry shell

# CLI 도구 사용 예시
keystroke-auth train --user-id user123 --phrase "my secure password"
keystroke-auth authenticate --user-id user123 --phrase "my secure password" --model models/user123_model.pkl
```

### Python API 사용 예시

```python
from keystroke_dynamics_auth.auth import KeystrokeDynamicsAuth
from keystroke_dynamics_auth.data_collection import collect_keystroke_data

# 키스트로크 인증 시스템 초기화
auth_system = KeystrokeDynamicsAuth()

# 사용자 데이터로 모델 학습
auth_system.train(user_data, non_user_data, user_id)

# 사용자 인증
is_authentic, confidence = auth_system.authenticate(keystroke_data, user_id)
```

### 데모 실행

데모 예제를 실행하여 시스템의 작동 방식을 확인할 수 있습니다:

```bash
# Poetry 쉘에서
python examples/demo.py
```

## 주요 기능

- 키스트로크 데이터 수집 및 특징 추출
- SVM을 사용한 사용자 타이핑 패턴 학습
- 실시간 사용자 인증
- 모델 저장 및 로드
- 시각화 도구 제공
- CLI 인터페이스

## 프로젝트 구조

```
keystroke-dynamics-auth/
├── keystroke_dynamics_auth/      # 메인 패키지
│   ├── __init__.py
│   ├── __main__.py               # 모듈 실행 진입점
│   ├── auth.py                   # 인증 클래스
│   ├── cli.py                    # CLI 인터페이스
│   ├── data_collection.py        # 데이터 수집 유틸리티
│   └── visualization.py          # 시각화 유틸리티
├── examples/
│   └── demo.py                   # 데모 실행 스크립트
├── pyproject.toml                # Poetry 설정
└── README.md
```