import os
from fastapi import APIRouter

from domain.models import AnalyzeClaimResponse
from adapter.agents import GeminiAgent
from .models import AnalyzeClaimRequest

router = APIRouter()
agent = GeminiAgent()

# Load prompt
PROMPT_PATH = os.path.join(
    os.path.dirname(__file__), 
    "../../adapter/agents/prompts/claim_analysis.txt"
)

def get_prompt():
    with open(PROMPT_PATH, "r") as f:
        return f.read()

@router.post("/analyze-claim", response_model=AnalyzeClaimResponse)
async def analyze_claim(payload: AnalyzeClaimRequest) -> AnalyzeClaimResponse:
    prompt = get_prompt()
    result = await agent.analyze_claim(prompt, payload.ro_text)
    return AnalyzeClaimResponse(**result)
