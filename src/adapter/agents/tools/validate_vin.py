# World Manufacturer Identifier (WMI) prefix -> make
WMI_MAKE_MAP = {
    "1G1": "Chevrolet",
    "1G2": "Pontiac",
    "1G4": "Buick",
    "1G6": "Cadillac",
    "1GC": "Chevrolet",
    "1GT": "GMC",
    "1FA": "Ford",
    "1FB": "Ford",
    "1FC": "Ford",
    "1FD": "Ford",
    "1FM": "Ford",
    "1FT": "Ford",
    "1FU": "Freightliner",
    "1C3": "Chrysler",
    "1C4": "Chrysler",
    "2T1": "Toyota",
    "JHM": "Honda",
    "JTD": "Toyota",
    "WBA": "BMW",
    "WVW": "Volkswagen",
}


def get_years_for_vin_char(char: str) -> set[int]:
    """
    Returns the set of possible model years for a given VIN year character.
    VIN year characters repeat every 30 years starting from 1980.
    """
    vin_chars = "ABCDEFGHJKLMNPRSTVWXY123456789"
    if char not in vin_chars:
        return set()
    
    index = vin_chars.index(char)
    base_year = 1980 + index
    # Return the last 3 cycles (covers 1980 to 2069)
    return {base_year, base_year + 30, base_year + 60}


def validate_vin(vin: str, make: str, model: str, year: int) -> dict:
    """
    Validates whether a VIN is consistent with the extracted make, model, and year
    using standard VIN decoding logic (WMI prefix and model year character).
    This tool MUST be called whenever a VIN is present in the repair order text.

    Args:
        vin: The 17-character Vehicle Identification Number to validate.
        make: The vehicle manufacturer extracted from the RO text.
        model: The vehicle model name extracted from the RO text.
        year: The vehicle model year extracted from the RO text.

    Returns:
        {
            "vin_valid": bool,
            "vin_issues": list[str]  # empty list if valid
        }
    """
    issues = []

    # Basic length check
    if len(vin) != 17:
        issues.append(f"VIN must be exactly 17 characters, got {len(vin)}.")
        return {"vin_valid": False, "vin_issues": issues}

    # Forbidden characters (I, O, Q are not allowed in VINs)
    forbidden = set("IOQ")
    bad_chars = [c for c in vin.upper() if c in forbidden]
    if bad_chars:
        issues.append(f"VIN contains invalid characters: {', '.join(set(bad_chars))}.")

    # WMI check (first 3 characters)
    wmi = vin[:3].upper()
    expected_make = WMI_MAKE_MAP.get(wmi)
    if expected_make is None:
        issues.append(f"WMI '{wmi}' is not a recognized manufacturer identifier.")
    elif expected_make.lower() != make.strip().lower():
        issues.append(
            f"WMI '{wmi}' indicates manufacturer '{expected_make}', but extracted make is '{make}'."
        )

    # Model year character (position 10, 0-indexed)
    year_char = vin[9].upper()
    valid_years = get_years_for_vin_char(year_char)
    
    if not valid_years:
        issues.append(f"Model year character '{year_char}' (position 10) is unrecognized.")
    elif year not in valid_years:
        # For the error message, show the most likely year (the one closest to the input year)
        best_match = min(valid_years, key=lambda x: abs(x - year))
        issues.append(
            f"Model year character '{year_char}' (position 10) decodes to {best_match} (or {sorted(list(valid_years - {best_match}))}), "
            f"but extracted year is {year}."
        )

    return {"vin_valid": len(issues) == 0, "vin_issues": issues}
