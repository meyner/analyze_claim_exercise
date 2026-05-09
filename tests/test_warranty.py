import pytest
from adapter.agents.tools.warranty import check_warranty_coverage

def test_warranty_none_vin():
    result = check_warranty_coverage(
        vin=None, make="Chevrolet", model="Bolt EV",
        year=2022, mileage=12340, part_number="24299461"
    )
    assert result["eligible"] is False
    assert "VIN is missing or invalid" in result["reason"]

def test_warranty_invalid_mileage_type():
    result = check_warranty_coverage(
        vin="1G1FY6S0XN0000123", make="Chevrolet", model="Bolt EV",
        year=2022, mileage="12340", part_number="24299461"
    )
    assert result["eligible"] is False
    assert "mileage must be an integer" in result["reason"]

def test_warranty_eligible_chevrolet():
    # 1G1 is Chevrolet, mileage < 100,000
    result = check_warranty_coverage(
        vin="1G1FY6S0XN0000123",
        make="Chevrolet",
        model="Bolt EV",
        year=2022,
        mileage=12340,
        part_number="24299461"
    )
    assert result["eligible"] is True
    assert result["warranty_type"] == "Voltec"

def test_warranty_eligible_powertrain():
    # 1G1 is Chevrolet, mileage < 100,000, not a Bolt
    result = check_warranty_coverage(
        vin="1G1YY26E955100000",
        make="Chevrolet",
        model="Corvette",
        year=2005,
        mileage=50000,
        part_number="12345678"
    )
    assert result["eligible"] is True
    assert result["warranty_type"] == "Powertrain"

def test_warranty_ineligible_mileage():
    # Mileage >= 100,000
    result = check_warranty_coverage(
        vin="1G1FY6S0XN0000123",
        make="Chevrolet",
        model="Bolt EV",
        year=2022,
        mileage=150000,
        part_number="24299461"
    )
    assert result["eligible"] is False
    assert "outside of standard warranty coverage limits" in result["reason"]

def test_warranty_ineligible_wmi():
    # 1FA is Ford, not in 1G1 check
    result = check_warranty_coverage(
        vin="1FAFY6S0XN0000123",
        make="Ford",
        model="Mustang",
        year=2022,
        mileage=10000,
        part_number="12345678"
    )
    assert result["eligible"] is False
    assert "outside of standard warranty coverage limits" in result["reason"]
