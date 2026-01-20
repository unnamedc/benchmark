import re


def validate_url(url: str) -> bool:
    pattern = r'^https?://[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(pattern, url.strip()))


def validate_count(count: str) -> int:
    try:
        value = int(count)
        if value <= 0:
            raise ValueError("Count must be positive")
        return value
    except ValueError as e:
        raise ValueError(f"Invalid count value: {e}")