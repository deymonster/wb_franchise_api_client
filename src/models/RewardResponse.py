from typing import Optional

from pydantic import BaseModel, Field


class ExtData(BaseModel):
    percent: list[float]
    supplier_return_sum: int
    supplier_tare_sum: int
    bags_sum: int
    office_rating: float
    currency_rate: Optional[float] = Field(default=None)
    currency_code: str
    office_rating_sum: float
    rating_sum_desc: str
    office_speed_sum: float
    rate_by_region: float


class RewardResponse(BaseModel):
    office_id: int
    date: str
    amount: float
    currency_code: str
    ext_data: ExtData


