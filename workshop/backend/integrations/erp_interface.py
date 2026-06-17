"""ERP 系统接口（预留）"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/integration/erp", tags=["ERP接口"])


class ERPOrder(BaseModel):
    """ERP 工单数据结构"""
    order_id: str
    product_name: str
    quantity: int
    deadline: Optional[str] = None
    priority: Optional[str] = "normal"


@router.post("/orders")
def sync_order(data: ERPOrder):
    """
    ERP 工单同步接口（预留）
    接收 ERP 系统推送的生产工单，同步到车间管理系统
    """
    return {
        "success": True,
        "message": f"ERP工单 {data.order_id} 已接收（预留接口）",
        "data": data.dict()
    }


@router.get("/orders")
def list_erp_orders():
    """查询 ERP 同步的工单列表（预留）"""
    return {"orders": [], "message": "ERP接口已预留，待实际对接"}
