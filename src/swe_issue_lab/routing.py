"""Exact and wildcard webhook event routing."""


class RouteNotFoundError(LookupError):
    pass


class EventRouter:
    def __init__(self) -> None:
        self._routes: dict[str, str] = {}

    def add(self, pattern: str, target: str) -> None:
        normalized_pattern = pattern.strip().lower()
        normalized_target = target.strip()
        if not normalized_pattern:
            raise ValueError("pattern must not be empty")
        if not normalized_target:
            raise ValueError("target must not be empty")
        if "*" in normalized_pattern and not normalized_pattern.endswith(".*"):
            raise ValueError("wildcards are only supported as a trailing '.*'")
        self._routes[normalized_pattern] = normalized_target

    def resolve(self, event_type: str) -> str:
        normalized_event = event_type.strip().lower()
        if not normalized_event:
            raise ValueError("event_type must not be empty")

        exact = self._routes.get(normalized_event)
        if exact is not None:
            return exact

        wildcard_routes = sorted(
            (
                (pattern, target)
                for pattern, target in self._routes.items()
                if pattern.endswith(".*")
            ),
            key=lambda route: len(route[0]),
            reverse=True,
        )
        for pattern, target in wildcard_routes:
            prefix = pattern.removesuffix("*")
            if normalized_event.startswith(prefix):
                return target

        raise RouteNotFoundError(f"no route configured for '{normalized_event}'")
