from pathlib import Path

# normally prompt should be stored in a database or a file storage system so it is centralized and any service can access it

_PROMPTS_DIR = Path(__file__).parent

def _load_prompt(filename: str) -> str:
    return (_PROMPTS_DIR / filename).read_text()

CLAIM_ANALYSIS_PROMPT = _load_prompt("claim_analysis.txt")
