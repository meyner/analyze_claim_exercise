# Analyze claim exercise

Warranty claim analysis from unstructured repair orders: extract structured data with an LLM, evaluate coverage with a Python tool, and return a single structured API response.

---

## Scenario

A warranty claims adjuster pastes the text from a repair order (RO) into your system. The RO holds unstructured information about the vehicle, the work performed, and the parts used. Your API should:

1. **Extract** structured claim data from the RO text using an LLM.
2. **Invoke** the provided Python tool to check warranty coverage eligibility.
3. **Respond** with structured output that includes both the extracted fields and the coverage determination.

---

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **Python** | 3.12 or newer (`requires-python` in `pyproject.toml` is `>=3.12`). |
| **uv** | Fast Python package and project manager. [Install uv](https://docs.astral.sh/uv/getting-started/installation/). |

Verify versions:

```bash
python3 --version   # expect 3.12.x or higher
uv --version
```

---

## Setup

1. **Clone the repository** (or open it in your editor) and go to the project root:

   ```bash
   cd analyze_claim_exercise
   ```

2. **Install dependencies** with uv (uses `pyproject.toml` and locks versions with `uv.lock`):

   ```bash
   uv sync
   ```

3. **Run the project** (example entrypoint):

   ```bash
   uv run python main.py
   ```

   Commands run inside uv’s managed environment, so you do not need to activate a virtualenv manually.

---

## Project layout

- `pyproject.toml` — project metadata and dependencies.
- `uv.lock` — locked dependency versions for reproducible installs.
- `main.py` — application entrypoint (replace or extend as you implement the scenario above).

When you add LLM or external API configuration, document any required environment variables or secrets in this file under a short **Configuration** subsection.
