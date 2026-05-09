import sys
import os

# Add src to path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import settings

if settings.gemini_api_key:
    print("Success: API Key loaded!")
else:
    print("Notice: API Key is empty (as expected if no .env.local file exists yet).")
