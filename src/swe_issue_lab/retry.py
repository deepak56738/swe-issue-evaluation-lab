"""Retry policy used by the delivery scheduling scenario."""


def calculate_retry_delay(
    attempt: int,
    *,
    base_seconds: float = 1.0,
    cap_seconds: float = 60.0,
) -> float:
    if isinstance(attempt, bool) or not isinstance(attempt, int):
        raise TypeError("attempt must be an integer")
    if attempt < 1:
        raise ValueError("attempt must be at least 1")
    if base_seconds <= 0:
        raise ValueError("base_seconds must be greater than zero")
    if cap_seconds < base_seconds:
        raise ValueError("cap_seconds must be at least base_seconds")

    delay = base_seconds * (2.0 ** (attempt - 1))
    return float(min(cap_seconds, delay))
