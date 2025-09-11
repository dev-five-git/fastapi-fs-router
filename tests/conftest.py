"""pytest 설정 및 픽스처"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app():
    """FastAPI 앱 픽스처"""
    return FastAPI()


@pytest.fixture
def client(app):
    """테스트 클라이언트 픽스처"""
    return TestClient(app)


@pytest.fixture
def sample_router():
    """샘플 APIRouter 픽스처"""
    from fastapi import APIRouter

    router = APIRouter()

    @router.get("/health")
    def health_check():
        return {"status": "ok"}

    @router.get("/users")
    def get_users():
        return {"users": []}

    return router
