import pytest

from swe_issue_lab.retry import calculate_retry_delay


def test_delay_never_exceeds_cap() -> None:
    assert calculate_retry_delay(20, base_seconds=1, cap_seconds=30) == 30


def test_delay_increases_between_early_attempts() -> None:
    first = calculate_retry_delay(1)
    second = calculate_retry_delay(2)

    assert second > first


@pytest.mark.parametrize("attempt", [0, -1])
def test_rejects_attempt_below_one(attempt: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        calculate_retry_delay(attempt)


@pytest.mark.parametrize("attempt", [True, 1.5])
def test_rejects_non_integer_attempt(attempt: object) -> None:
    with pytest.raises(TypeError, match="integer"):
        calculate_retry_delay(attempt)  # type: ignore[arg-type]


def test_rejects_non_positive_base() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_retry_delay(1, base_seconds=0)


def test_rejects_cap_below_base() -> None:
    with pytest.raises(ValueError, match="at least base_seconds"):
        calculate_retry_delay(1, base_seconds=5, cap_seconds=4)
