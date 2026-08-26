# geo.py

def is_valid_us_zip(zip_code: str) -> bool:
    """Return True if the input is a valid 5-digit US ZIP code."""
    return isinstance(zip_code, str) and zip_code.isdigit() and len(zip_code) == 5
