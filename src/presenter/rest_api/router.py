from fastapi import APIRouter
from fastapi.responses import Response

from .models import AnalyzeClaimRequest

router = APIRouter()


@router.post("/analyze-claim", status_code=200)
async def analyze_claim(payload: AnalyzeClaimRequest) -> Response:
    return Response(status_code=200)
