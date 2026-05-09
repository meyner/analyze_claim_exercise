import json
from google import genai
from google.genai import types
from config import settings
from .tools.warranty import check_warranty_coverage
from .tools.validate_vin import validate_vin

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
        
        # In the new SDK, we use generate_content with tools and automatic_function_calling
        # The async client is accessed via .aio
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                response_mime_type="application/json",
            )
        )
        
        try:
            # The final response should be the JSON data
            return json.loads(response.text)
        except json.JSONDecodeError:
            # If the model didn't return pure JSON, we might need to extract it
            raise ValueError(f"Failed to parse JSON from Gemini response: {response.text}")

    async def generate_completion(self, prompt: str, content: str) -> str:
        """
        Runs an LLM completion using the Gemini model.
        """
        full_prompt = f"{prompt}\n\nInput Data:\n{content}"
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=full_prompt
        )
        return response.text
