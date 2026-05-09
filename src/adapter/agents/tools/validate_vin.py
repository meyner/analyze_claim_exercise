VIN_YEAR_MAP = {
    "A": 1980, "B": 1981, "C": 1982, "D": 1983, "E": 1984,
    "F": 1985, "G": 1986, "H": 1987, "J": 1988, "K": 1989,
    "L": 1990, "M": 1991, "N": 1992, "P": 1993, "R": 1994,
    "S": 1995, "T": 1996, "V": 1997, "W": 1998, "X": 1999,
    "Y": 2000, "1": 2001, "2": 2002, "3": 2003, "4": 2004,
    "5": 2005, "6": 2006, "7": 2007, "8": 2008, "9": 2009,
    "A2": 2010, "B2": 2011, "C2": 2012, "D2": 2013, "E2": 2014,
    "F2": 2015, "G2": 2016, "H2": 2017, "J2": 2018, "K2": 2019,
    "L2": 2020, "M2": 2021, "N2": 2022, "P2": 2023, "R2": 2024,
}

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
    # Handle 2010+ two-key lookup by checking single-char first, then appending "2"
    decoded_year = VIN_YEAR_MAP.get(year_char) or VIN_YEAR_MAP.get(year_char + "2")
    if decoded_year is None:
        issues.append(f"Model year character '{year_char}' (position 10) is unrecognized.")
    elif decoded_year != year:
        issues.append(
            f"Model year character '{year_char}' (position 10) decodes to {decoded_year}, "
            f"but extracted year is {year}."
        )

    return {"vin_valid": len(issues) == 0, "vin_issues": issues}
