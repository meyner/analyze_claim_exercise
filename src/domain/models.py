from pydantic import BaseModel


class AnalyzeClaimResponse(BaseModel):
    vin: str
    year: int
    make: str
    model: str
    mileage: int
    repair_description: str
    part_number: str
    labor_hours: float
    vin_valid: bool
    vin_issues: list[str]
    coverage_eligible: bool
    coverage_reason: str
