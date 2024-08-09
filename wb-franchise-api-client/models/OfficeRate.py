from typing import Optional
from pydantic import BaseModel, Field


class OfficeRate(BaseModel):
    avg_rate: float
    avg_region_rate: float
    office_id: int

