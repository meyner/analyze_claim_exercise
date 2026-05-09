import sys
import os
import asyncio
import json

# Add src to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from feature.analyze_claim import ClaimAnalysisFeature
from feature.get_claim import GetClaimFeature
from config import settings

async def run_analysis(feature, ro_text, label):
    print(f"--- {label} ---")
    print(f"Input RO text: {ro_text}\n")
    try:
        result = await feature.execute(ro_text)
        print("Analysis Result:")
        print(json.dumps(result.model_dump(), indent=2))
        return result.claim_id
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None
    finally:
        print()

def run_get_claim(feature, claim_id, label):
    print(f"--- {label} ---")
    result = feature.execute(claim_id)
    if result:
        print(json.dumps(result.model_dump(), indent=2))
    else:
        print(f"Claim '{claim_id}' not found.")
    print()

async def main():
    if not settings.gemini_api_key:
        print("Error: GEMINI_API_KEY not found in .env.local")
        return

    analyze = ClaimAnalysisFeature()
    get_claim = GetClaimFeature()

    valid_ro = "RO# 847291 | VIN: 1G1FY6S0XN0000123 | 2022 Chevrolet Bolt EV | Mileage: 12,340 | Repair: Replaced high-voltage battery module. | Parts: 24299461 | Labor: 4.2 hrs"
    claim_id_1 = await run_analysis(analyze, valid_ro, "ANALYZE CLAIM 1 (valid, in warranty)")

    invalid_ro = "RO# 999999 | VIN: 1G1FY6S0XN0000123 | 2022 Chevrolet Bolt EV | Mileage: 150,000 | Repair: Replaced high-voltage battery module. | Parts: 24299461 | Labor: 4.2 hrs"
    claim_id_2 = await run_analysis(analyze, invalid_ro, "ANALYZE CLAIM 2 (valid VIN, out of warranty)")

    if claim_id_1:
        run_get_claim(get_claim, claim_id_1, f"GET CLAIM 1 ({claim_id_1})")
    if claim_id_2:
        run_get_claim(get_claim, claim_id_2, f"GET CLAIM 2 ({claim_id_2})")

if __name__ == "__main__":
    asyncio.run(main())
