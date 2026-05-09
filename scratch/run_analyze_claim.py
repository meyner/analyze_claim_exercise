import sys
import os
import asyncio
import json

# Add src to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from feature.analyze_claim import ClaimAnalysisFeature
from config import settings

async def run_analysis(feature, ro_text, label):
    print(f"--- {label} ---")
    print(f"Input RO text: {ro_text}\n")
    try:
        result = await feature.execute(ro_text)
        print("Analysis Result:")
        print(json.dumps(result.model_dump(), indent=2))
    except Exception as e:
        print(f"Error during analysis: {e}")
    print("\n")

async def main():
    # Check if API key is set
    if not settings.gemini_api_key:
        print("Error: GEMINI_API_KEY not found in .env.local")
        return

    feature = ClaimAnalysisFeature()
    
    # 1. Valid Data Case
    valid_ro = "RO# 847291 | VIN: 1G1FY6S0XN0000123 | 2022 Chevrolet Bolt EV | Mileage: 12,340 | Repair: Replaced high-voltage battery module. | Parts: 24299461 | Labor: 4.2 hrs"
    await run_analysis(feature, valid_ro, "VALID DATA RUN")

    # 2. Invalid Data Case (High mileage - out of warranty)
    invalid_ro = "RO# 999999 | VIN: 1G1FY6S0XN0000123 | 2022 Chevrolet Bolt EV | Mileage: 150,000 | Repair: Replaced high-voltage battery module. | Parts: 24299461 | Labor: 4.2 hrs"
    await run_analysis(feature, invalid_ro, "INVALID DATA RUN (OUT OF WARRANTY)")

if __name__ == "__main__":
    asyncio.run(main())
