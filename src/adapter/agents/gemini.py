import google.generativeai as genai
from config import settings

class GeminiAgent:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(model_name)

    async def generate_completion(self, prompt: str, content: str) -> str:
        """
        Runs an LLM completion using the Gemini model.
        """
        full_prompt = f"{prompt}\n\nInput Data:\n{content}"
        # Note: google-generativeai's async support might vary by version, 
        # but for this exercise we'll wrap it or use the async method if available.
        # generate_content_async is available in recent versions.
        response = await self.model.generate_content_async(full_prompt)
        return response.text
