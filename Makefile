PYTHON ?= python

.PHONY: install lint test run

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check .

test:
	pytest

run:
	uvicorn policylens.api.main:app --app-dir backend/src --reload --host $${POLICYLENS_API_HOST:-127.0.0.1} --port $${POLICYLENS_API_PORT:-8000}
