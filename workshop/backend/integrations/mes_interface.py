"""MES 系统接口（预留）"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/integration/mes", tags=["MES接口"])


class MESProgress(BaseModel):
    """MES 生产进度数据结构"""
    task_id: str
    workstation: str
    quantity_done: int
    status: str
    operator: str


@router.post("/progress")
def report_progress(data: MESProgress):
    """
    MES 生产进度上报接口（预留）
    接收 MES 系统推送的生产进度数据
    """
    return {
        "success": True,
        "message": f"工位{data.workstation}进度已上报（预留接口）",
        "data": data.dict()
    }


@router.get("/workstations")
def list_workstations():
    """查询工位状态（预留）"""
    return {"workstations": [], "message": "MES接口已预留，待实际对接"}
