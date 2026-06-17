"""
车间管理系统 — FastAPI 后端入口
启动: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
文档: http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import auth, users, tasks, qrcode
from backend.integrations import erp_interface, mes_interface, wms_interface

app = FastAPI(
    title="车间管理系统 WMS",
    description="人员管理 + 任务管理 + 二维码扫码 | ERP/MES/WMS 接口预留",
    version="1.0.0",
)

# CORS 跨域（允许小程序调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(qrcode.router)

# 注册预留接口
app.include_router(erp_interface.router)
app.include_router(mes_interface.router)
app.include_router(wms_interface.router)


@app.get("/")
def root():
    return {"message": "车间管理系统 API 运行中", "docs": "/docs"}
