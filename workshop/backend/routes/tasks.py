"""任务管理路由 - 管理员 CRUD + 用户查看自己的任务"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.config import get_connection

router = APIRouter(prefix="/api/tasks", tags=["任务管理"])


class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "pending"
    quantity: Optional[int] = 0
    deadline: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    quantity: Optional[int] = None
    deadline: Optional[str] = None


@router.get("")
def list_tasks():
    """查询所有任务"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT t.*, u.name as user_name, u.student_id
            FROM tasks t JOIN users u ON t.user_id = u.id
            ORDER BY t.created_at DESC
        """)
        return {"tasks": cursor.fetchall()}
    finally:
        cursor.close()
        conn.close()


@router.get("/{task_id}")
def get_task(task_id: int):
    """查询单个任务"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return task
    finally:
        cursor.close()
        conn.close()


@router.post("")
def create_task(data: TaskCreate):
    """新增任务"""
    if not data.title or not data.title.strip():
        raise HTTPException(status_code=400, detail="任务标题不能为空")
    if not data.user_id:
        raise HTTPException(status_code=400, detail="负责人不能为空")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO tasks (user_id, title, description, status, quantity, deadline) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (data.user_id, data.title, data.description, data.status, data.quantity, data.deadline))
        conn.commit()
        return {"success": True, "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.put("/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    """修改任务"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM tasks WHERE id=%s", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="任务不存在")

        fields = []
        values = []
        for key in ['title', 'description', 'status', 'quantity', 'deadline']:
            val = getattr(data, key)
            if val is not None:
                fields.append(f"{key}=%s"); values.append(val)

        if fields:
            values.append(task_id)
            cursor.execute(f"UPDATE tasks SET {','.join(fields)} WHERE id=%s", values)
            conn.commit()
        return {"success": True}
    finally:
        cursor.close()
        conn.close()


@router.delete("/{task_id}")
def delete_task(task_id: int):
    """删除任务"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="任务不存在")
        conn.commit()
        return {"success": True}
    finally:
        cursor.close()
        conn.close()


# ---- 用户端 ----

@router.get("/my/{user_id}")
def my_data(user_id: int):
    """用户查看自己的信息和任务"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, student_id, name, class_name, qrcode_token FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        cursor.execute("SELECT * FROM tasks WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
        user['tasks'] = cursor.fetchall()
        return user
    finally:
        cursor.close()
        conn.close()
