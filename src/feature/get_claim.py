from typing import Optional
from adapter.memory_db import claims_db
from domain.models import AnalyzeClaimResponse


class GetClaimFeature:
    def execute(self, claim_id: str) -> Optional[AnalyzeClaimResponse]:
        return claims_db.get_claim(claim_id)
