from fastapi import APIRouter, HTTPException

from domain.models import AnalyzeClaimResponse
from feature.analyze_claim import ClaimAnalysisFeature
from feature.get_claim import GetClaimFeature
from .models import AnalyzeClaimRequest

router = APIRouter()
analyze_claim_feature = ClaimAnalysisFeature()
get_claim_feature = GetClaimFeature()

@router.post("/analyze-claim", response_model=AnalyzeClaimResponse, status_code=201)
async def analyze_claim(payload: AnalyzeClaimRequest) -> AnalyzeClaimResponse:
    return await analyze_claim_feature.execute(payload.ro_text)

@router.get("/claims/{claim_id}", response_model=AnalyzeClaimResponse)
async def get_claim(claim_id: str) -> AnalyzeClaimResponse:
    claim = get_claim_feature.execute(claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail=f"Claim '{claim_id}' not found.")
    return claim
