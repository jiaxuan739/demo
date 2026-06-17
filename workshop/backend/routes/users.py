"""人员管理路由 - 管理员 CRUD"""
import hashlib
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.config import get_connection

router = APIRouter(prefix="/api/users", tags=["人员管理"])


class UserCreate(BaseModel):
    student_id: str
    name: str
    class_name: Optional[str] = ""
    phone: Optional[str] = ""


class UserUpdate(BaseModel):
    name: Optional[str] = None
    class_name: Optional[str] = None
    phone: Optional[str] = None


@router.get("")
def list_users():
    """查询所有用户"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, student_id, name, class_name, phone, qrcode_token, created_at FROM users ORDER BY id")
        return {"users": cursor.fetchall()}
    finally:
        cursor.close()
        conn.close()


@router.get("/{user_id}")
def get_user(user_id: int):
    """查询单个用户及其任务"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        cursor.execute("SELECT * FROM tasks WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
        user['tasks'] = cursor.fetchall()
        return user
    finally:
        cursor.close()
        conn.close()


@router.post("")
def create_user(data: UserCreate):
    """新增用户（自动生成二维码 token）"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        qrcode_token = "qr_" + hashlib.md5(data.student_id.encode()).hexdigest()[:16]
        sql = "INSERT INTO users (student_id, name, class_name, phone, qrcode_token) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (data.student_id, data.name, data.class_name, data.phone, qrcode_token))
        conn.commit()
        return {"success": True, "id": cursor.lastrowid, "qrcode_token": qrcode_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate):
    """修改用户信息"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="用户不存在")

        fields = []
        values = []
        if data.name is not None:
            fields.append("name=%s"); values.append(data.name)
        if data.class_name is not None:
            fields.append("class_name=%s"); values.append(data.class_name)
        if data.phone is not None:
            fields.append("phone=%s"); values.append(data.phone)

        if fields:
            values.append(user_id)
            cursor.execute(f"UPDATE users SET {','.join(fields)} WHERE id=%s", values)
            conn.commit()
        return {"success": True}
    finally:
        cursor.close()
        conn.close()


@router.delete("/{user_id}")
def delete_user(user_id: int):
    """删除用户"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="用户不存在")
        conn.commit()
        return {"success": True}
    finally:
        cursor.close()
        conn.close()
