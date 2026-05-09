import json
from typing import Optional
from google import genai
from google.genai import types
from config import settings
from domain.models import AnalyzeClaimResponse
from .tools.warranty import check_warranty_coverage
from .tools.validate_vin import validate_vin

class ClaimAnalysisInternal(AnalyzeClaimResponse):
    vin_valid: Optional[bool] = None
    vin_issues: Optional[list[str]] = None

class GeminiAgent:
    def __init__(self, model_name: str = settings.gemini_model):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = model_name
        self.tools = [validate_vin, check_warranty_coverage]

    async def analyze_claim(self, prompt: str, ro_text: str) -> dict:
        """
        Analyzes the RO text using Gemini with native function calling for warranty checks.
        """
        full_prompt = f"{prompt}\n\nInput Data:\n{ro_text}"
        
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                response_json_schema=ClaimAnalysisInternal.model_json_schema(),
            )
        )

        text = response.text
        if text.startswith("```"):
            # Strip markdown code blocks
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse structured response: {response.text}")
