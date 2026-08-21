.PHONY: install test coverage lint typecheck evaluate check docker-build

install:
	uv sync --extra dev

test:
	uv run pytest

coverage:
	uv run pytest --cov --cov-report=term-missing

lint:
	uv run ruff check .

typecheck:
	uv run mypy src

evaluate:
	uv run evaluate-scenarios

check: lint typecheck coverage evaluate

docker-build:
	docker build --tag swe-issue-evaluation-lab:local .
