import json
import google.generativeai as genai
from config import settings
from .tools.warranty import check_warranty_coverage

class GeminiAgent:
    def __init__(self, model_name: str = settings.gemini_model):
        genai.configure(api_key=settings.gemini_api_key)
        # Initialize model with tools
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=[check_warranty_coverage]
        )

    async def analyze_claim(self, prompt: str, ro_text: str) -> dict:
        """
        Analyzes the RO text using Gemini with native function calling for warranty checks.
        """
        # Start a chat session with automatic function calling enabled
        chat = self.model.start_chat(enable_automatic_function_calling=True)
        
        full_prompt = f"{prompt}\n\nInput Data:\n{ro_text}"
        
        # Send message and let Gemini decide whether to call the tool
        response = await chat.send_message_async(
            full_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        try:
            # The final response should be the JSON data
            return json.loads(response.text)
        except json.JSONDecodeError:
            # If the model didn't return pure JSON, we might need to extract it
            # or handle the error. For now, we'll raise.
            raise ValueError(f"Failed to parse JSON from Gemini response: {response.text}")

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
