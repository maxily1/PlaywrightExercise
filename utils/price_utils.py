import re

def parse_price(text: str):
    if not text:
        return None

    match = re.search(r"([\d,.]+)", text)
    if not match:
        return None

    return float(match.group(1).replace(",", ""))
