import re

def parse_price(text: str):
    if not text:
        return None
    # Extracts numbers including decimals, ignoring ILS or $ symbols
    match = re.search(r"([\d,.]+)", text)
    if not match:
        return None
    try:
        # Remove commas for conversion
        return float(match.group(1).replace(",", ""))
    except ValueError:
        return None