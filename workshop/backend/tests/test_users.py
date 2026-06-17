# -*- coding: utf-8 -*-
"""测试人员管理 API"""
import pytest


class TestListUsers:
    """查询用户列表"""

    def test_list_all_users(self, client):
        """获取所有用户列表"""
        resp = client.get("/api/users")
        assert resp.status_code == 200
        data = resp.json()
        assert "users" in data
        assert len(data["users"]) >= 3  # 至少有 3 个测试用户

    def test_get_single_user(self, client, test_user_id):
        """获取单个用户详情（含任务）"""
        resp = client.get(f"/api/users/{test_user_id}")
        assert resp.status_code == 200
        user = resp.json()
        assert "name" in user
        assert "student_id" in user
        assert "tasks" in user  # 包含任务列表

    def test_get_user_not_found(self, client):
        """查询不存在的用户应返回 404"""
        resp = client.get("/api/users/99999")
        assert resp.status_code == 404


class TestCreateUser:
    """创建用户"""

    def test_create_user(self, client):
        """创建新用户并自动生成二维码 token"""
        resp = client.post("/api/users", json={
            "student_id": "2024999",
            "name": "测试用户",
            "class_name": "测试班",
            "phone": "13800000000"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "id" in data
        assert "qrcode_token" in data

        # 清理：删除测试用户
        client.delete(f"/api/users/{data['id']}")

    def test_create_duplicate_student_id(self, client):
        """重复学号应返回 400"""
        # 先创建
        resp = client.post("/api/users", json={
            "student_id": "99990001", "name": "重复测试"
        })
        assert resp.status_code == 200
        uid = resp.json()["id"]

        # 重复创建
        resp = client.post("/api/users", json={
            "student_id": "99990001", "name": "重复测试2"
        })
        assert resp.status_code == 400

        # 清理
        client.delete(f"/api/users/{uid}")


class TestUpdateUser:
    """更新用户"""

    def test_update_user_name(self, client, test_user_id):
        """更新用户姓名"""
        resp = client.put(f"/api/users/{test_user_id}", json={
            "name": "张三（已修改）"
        })
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        # 恢复原名
        client.put(f"/api/users/{test_user_id}", json={"name": "张三"})


class TestDeleteUser:
    """删除用户"""

    def test_delete_user(self, client):
        """删除一个临时创建的用户"""
        # 先创建
        resp = client.post("/api/users", json={
            "student_id": "99990002", "name": "待删除用户"
        })
        uid = resp.json()["id"]

        # 删除
        resp = client.delete(f"/api/users/{uid}")
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        # 确认已删除
        resp = client.get(f"/api/users/{uid}")
        assert resp.status_code == 404
