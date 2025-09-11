# FastAPI FS Router

FastAPI 애플리케이션에서 파일 시스템 기반으로 라우터를 자동으로 로드하는 라이브러리입니다.

[English](README.md) | 한국어

## 기능

- 📁 파일 시스템 구조를 기반으로 한 자동 라우터 로딩
- 🔗 디렉토리 구조가 API 경로로 자동 매핑
- 🎯 APIRouter 인스턴스를 자동으로 감지하고 등록
- ⚙️ 커스텀 프리픽스 지원
- 🚀 중복 라우터 방지
- 🛣️ 패스 파라미터와 라우트 그룹 지원

## 설치

```bash
pip install fastapi-fs-router
```

## 사용법

### 기본 사용법

```python
from fastapi import FastAPI
from fastapi_fs_router import load_fs_router

app = FastAPI()

# routers 디렉토리에서 모든 라우터를 자동으로 로드
load_fs_router(app, "routers")
```

### 디렉토리 구조 예시

```
routers/
├── users.py          # /users 경로로 매핑
├── items.py          # /items 경로로 매핑
└── v1/
    └── admin/
        └── users.py  # /v1/admin/users 경로로 매핑
```

### 라우터 파일 예시

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    return {"users": []}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### 커스텀 프리픽스 사용

```python
from fastapi import FastAPI
from fastapi_fs_router import load_fs_router

app = FastAPI()

# 모든 라우터에 /api/v1 프리픽스 추가
load_fs_router(app, "routers", prefix="/api/v1")
```

이 경우 라우터들은 다음과 같이 매핑됩니다:
- `routers/users.py` → `/api/v1/users`
- `routers/v1/admin/users.py` → `/api/v1/v1/admin/users`
- `routers/(empty)/admin/users.py` → `/api/admin/users`
- `routers/hello_world/admin/hello_world.py` → `/hello-world/admin/hello-world`
- `routers/{path_param}/admin.py` → `/{path_param}/admin`

### 경로 변환 규칙

- 패스파라미터를 제외한 언더스코어(`_`)는 하이픈(`-`)으로 변환됩니다
- 대괄호로 감싸진 부분은 중괄호로 변환됩니다 (예: `[id]` → `{id}`)
- 괄호로 감싸진 부분은 무시됩니다 (예: `(empty)`)

## API 참조

### `load_fs_router(app, route_dir, *, prefix="")`

FastAPI 애플리케이션에 파일 시스템 기반 라우터를 로드합니다.

**매개변수:**
- `app` (FastAPI): FastAPI 애플리케이션 인스턴스
- `route_dir` (Path | str): 라우터 파일들이 있는 디렉토리 경로 (기본값: "routers")
- `prefix` (str): 모든 라우터에 추가할 프리픽스 (기본값: "")

**동작:**
1. 지정된 디렉토리를 재귀적으로 탐색
2. `.py` 파일에서 `APIRouter` 인스턴스를 찾음
3. 디렉토리 구조를 기반으로 API 경로 생성
4. FastAPI 앱에 라우터 등록

## 개발

### 의존성 설치

```bash
# 개발 의존성 설치
uv sync
```

### 테스트 실행

```bash
# 모든 테스트 실행
uv run pytest
```

### 코드 품질 검사

```bash
# 린팅
ruff check src/ tests/

# 포맷팅
ruff format src/ tests/
```

## 라이선스

이 프로젝트는 아파치 라이선스 2.0 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여

버그 리포트, 기능 요청, 풀 리퀘스트를 환영합니다! 기여하기 전에 이슈를 먼저 생성해 주세요.

## 작성자

- **owjs3901** - *초기 작업* - [owjs3901@gmail.com](mailto:owjs3901@gmail.com)
