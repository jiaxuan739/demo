"""二维码路由 - 扫码验证 + 生成二维码图片"""
import qrcode
import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.config import get_connection

router = APIRouter(prefix="/api/qrcode", tags=["二维码"])


@router.get("/{token}")
def scan_qrcode(token: str):
    """扫码后调用此接口，返回用户基本信息"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, student_id, name, class_name, qrcode_token FROM users WHERE qrcode_token=%s",
            (token,)
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="无效的二维码")
        # 同时查询该用户的任务
        cursor.execute("SELECT * FROM tasks WHERE user_id=%s ORDER BY created_at DESC", (user['id'],))
        user['tasks'] = cursor.fetchall()
        return {"success": True, "user": user}
    finally:
        cursor.close()
        conn.close()


@router.get("/{user_id}/image")
def generate_qrcode_image(user_id: int):
    """生成用户的二维码图片"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT qrcode_token, name FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 二维码内容：指向小程序页面的 URL 参数
        qr_url = f"https://workshop.example.com?token={user['qrcode_token']}"

        img = qrcode.make(qr_url)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    finally:
        cursor.close()
        conn.close()
