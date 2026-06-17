# -*- coding: utf-8 -*-
"""测试认证 API"""
import pytest


class TestAdminAuth:
    """管理员登录测试"""

    def test_admin_login_success(self, client):
        """正确账号密码应登录成功"""
        resp = client.post("/api/auth/admin/login", json={
            "username": "admin",
            "password": "admin123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["admin"]["username"] == "admin"
        assert data["admin"]["role"] == "super_admin"

    def test_admin_login_wrong_password(self, client):
        """错误密码应返回 401"""
        resp = client.post("/api/auth/admin/login", json={
            "username": "admin",
            "password": "wrong_password"
        })
        assert resp.status_code == 401

    def test_admin_login_empty_fields(self, client):
        """空字段应返回 422（Pydantic 验证）"""
        resp = client.post("/api/auth/admin/login", json={
            "username": "",
            "password": ""
        })
        assert resp.status_code in (422, 401)


class TestUserScanLogin:
    """用户扫码登录测试"""

    def test_user_login_by_token(self, client):
        """有效 token 应成功登录"""
        resp = client.post("/api/auth/user/login", json={
            "qrcode_token": "qr_zhangsan"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["user"]["name"] == "张三"

    def test_user_login_invalid_token(self, client):
        """无效 token 应返回 404"""
        resp = client.post("/api/auth/user/login", json={
            "qrcode_token": "invalid_token_xyz"
        })
        assert resp.status_code == 404
