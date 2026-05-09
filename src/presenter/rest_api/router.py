from fastapi import APIRouter

from domain.models import AnalyzeClaimResponse
from .models import AnalyzeClaimRequest

router = APIRouter()


@router.post("/analyze-claim", response_model=AnalyzeClaimResponse)
async def analyze_claim(payload: AnalyzeClaimRequest) -> AnalyzeClaimResponse:
    # Dummy response based on example
    return AnalyzeClaimResponse(
        vin="1G1FY6S00N0000123",
        year=2022,
        make="Chevrolet",
        model="Bolt EV",
        mileage=12340,
        repair_description="Replaced high-voltage battery module",
        part_number="24299461",
        labor_hours=4.2,
        coverage_eligible=True,
        coverage_reason="Vehicle within Voltec warranty: 8yr/100k miles",
    )
