from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent

def _load_prompt(filename: str) -> str:
    return (_PROMPTS_DIR / filename).read_text()

CLAIM_ANALYSIS_PROMPT = _load_prompt("claim_analysis.txt")
