# Analyze Claim Exercise

A warranty claim analysis system that extracts structured data from unstructured repair orders (RO) using an agentic LLM workflow.

---

## Setup

### Prerequisites
- **Python 3.12+**
- **uv** (Fast Python package manager)

### Environment Configuration
Create a `src/.env.local` file with your Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

### Installation
```bash
uv sync
```

### Running the API

#### Option A: Local Development (uv)
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uv run python src/main.py
```

#### Option B: Docker (Recommended)
The easiest way to run the API is using Docker Compose. A helper script is provided to manage the environment and build the container:

```bash
./run_docker.sh
```
*Note: The script will automatically detect your `src/.env.local` and use it for the container.*

The API will be available at `http://localhost:8000`. You can view the interactive docs at `/docs`.

---

## Design Decisions

### 1. Agentic Workflow: Tools as Capabilities
Instead of a rigid "Extract → Validate → Check" pipeline, this project opts for an **agentic workflow**. While a deterministic pipeline is often preferred for high-stakes production systems, the agentic approach was chosen here to demonstrate a more flexible, reasoning-heavy alternative.

- **Tools as Options:** `validate_vin` and `check_warranty_coverage` are not just steps; they are **capabilities** granted to the agent. By exposing them as tools, the agent can choose *when* and *if* to call them based on the quality of the extracted data.
- **Win Condition vs. Scripting:** Rather than scripting every edge case (e.g., "what if the VIN is 16 chars?"), we define a "Win Condition"—a complete, validated JSON response. The agent uses its internal logic to navigate the messy input toward this goal, using tools to resolve uncertainties.
- **Trade-offs:**
    - **Pros (Flexibility & Intelligence):** The agent naturally handles "fuzzy" inputs and non-linear logic. If a VIN is missing, it skips validation; if a tool returns an error, it can reason about that failure and incorporate it into the final response without requiring complex `if/else` branching in Python.
    - **Cons (Determinism & Latency):** Agentic flows are inherently less predictable than hardcoded pipelines. They rely on the model's ability to follow instructions and can be slower due to the sequential nature of LLM-managed tool calls. **In this implementation, the end-to-end analysis typically takes about 5 seconds.**

By giving the model **agency** over its tools, we shift the complexity from the "glue code" (state machines/graphs) to the **prompt and tool definitions**, allowing the system to adapt to messy, real-world repair order text more fluidly.

### 2. Observability & Agent Tracing
Because the Google GenAI SDK uses **Automatic Function Calling (AFC)**, the model's internal tool-calling turns are handled by the SDK and are not exposed in the final response object. Attempting to read them from the response would only show the final text output.

Instead, logging is placed directly inside the tool functions, capturing both inputs and return values at the boundary where Python code actually executes. This gives an accurate, complete trace of what the agent did:

```
analyze_claim_start   claim_id=... ro_length=161
agent_request         model=gemini-2.5-flash
tool_call             validate_vin vin=1G1FY6S0XN0000123 make=Chevrolet year=2022
tool_result           validate_vin vin_valid=True issues=[]
tool_call             check_warranty_coverage vin=1G1FY6S0XN0000123 mileage=12340
tool_result           check_warranty_coverage eligible=True warranty_type=Voltec
agent_response        elapsed_ms=5312
agent_parse_ok        coverage_eligible=True
analyze_claim_complete claim_id=... vin=1G1FY6S0XN0000123 coverage_eligible=True
```

If a claim is wrongly denied, you can look up the `claim_id` in the logs and see exactly what the tool returned — not just what the model was asked to call.

### 3. Graceful Degradation (Always-Responding)
The system is designed to be robust against "garbage" data or missing fields:
- **Full Payload Guarantees:** The API is instructed to always return a full JSON response. If data is missing, fields are set to `null` rather than omitting them or failing the request.
- **Actionable Reasons:** The `coverage_reason` field is used to provide clear, human-readable explanations for any failures (e.g., "Odometer reading of 112,500 miles exceeds the 100,000-mile warranty limit") rather than generic error codes.

### 4. Modern Async Stack (FastAPI)
The project is built on **FastAPI** to leverage the modern Python asynchronous ecosystem.
- **Concurrency for I/O:** LLM calls and tool executions are I/O-bound operations. Using an `async` stack allows the server to handle multiple concurrent requests efficiently without blocking on a single agent's reasoning loop.
- **Type Safety & Validation:** By using Pydantic models for both the domain and the API layer, we get automatic request validation and clear, self-documenting schemas (OpenAPI/Swagger) out of the box—a significant step up from traditional synchronous frameworks like Flask.

### 5. Safety & Error Handling
The system implements a "fail-safe" rather than a "catch-all" approach:
- **Input Guards:** Tools use strict type and presence checks (e.g., `isinstance(year, int)`) to return structured error messages back to the agent instead of raising Python exceptions. This allows the agent to reason about the failure.
- **Prompt-Level Recovery:** The agent's prompt includes explicit instructions (**Step 3a**) on how to handle tool failures, ensuring it still returns a valid JSON payload with a clear `coverage_reason`.
- **Global Safety Net:** FastAPI exception handlers catch `ValueError` (for agent parsing issues) and generic `Exception` (for system crashes), returning clean `422` or `500` responses to the client while logging full stack traces for developers.

---

## Testing
Unit tests cover tool logic, memory database operations, and agent parsing:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uv run pytest tests
```

---

## AI Tooling & Productivity

This project was developed using a "Human-in-the-loop" AI-augmented workflow, leveraging specialized agents to accelerate development:

- **Cursor:** Used as the primary IDE and orchestration layer. Its agentic capabilities allowed for rapid refactoring, such as moving the database logic from the presenter to the feature layer and ensuring architectural consistency across the project.
- **Gemini 3 Flash:** Served as the "brain" of the application. Its native support for **Automatic Function Calling (AFC)** and structured JSON output (via `response_json_schema`) significantly reduced the amount of manual "glue code" required to connect the LLM to the Python tools.
- **Claude (Sonnet 4.6):** Utilized for high-level architectural planning, prompt engineering, and complex logic verification (such as the VIN checksum algorithm).

At times, both models were used to cross-reference each other on certain logic pieces, which allowed me to catch errors or inconsistencies. Approaching the same problem from a fresh angle proved invaluable for identifying edge cases and ensuring robustness.

By using these tools in concert, we were able to implement a robust, tested, and observable system with a clean separation of concerns in a fraction of the time a traditional development cycle would require.
