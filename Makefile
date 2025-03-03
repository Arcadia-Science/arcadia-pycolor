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
		poetry run jupyter execute --inplace $$file; \
	done

.PHONY: lint
lint:
	ruff check --exit-zero .
	ruff format --check .

.PHONY: format
format:
	ruff check --fix .
	ruff format .

.PHONY: typecheck
typecheck:
	pyright --project pyproject.toml .

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -v .

.PHONY: clean
clean:
	rm -rf dist

.PHONY: build
build: clean
	poetry build

# Note: `poetry` does not appear to read the `POETRY_PYPI_TOKEN_<NAME>` environment variable,
# so we need to pass it explicitly in these `publish` commands.
.PHONY: build-and-test-publish
build-and-test-publish: build
	poetry publish \
		--repository pypi_test \
		--username __token__ \
		--password ${POETRY_PYPI_TOKEN_PYPI_TEST}

.PHONY: build-and-publish
build-and-publish: build
	poetry publish \
		--username __token__ \
		--password ${POETRY_PYPI_TOKEN_PYPI}
