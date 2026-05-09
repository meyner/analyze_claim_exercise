import logging
from typing import Optional
from adapter.database.memory_db import claims_db
from domain.models import AnalyzeClaimResponse

logger = logging.getLogger(__name__)

class GetClaimFeature:
    def execute(self, claim_id: str) -> Optional[AnalyzeClaimResponse]:
        claim = claims_db.get_claim(claim_id)
        if claim is None:
            logger.warning(f"get_claim_miss claim_id={claim_id}")
        else:
            logger.info(f"get_claim_hit claim_id={claim_id}")
        return claim
