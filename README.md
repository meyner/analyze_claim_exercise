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
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uv run python src/main.py
```
The API will be available at `http://localhost:8000`. You can view the interactive docs at `/docs`.

---

## Design Decisions

### 1. Agentic Workflow vs. Strict Pipeline
Instead of a rigid "Extract → Validate → Check" pipeline, this project opts for an **agentic workflow**. While a deterministic pipeline is often preferred for high-stakes production systems, the agentic approach was chosen here to demonstrate a more flexible, reasoning-heavy alternative.

**Trade-offs:**
- **Pros (Flexibility & Intelligence):** The agent naturally handles "fuzzy" inputs and non-linear logic. If a VIN is missing, it skips validation; if a tool returns an error, it can reason about that failure and incorporate it into the final response without requiring complex `if/else` branching in Python.
- **Cons (Determinism & Latency):** Agentic flows are inherently less predictable than hardcoded pipelines. They rely on the model's ability to follow instructions and can be slower due to the sequential nature of LLM-managed tool calls. **In this implementation, the end-to-end analysis typically takes about 5 seconds.**

By giving the model **agency** over its tools, we shift the complexity from the "glue code" (state machines/graphs) to the **prompt and tool definitions**, allowing the system to adapt to messy, real-world repair order text more fluidly.

### 2. Observability & Agent Tracing
To solve the "black box" problem of LLMs, we implemented a structured logging system:
- **Flow Capture:** Every step of the agentic process is logged, including the initial request, tool calls (even when using Automatic Function Calling), and the final parse result.
- **Production Debugging:** This provides a "Langfuse-lite" trace in the logs, allowing developers to see exactly why an agent made a specific decision or where a tool call might have received unexpected arguments.

### 3. Graceful Degradation (Always-Responding)
The system is designed to be robust against "garbage" data or missing fields:
- **Full Payload Guarantees:** The API is instructed to always return a full JSON response. If data is missing, fields are set to `null` rather than omitting them or failing the request.
- **Actionable Reasons:** The `coverage_reason` field is used to provide clear, human-readable explanations for any failures (e.g., "Odometer reading of 112,500 miles exceeds the 100,000-mile warranty limit") rather than generic error codes.

### 4. Modern Async Stack (FastAPI)
The project is built on **FastAPI** to leverage the modern Python asynchronous ecosystem.
- **Concurrency for I/O:** LLM calls and tool executions are I/O-bound operations. Using an `async` stack allows the server to handle multiple concurrent requests efficiently without blocking on a single agent's reasoning loop.
- **Type Safety & Validation:** By using Pydantic models for both the domain and the API layer, we get automatic request validation and clear, self-documenting schemas (OpenAPI/Swagger) out of the box—a significant step up from traditional synchronous frameworks like Flask.

---

## Testing
Unit tests cover tool logic, memory database operations, and agent parsing:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uv run pytest tests
```
