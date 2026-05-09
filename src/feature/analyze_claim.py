import logging
import time
import uuid
from adapter.agents import GeminiAgent
from adapter.agents.prompts import CLAIM_ANALYSIS_PROMPT
from adapter.database.memory_db import claims_db
from domain.models import AnalyzeClaimResponse

logger = logging.getLogger(__name__)

class ClaimAnalysisFeature:
    def __init__(self):
        self.agent = GeminiAgent()

    async def execute(self, ro_text: str) -> AnalyzeClaimResponse:
        claim_id = str(uuid.uuid4())
        logger.info(f"analyze_claim_start claim_id={claim_id} ro_length={len(ro_text)}")
        t0 = time.perf_counter()

        result = await self.agent.analyze_claim(CLAIM_ANALYSIS_PROMPT, ro_text)
        claim = AnalyzeClaimResponse(claim_id=claim_id, **result)
        claims_db.save_claim(claim)

        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            f"analyze_claim_complete claim_id={claim_id} "
            f"vin={claim.vin} coverage_eligible={claim.coverage_eligible} "
            f"elapsed_ms={elapsed_ms}"
        )
        return claim
