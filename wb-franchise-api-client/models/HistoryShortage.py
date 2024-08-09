from typing import Optional
from pydantic import BaseModel, Field


class Responsible(BaseModel):
    guilty_employee_id: int
    name: Optional[str] = Field(None)
    office_id: int
    supplier_id: int


class ApointedTo(BaseModel):
    employee_id: Optional[int] = Field(None)
    group_name: str


class HistoryShortage(BaseModel):
    appointed_to: ApointedTo
    comment: str
    dt: str
    employee_id: int
    employee_name: str
    supplier_id: Optional[int] = Field(None)
    supplier_name: Optional[str] = Field(None)
    loss_responsible: Responsible
    status_id: int


