"""认证路由 - 管理员登录 + 用户扫码登录"""
import hashlib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.config import get_connection

router = APIRouter(prefix="/api/auth", tags=["认证"])


class AdminLogin(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    qrcode_token: str


@router.post("/admin/login")
def admin_login(data: AdminLogin):
    """管理员登录 - 用户名+密码"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        pw_hash = hashlib.sha256(data.password.encode()).hexdigest()
        cursor.execute(
            "SELECT id, username, name, role FROM admins WHERE username=%s AND password_hash=%s",
            (data.username, pw_hash)
        )
        admin = cursor.fetchone()
        if not admin:
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        return {"success": True, "admin": admin}
    finally:
        cursor.close()
        conn.close()


@router.post("/user/login")
def user_login(data: UserLogin):
    """用户扫码登录 - 用二维码 token 登录"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, student_id, name, class_name FROM users WHERE qrcode_token=%s",
            (data.qrcode_token,)
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="无效的二维码")
        return {"success": True, "user": user}
    finally:
        cursor.close()
        conn.close()
