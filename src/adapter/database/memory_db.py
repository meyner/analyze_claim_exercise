from typing import Optional
from domain.models import AnalyzeClaimResponse


class MemoryDatabase:
    def __init__(self):
        self._claims: dict[str, AnalyzeClaimResponse] = {}

    def save_claim(self, claim: AnalyzeClaimResponse) -> None:
        self._claims[claim.claim_id] = claim

    def get_claim(self, claim_id: str) -> Optional[AnalyzeClaimResponse]:
        return self._claims.get(claim_id)

    def __len__(self) -> int:
        return len(self._claims)


# Module-level singleton shared across the app
claims_db = MemoryDatabase()
