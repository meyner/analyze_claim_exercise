import pytest
from adapter.agents.tools.validate_vin import validate_vin, calculate_vin_checksum

def test_vin_none_input():
    result = validate_vin(None, "Chevrolet", "Bolt EV", 2022)
    assert result["vin_valid"] is False
    assert "missing or not a valid string" in result["vin_issues"][0]

def test_vin_none_make():
    result = validate_vin("1G1FY6S0XN0000123", None, "Bolt EV", 2022)
    assert result["vin_valid"] is False
    assert "Make is missing" in result["vin_issues"][0]

def test_vin_invalid_year_type():
    result = validate_vin("1G1FY6S0XN0000123", "Chevrolet", "Bolt EV", "2022")
    assert result["vin_valid"] is False
    assert "Year must be an integer" in result["vin_issues"][0]

def test_vin_length_too_short():
    result = validate_vin("123", "Chevrolet", "Bolt EV", 2022)
    assert result["vin_valid"] is False
    assert "VIN must be exactly 17 characters" in result["vin_issues"][0]

def test_vin_length_too_long():
    result = validate_vin("1" * 18, "Chevrolet", "Bolt EV", 2022)
    assert result["vin_valid"] is False
    assert "VIN must be exactly 17 characters" in result["vin_issues"][0]

def test_vin_forbidden_characters():
    # I, O, Q are forbidden
    result = validate_vin("1G1FY6S0IX0000123", "Chevrolet", "Bolt EV", 2022)
    assert result["vin_valid"] is False
    assert "VIN contains invalid characters: I" in result["vin_issues"][0]

def test_vin_checksum_valid():
    # 1G1FY6S0XN0000123 is valid (checksum 'X' at index 8)
    result = validate_vin("1G1FY6S0XN0000123", "Chevrolet", "Bolt EV", 2022)
    assert result["vin_valid"] is True
    assert len(result["vin_issues"]) == 0

def test_vin_checksum_invalid():
    # Change 'X' to '0' to fail checksum
    result = validate_vin("1G1FY6S00N0000123", "Chevrolet", "Bolt EV", 2022)
    assert result["vin_valid"] is False
    assert "VIN checksum failed" in result["vin_issues"][0]

def test_vin_wmi_mismatch():
    # 1FA is Ford, but we pass Chevrolet
    # VIN: 1FAFY6S0XN0000123 (checksum might fail, that's okay, we check for the WMI issue specifically)
    result = validate_vin("1FAFY6S0XN0000123", "Chevrolet", "Bolt EV", 2022)
    assert result["vin_valid"] is False
    assert any("indicates manufacturer 'Ford', but extracted make is 'Chevrolet'" in issue for issue in result["vin_issues"])

def test_vin_year_mismatch():
    # 'N' (index 9) is 2022 (or 1992, 2052), but we pass 2021
    result = validate_vin("1G1FY6S0XN0000123", "Chevrolet", "Bolt EV", 2021)
    assert result["vin_valid"] is False
    assert "decodes to 2022" in result["vin_issues"][0]

def test_calculate_vin_checksum_x():
    # Test case where remainder is 10 (X)
    assert calculate_vin_checksum("1G1FY6S0XN0000123") == "X"

def test_calculate_vin_checksum_numeric():
    # Test case where remainder is numeric (e.g. 1G1YY26E955100000 -> 9)
    assert calculate_vin_checksum("1G1YY26E955100000") == "9"
