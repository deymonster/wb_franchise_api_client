from typing import Optional

from pydantic import BaseModel, Field


class OfficeWorkload(BaseModel):
    inbox_count: int
    limit_delivery: int
    office_id: int
    total_count: int
    workload: int
