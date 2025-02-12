.PHONY: start test

start:
	PYTHONPATH=. uv run main.py

test:
	PYTHONPATH=. uv run python -m unittest discover tests
