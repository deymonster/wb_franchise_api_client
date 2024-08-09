from typing import Optional

from pydantic import BaseModel, Field


class Shortage(BaseModel):
    shortage_id: int
    create_dt: str
    guilty_employee_id: Optional[int] = Field(default=None, alias='guilty_employee_id')
    guilty_employee_name: Optional[str] = Field(default=None, alias='guilty_employee_name')
    amount: float
    comment: str
    status_id: int
    is_history_exist: bool


class OfficeShortage(BaseModel):
    office_id: Optional[int] = Field(default=0, alias='office_id')
    office_name: Optional[str] = Field(default="Unknown", alias='office_name')
    office_amount: float
    shortages: list[Shortage]


class ShortageResponse(BaseModel):
    total_amount: float
    offices: list[OfficeShortage]


