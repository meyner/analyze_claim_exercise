import json
import logging
import time
from typing import Optional
from google import genai
from google.genai import types
from config import settings
from domain.models import AnalyzeClaimResponse
from .tools.warranty import check_warranty_coverage
from .tools.validate_vin import validate_vin

logger = logging.getLogger(__name__)

class ClaimAnalysisInternal(AnalyzeClaimResponse):
    vin_valid: Optional[bool] = None
    vin_issues: Optional[list[str]] = None

class GeminiAgent:
    def __init__(self, model_name: str = settings.gemini_model):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = model_name
        self.tools = [validate_vin, check_warranty_coverage]

    def _log_agent_trace(self, response) -> None:
        """Logs each part of the model response for agent observability."""
        try:
            parts = response.candidates[0].content.parts
        except (IndexError, AttributeError):
            logger.warning("agent_trace could not read response parts")
            return

        for part in parts:
            if part.function_call:
                logger.info(
                    f"agent_tool_call tool={part.function_call.name} "
                    f"args={dict(part.function_call.args)}"
                )
            elif part.text:
                preview = part.text[:120].replace("\n", " ")
                logger.info(f"agent_text_part preview=\"{preview}\"")

    async def analyze_claim(self, prompt: str, ro_text: str) -> dict:
        """
        Analyzes the RO text using Gemini with native function calling for warranty checks.
        """
        full_prompt = f"{prompt}\n\nInput Data:\n{ro_text}"

        logger.info(f"agent_request model={self.model_name} ro_length={len(ro_text)}")
        t0 = time.perf_counter()

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                response_json_schema=ClaimAnalysisInternal.model_json_schema(),
            )
        )

        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        self._log_agent_trace(response)
        logger.info(f"agent_response elapsed_ms={elapsed_ms}")

        text = response.text
        if not text:
            raise ValueError("Model returned an empty response. The request may have been blocked or the model failed to generate output.")

        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        try:
            result = json.loads(text)
            logger.info(f"agent_parse_ok coverage_eligible={result.get('coverage_eligible')}")
            return result
        except json.JSONDecodeError:
            logger.error(f"agent_parse_failed raw_preview=\"{response.text[:200]}\"")
            raise ValueError(f"Model returned non-JSON output: {response.text[:500]}")
