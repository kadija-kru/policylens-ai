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
	uvicorn policylens.api.main:app --app-dir backend/src --reload
