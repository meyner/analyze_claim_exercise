from pydantic import BaseModel


class AnalyzeClaimRequest(BaseModel):
    ro_text: str
