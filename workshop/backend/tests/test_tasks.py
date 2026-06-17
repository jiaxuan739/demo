# -*- coding: utf-8 -*-
"""测试任务管理 API"""
import pytest


class TestListTasks:
    """查询任务列表"""

    def test_list_all_tasks(self, client):
        """获取所有任务"""
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert "tasks" in data
        assert len(data["tasks"]) >= 4  # 至少有 4 个测试任务

    def test_task_has_related_user(self, client):
        """任务应该包含关联用户信息"""
        resp = client.get("/api/tasks")
        tasks = resp.json()["tasks"]
        task = tasks[0]
        assert "user_name" in task  # 左连接后的用户名
        assert "student_id" in task

    def test_get_single_task(self, client):
        """获取单个任务"""
        resp = client.get("/api/tasks/1")
        assert resp.status_code == 200
        task = resp.json()
        assert "title" in task

    def test_get_task_not_found(self, client):
        """不存在的任务应返回 404"""
        resp = client.get("/api/tasks/99999")
        assert resp.status_code == 404


class TestCreateTask:
    """创建任务"""

    def test_create_task(self, client, test_user_id):
        """创建新任务"""
        resp = client.post("/api/tasks", json={
            "user_id": test_user_id,
            "title": "测试创建任务",
            "description": "这是一个测试任务",
            "status": "pending",
            "quantity": 10,
            "deadline": "2026-12-31"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        tid = data["id"]

        # 清理
        client.delete(f"/api/tasks/{tid}")

    def test_create_task_empty_title(self, client):
        """空标题应返回 400"""
        resp = client.post("/api/tasks", json={
            "user_id": 1,
            "title": "",
        })
        assert resp.status_code == 400


class TestUpdateTask:
    """更新任务"""

    def test_update_task_status(self, client):
        """更新任务状态"""
        # 先创建
        resp = client.post("/api/tasks", json={
            "user_id": 1, "title": "状态更新测试",
            "status": "pending"
        })
        tid = resp.json()["id"]

        # 更新为已完成
        resp = client.put(f"/api/tasks/{tid}", json={"status": "completed"})
        assert resp.status_code == 200

        # 验证
        resp = client.get(f"/api/tasks/{tid}")
        assert resp.json()["status"] == "completed"

        # 清理
        client.delete(f"/api/tasks/{tid}")


class TestDeleteTask:
    """删除任务"""

    def test_delete_task(self, client):
        """删除任务"""
        resp = client.post("/api/tasks", json={
            "user_id": 1, "title": "待删除任务"
        })
        tid = resp.json()["id"]

        resp = client.delete(f"/api/tasks/{tid}")
        assert resp.status_code == 200

        resp = client.get(f"/api/tasks/{tid}")
        assert resp.status_code == 404


class TestUserMyData:
    """用户查看自己数据"""

    def test_my_data(self, client):
        """用户查看自己的信息和任务"""
        resp = client.get("/api/tasks/my/1")
        assert resp.status_code == 200
        data = resp.json()
        assert "name" in data
        assert "tasks" in data

    def test_my_data_not_found(self, client):
        """不存在用户应返回 404"""
        resp = client.get("/api/tasks/my/99999")
        assert resp.status_code == 404
