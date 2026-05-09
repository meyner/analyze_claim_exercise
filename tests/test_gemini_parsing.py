import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def _mock_response(text: str) -> MagicMock:
    response = MagicMock()
    response.text = text
    response.candidates = []
    return response


@pytest.fixture
def agent():
    with patch("adapter.agents.gemini.genai.Client"):
        from adapter.agents.gemini import GeminiAgent
        return GeminiAgent()


@pytest.mark.anyio
async def test_valid_json_response_is_parsed(agent):
    payload = {"vin": "1G1FY6S0XN0000123", "coverage_eligible": True}
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response(json.dumps(payload))
    )
    result = await agent.analyze_claim("prompt", "ro_text")
    assert result["vin"] == "1G1FY6S0XN0000123"


@pytest.mark.anyio
async def test_coverage_eligible_false_is_parsed(agent):
    payload = {"vin": "1G1FY6S0XN0000123", "coverage_eligible": False}
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response(json.dumps(payload))
    )
    result = await agent.analyze_claim("prompt", "ro_text")
    assert result["coverage_eligible"] is False


@pytest.mark.anyio
async def test_markdown_json_block_is_stripped(agent):
    payload = {"vin": "1G1FY6S0XN0000123"}
    wrapped = f"```json\n{json.dumps(payload)}\n```"
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response(wrapped)
    )
    result = await agent.analyze_claim("prompt", "ro_text")
    assert result["vin"] == "1G1FY6S0XN0000123"


@pytest.mark.anyio
async def test_plain_markdown_block_is_stripped(agent):
    payload = {"vin": "1G1FY6S0XN0000123"}
    wrapped = f"```\n{json.dumps(payload)}\n```"
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response(wrapped)
    )
    result = await agent.analyze_claim("prompt", "ro_text")
    assert result["vin"] == "1G1FY6S0XN0000123"


@pytest.mark.anyio
async def test_empty_response_text_raises(agent):
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response("")
    )
    with pytest.raises(ValueError, match="empty response"):
        await agent.analyze_claim("prompt", "ro_text")


@pytest.mark.anyio
async def test_none_response_text_raises(agent):
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response(None)
    )
    with pytest.raises(ValueError, match="empty response"):
        await agent.analyze_claim("prompt", "ro_text")


@pytest.mark.anyio
async def test_non_json_response_raises(agent):
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response("Sorry, I cannot process this request.")
    )
    with pytest.raises(ValueError, match="non-JSON"):
        await agent.analyze_claim("prompt", "ro_text")


@pytest.mark.anyio
async def test_partial_json_response_raises(agent):
    agent.client.aio.models.generate_content = AsyncMock(
        return_value=_mock_response('{"vin": "1G1FY6S0XN0000123"')
    )
    with pytest.raises(ValueError, match="non-JSON"):
        await agent.analyze_claim("prompt", "ro_text")
