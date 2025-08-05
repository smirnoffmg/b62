.PHONY: build_package test ci clean benchmark format lint install-dev

# Build the package in development mode
build_package:
	uv run maturin develop

# Run all tests
test: build_package
	uv run pytest -s -v

# Code quality checks
ci: build_package
	uv run ruff check --fix

# Format code
format:
	uv run ruff format .

# Lint code
lint:
	uv run ruff check .

# Install development dependencies
install-dev:
	uv sync

# Clean build artifacts
clean:
	rm -rf target/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build wheel for distribution (current platform)
build-wheel:
	uv run maturin build --release

# Build wheels for multiple platforms (for PyPI release)
build-wheels:
	uv run maturin build --release --target x86_64-unknown-linux-gnu
	uv run maturin build --release --target x86_64-apple-darwin
	uv run maturin build --release --target aarch64-apple-darwin
	uv run maturin build --release --target x86_64-pc-windows-msvc

# Build universal wheel (if possible)
build-universal:
	uv run maturin build --release --universal2

# Build for PyPI release (recommended for releases)
build-release:
	uv run maturin build --release --target x86_64-unknown-linux-gnu
	uv run maturin build --release --target x86_64-apple-darwin
	uv run maturin build --release --target aarch64-apple-darwin

# Build and install in development mode
dev: build_package

# Quick test (skip property-based tests)
test-quick: build_package
	uv run pytest tests/test_unit.py -s -v

# Run all checks (build, test, lint, type check)
check: build_package test ci