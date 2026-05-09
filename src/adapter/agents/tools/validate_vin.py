import logging

logger = logging.getLogger(__name__)

# World Manufacturer Identifier (WMI) prefix -> make
WMI_MAKE_MAP = {
    "1G1": "Chevrolet",
    "1G2": "Pontiac",
    "1G4": "Buick",
    "1G6": "Cadillac",
    "1GC": "Chevrolet",
    "1GN": "Chevrolet",
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

# VIN character values for checksum calculation
VIN_CHAR_VALUES = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
    'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

# VIN position weights for checksum calculation
VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def calculate_vin_checksum(vin: str) -> str:
    """
    Calculates the expected check digit (9th character) for a VIN.
    The 9th character (index 8) has a weight of 0 in the standard.
    """
    total = 0
    for i, char in enumerate(vin.upper()):
        val = VIN_CHAR_VALUES.get(char)
        if val is None:
            return ""  # Invalid character handled elsewhere
        total += val * VIN_WEIGHTS[i]
    
    remainder = total % 11
    return "X" if remainder == 10 else str(remainder)


def get_years_for_vin_char(char: str) -> set[int]:
    """
    Returns the set of possible model years for a given VIN year character.
    VIN year characters repeat every 30 years starting from 1980.
    Note: VIN year characters (position 10) exclude I, O, Q, U, Z, and 0.
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
    logger.info(f"tool_call validate_vin vin={vin} make={make} year={year}")

    def _result(valid: bool, issues: list) -> dict:
        result = {"vin_valid": valid, "vin_issues": issues}
        if valid:
            logger.info("tool_result validate_vin vin_valid=True issues=[]")
        else:
            logger.warning(f"tool_result validate_vin vin_valid=False issues={issues}")
        return result

    if not vin or not isinstance(vin, str):
        return _result(False, ["VIN is missing or not a valid string."])
    if not make or not isinstance(make, str):
        return _result(False, ["Make is missing or not a valid string."])
    if not isinstance(year, int):
        return _result(False, [f"Year must be an integer, got: {type(year).__name__}."])

    issues = []

    # Basic length check
    if len(vin) != 17:
        issues.append(f"VIN must be exactly 17 characters, got {len(vin)}.")
        return _result(False, issues)

    # Forbidden characters (I, O, Q are not allowed in VINs)
    forbidden = set("IOQ")
    bad_chars = [c for c in vin.upper() if c in forbidden]
    if bad_chars:
        issues.append(f"VIN contains invalid characters: {', '.join(set(bad_chars))}.")
    else:
        # Checksum validation (only if no invalid characters)
        expected_check = calculate_vin_checksum(vin)
        actual_check = vin[8].upper()
        if expected_check and actual_check != expected_check:
            issues.append(
                f"VIN checksum failed. Expected check digit '{expected_check}' at position 9, but found '{actual_check}'."
            )

    # WMI check (first 3 characters)
    # Note: If the 3rd digit is '9', it's a small manufacturer, and the WMI
    # is actually defined by positions 1, 2, 3, 12, 13, and 14.
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

    return _result(len(issues) == 0, issues)
