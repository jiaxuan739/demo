"""WMS 系统接口（预留）"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/integration/wms", tags=["WMS接口"])


class WMSInventory(BaseModel):
    """WMS 库存数据结构"""
    material_code: str
    material_name: str
    quantity: float
    warehouse: str
    location: str


@router.post("/inventory")
def sync_inventory(data: WMSInventory):
    """
    WMS 库存同步接口（预留）
    接收 WMS 系统推送的库存数据
    """
    return {
        "success": True,
        "message": f"物料{data.material_code}库存已同步（预留接口）",
        "data": data.dict()
    }


@router.get("/materials")
def list_materials():
    """查询物料列表（预留）"""
    return {"materials": [], "message": "WMS接口已预留，待实际对接"}
