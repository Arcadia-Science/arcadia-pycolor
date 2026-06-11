DOCS_DIR := ./docs
JUPYTER_NOTEBOOKS := $(shell find $(DOCS_DIR) -type f -name '*.ipynb')

# Load environment variables from the `.env` file if it exists.
ifneq (,$(wildcard .env))
    include .env
endif

.PHONY: execute-all-notebooks
execute-all-notebooks:
	@if [ -n "$$CI" ]; then set -e; fi; \
	for file in $(JUPYTER_NOTEBOOKS); do \
		echo "Executing notebook $$file"; \
		uv run jupyter execute --inplace $$file; \
	done

.PHONY: lint
lint:
	uv run ruff check --exit-zero .
	uv run ruff format --check .

.PHONY: format
format:
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: typecheck
typecheck:
	uv run pyright --project pyproject.toml .

.PHONY: pre-commit
pre-commit:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest -v .

.PHONY: clean
clean:
	rm -rf dist

.PHONY: build
build: clean
	uv build

.PHONY: build-and-test-publish
build-and-test-publish: build
	uv publish \
		--publish-url https://test.pypi.org/legacy/ \
		--token ${UV_PUBLISH_TOKEN_PYPI_TEST}

.PHONY: build-and-publish
build-and-publish: build
	uv publish \
		--token ${UV_PUBLISH_TOKEN_PYPI}

.PHONY: preview-docs
preview-docs:
	uv run mkdocs serve