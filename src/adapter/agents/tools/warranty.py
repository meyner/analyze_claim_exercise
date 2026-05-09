def check_warranty_coverage(
    vin: str,
    make: str,
    model: str,
    year: int,
    mileage: int,
    part_number: str
) -> dict:
    """
    Determines warranty coverage eligibility for a vehicle and repair. 
    If all parameters (vin, make, model, year, mileage, part_number) are extracted from the text, 
    this tool MUST be called to get coverage details.

    Args:
        vin: The Vehicle Identification Number.
        make: The vehicle manufacturer.
        model: The vehicle model name.
        year: The vehicle model year.
        mileage: The current odometer reading.
        part_number: The primary part number being replaced.
    """
    # Reasonable stub/mock for testing
    if "1G1" in vin and mileage < 100000:
        return {
            "eligible": True,
            "reason": f"Vehicle within {year} {make} {model} warranty limits.",
            "warranty_type": "Voltec" if "Bolt" in model else "Powertrain"
        }
    
    return {
        "eligible": False,
        "reason": "Vehicle outside of standard warranty coverage limits.",
        "warranty_type": "None"
    }
