from fastapi import APIRouter, HTTPException

from adapter.memory_db import claims_db
from domain.models import AnalyzeClaimResponse
from feature.analyze_claim import ClaimAnalysisFeature
from .models import AnalyzeClaimRequest

router = APIRouter()
feature = ClaimAnalysisFeature()

@router.post("/analyze-claim", response_model=AnalyzeClaimResponse, status_code=201)
async def analyze_claim(payload: AnalyzeClaimRequest) -> AnalyzeClaimResponse:
    return await feature.execute(payload.ro_text)

@router.get("/claims/{claim_id}", response_model=AnalyzeClaimResponse)
async def get_claim(claim_id: str) -> AnalyzeClaimResponse:
    claim = claims_db.get_claim(claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail=f"Claim '{claim_id}' not found.")
    return claim
