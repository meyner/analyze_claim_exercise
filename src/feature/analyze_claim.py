from adapter.agents import GeminiAgent
from adapter.agents.prompts import CLAIM_ANALYSIS_PROMPT
from domain.models import AnalyzeClaimResponse

class ClaimAnalysisFeature:
    def __init__(self):
        self.agent = GeminiAgent()

    async def execute(self, ro_text: str) -> AnalyzeClaimResponse:
        result = await self.agent.analyze_claim(CLAIM_ANALYSIS_PROMPT, ro_text)
        return AnalyzeClaimResponse(**result)
