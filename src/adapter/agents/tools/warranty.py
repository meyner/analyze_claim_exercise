import logging

logger = logging.getLogger(__name__)

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
    This tool MUST be called when vin, make, model, year, mileage, and part_number
    are all successfully extracted from the repair order text.
    The coverage_reason in the final response must incorporate both this result
    and the outcome of validate_vin.

    Args:
        vin: The Vehicle Identification Number.
        make: The vehicle manufacturer.
        model: The vehicle model name.
        year: The vehicle model year.
        mileage: The current odometer reading.
        part_number: The primary part number being replaced.
    """
    logger.info(f"tool_call check_warranty_coverage vin={vin} mileage={mileage}")
    # NOTE: part_number is not used for anything in this mocked tool

    def _result(result: dict) -> dict:
        if result["eligible"]:
            logger.info(f"tool_result check_warranty_coverage eligible=True warranty_type={result['warranty_type']}")
        else:
            logger.warning(f"tool_result check_warranty_coverage eligible=False reason=\"{result['reason']}\"")
        return result

    if not vin or not isinstance(vin, str):
        return _result({"eligible": False, "reason": "Warranty check failed: VIN is missing or invalid.", "warranty_type": "None"})
    if not isinstance(mileage, int):
        return _result({"eligible": False, "reason": f"Warranty check failed: mileage must be an integer, got {type(mileage).__name__}.", "warranty_type": "None"})

    # Reasonable stub/mock for testing
    if "1G1" in vin and mileage < 100000:
        return _result({
            "eligible": True,
            "reason": f"Vehicle within {year} {make} {model} warranty limits.",
            "warranty_type": "Voltec" if "Bolt" in model else "Powertrain"
        })

    return _result({
        "eligible": False,
        "reason": "Vehicle outside of standard warranty coverage limits.",
        "warranty_type": "None"
    })
