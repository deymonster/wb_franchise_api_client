from typing import Optional

from pydantic import BaseModel, Field


class OfficeSpeed(BaseModel):
    avg_hours: float
    avg_hours_by_region: float
    office_id: int
