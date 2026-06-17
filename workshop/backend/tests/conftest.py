# -*- coding: utf-8 -*-
"""测试配置 - 使用 FastAPI TestClient"""
import pytest
from backend.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """创建测试客户端"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_token(client):
    """获取管理员登录凭据（用于后续测试）"""
    resp = client.post("/api/auth/admin/login", json={
        "username": "admin",
        "password": "admin123"
    })
    return resp.json()


@pytest.fixture
def test_user_id(client):
    """获取测试用户 ID"""
    resp = client.get("/api/users")
    users = resp.json().get("users", [])
    return users[0]["id"] if users else 1
