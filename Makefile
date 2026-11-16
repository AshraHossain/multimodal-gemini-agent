.PHONY: setup dev test lint eval check docker-build

setup:
	uv sync

dev:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check .

test:
	uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=80

eval:
	uv run python -m app.eval

check: lint test eval

docker-build:
	docker build -t multimodal-gemini-agent:latest .
