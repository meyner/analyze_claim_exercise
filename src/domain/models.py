from pydantic import BaseModel
from typing import Optional


class AnalyzeClaimResponse(BaseModel):
    claim_id: str
    vin: Optional[str] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    mileage: Optional[int] = None
    repair_description: Optional[str] = None
    part_number: Optional[str] = None
    labor_hours: Optional[float] = None
    coverage_eligible: Optional[bool] = None
    coverage_reason: Optional[str] = None
