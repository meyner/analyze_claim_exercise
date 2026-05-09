import pytest
from adapter.database.memory_db import MemoryDatabase
from domain.models import AnalyzeClaimResponse


def make_claim(claim_id: str = "test-123") -> AnalyzeClaimResponse:
    return AnalyzeClaimResponse(claim_id=claim_id)


def test_get_unknown_claim_returns_none():
    db = MemoryDatabase()
    assert db.get_claim("nonexistent-id") is None


def test_saved_claim_can_be_retrieved():
    db = MemoryDatabase()
    claim = make_claim("abc-123")
    db.save_claim(claim)
    assert db.get_claim("abc-123") == claim


def test_two_claims_stored_independently():
    db = MemoryDatabase()
    claim_a = make_claim("id-a")
    claim_b = make_claim("id-b")
    db.save_claim(claim_a)
    db.save_claim(claim_b)
    assert db.get_claim("id-a") == claim_a
    assert db.get_claim("id-b") == claim_b


def test_saving_same_id_overwrites_previous():
    db = MemoryDatabase()
    claim_v1 = AnalyzeClaimResponse(claim_id="same-id", vin="1G1FY6S0XN0000123")
    claim_v2 = AnalyzeClaimResponse(claim_id="same-id", vin="1G1YY26E955100000")
    db.save_claim(claim_v1)
    db.save_claim(claim_v2)
    assert db.get_claim("same-id").vin == "1G1YY26E955100000"


def test_len_starts_at_zero():
    db = MemoryDatabase()
    assert len(db) == 0


def test_len_increments_with_each_save():
    db = MemoryDatabase()
    db.save_claim(make_claim("x"))
    db.save_claim(make_claim("y"))
    assert len(db) == 2
