from fastapi import APIRouter

from domain.models import AnalyzeClaimResponse
from feature.analyze_claim import ClaimAnalysisFeature
from .models import AnalyzeClaimRequest

router = APIRouter()
feature = ClaimAnalysisFeature()

@router.post("/analyze-claim", response_model=AnalyzeClaimResponse)
async def analyze_claim(payload: AnalyzeClaimRequest) -> AnalyzeClaimResponse:
    return await feature.execute(payload.ro_text)
