from pydantic import BaseModel


class ByOffice(BaseModel):
    date: str
    sale_sum: float
    sale_count: int
    return_sum:  int
    return_count: int
    proceeds: float
    diff_count: int
    on_place_count: int
    source_type: int


class OfficeProceed(BaseModel):
    office_id: int
    office_name: str
    office_shk: str
    by_office: list[ByOffice]




