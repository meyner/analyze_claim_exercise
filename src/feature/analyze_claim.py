import uuid
from adapter.agents import GeminiAgent
from adapter.agents.prompts import CLAIM_ANALYSIS_PROMPT
from adapter.memory_db import claims_db
from domain.models import AnalyzeClaimResponse

class ClaimAnalysisFeature:
    def __init__(self):
        self.agent = GeminiAgent()

    async def execute(self, ro_text: str) -> AnalyzeClaimResponse:
        claim_id = str(uuid.uuid4())
        result = await self.agent.analyze_claim(CLAIM_ANALYSIS_PROMPT, ro_text)
        claim = AnalyzeClaimResponse(claim_id=claim_id, **result)
        claims_db.save_claim(claim)
        return claim
