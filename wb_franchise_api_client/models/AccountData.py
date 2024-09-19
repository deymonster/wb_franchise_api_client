from typing import Optional

from pydantic import BaseModel, Field


class Employee(BaseModel):
    """Model for Employee"""
    create_date: str
    employee_id: int
    first_name: str
    is_deleted: bool
    last_name: str
    middle_name: str
    phones: list[str]
    rating: Optional[float] = Field(default=None)
    shortages_sum: Optional[float] = Field(default=None)


class Office(BaseModel):
    """Model for Office"""
    id: int
    is_site_active:  bool
    name: str
    office_shk: str


class AccountData(BaseModel):
    supplier_id: int
    name: str
    employees: list[Employee]
    offices: list[Office]

