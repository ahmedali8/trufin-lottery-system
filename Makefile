.PHONY: start test

start:
	PYTHONPATH=. uv run main.py

test:
	PYTHONPATH=. uv run pytest
