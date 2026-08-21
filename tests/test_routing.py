import pytest

from swe_issue_lab.routing import EventRouter, RouteNotFoundError


def test_exact_route_wins_over_wildcard() -> None:
    router = EventRouter()
    router.add("orders.*", "general-order-handler")
    router.add("orders.created", "new-order-handler")

    assert router.resolve(" ORDERS.CREATED ") == "new-order-handler"


def test_wildcard_routes_nested_event() -> None:
    router = EventRouter()
    router.add("orders.*", "order-handler")

    assert router.resolve("orders.shipment.created") == "order-handler"


def test_longest_wildcard_prefix_wins() -> None:
    router = EventRouter()
    router.add("orders.*", "order-handler")
    router.add("orders.shipment.*", "shipment-handler")

    assert router.resolve("orders.shipment.created") == "shipment-handler"


def test_unknown_event_raises_clear_error() -> None:
    router = EventRouter()
    router.add("orders.*", "order-handler")

    with pytest.raises(RouteNotFoundError, match=r"payments\.created"):
        router.resolve("payments.created")


@pytest.mark.parametrize(
    "event_type",
    ["orders", "orderly.created", "orders_archive.created", "orders-v2.created"],
)
def test_wildcard_respects_event_namespace_boundary(event_type: str) -> None:
    router = EventRouter()
    router.add("orders.*", "order-handler")

    with pytest.raises(RouteNotFoundError):
        router.resolve(event_type)


@pytest.mark.parametrize(
    ("pattern", "target", "message"),
    [
        ("", "handler", "pattern"),
        ("orders.*", "", "target"),
        ("orders.*.created", "handler", "trailing"),
    ],
)
def test_rejects_invalid_route_configuration(
    pattern: str,
    target: str,
    message: str,
) -> None:
    router = EventRouter()

    with pytest.raises(ValueError, match=message):
        router.add(pattern, target)


def test_rejects_blank_event_type() -> None:
    with pytest.raises(ValueError, match="event_type"):
        EventRouter().resolve("  ")
