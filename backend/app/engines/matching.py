from typing import Any


def build_match_key(values: dict[str, Any], field_codes: list[str]) -> str:
    return "|".join(str(values.get(code, "")).strip() for code in field_codes)
