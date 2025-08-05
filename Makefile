build_package:
	uv run maturin develop

test: build_package
	uv run pytest -s -v

ci:
	uv run ruff check --fix
	uv run mypy .