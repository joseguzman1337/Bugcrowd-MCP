.PHONY: install format format-check lint test test-integration clean

# ── Dependencies ────────────────────────────────────────────────────────────
install:
	pip install -r requirements.txt

# ── Formatting ──────────────────────────────────────────────────────────────
format:
	python -m black .

format-check:
	python -m black --check .

# ── Tests ────────────────────────────────────────────────────────────────────
test:
	pytest -m "not integration" -v

test-integration:
	pytest -m integration -v

# ── Clean ───────────────────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .mypy_cache dist build *.egg-info
