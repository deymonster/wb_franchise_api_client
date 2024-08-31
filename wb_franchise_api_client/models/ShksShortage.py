from typing import Optional
from pydantic import BaseModel, Field


class Shk(BaseModel):
    shk_id: int
    wb_sticker:  Optional[int] = Field(None)
    amount: int
    currency_id: int
    item_name: str
    item_photo_url: str
    item_site_url: str
    new_shk_id: int
    reorder_status: Optional[int] = Field(None)
    found_info: Optional[str] = Field(None)


class ShksShortage(BaseModel):
    shortage_id: int
    comment: str
    reason_id: int
    office_id: int
    shks: list[Shk]
