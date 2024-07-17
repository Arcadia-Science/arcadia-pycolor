include .env

DOCS_DIR := ./docs
JUPYTER_NOTEBOOKS := $(shell find $(DOCS_DIR) -type f -name '*.ipynb')

.PHONY: execute-all-notebooks
execute-all-notebooks:
	@for file in $(JUPYTER_NOTEBOOKS); do \
		echo "Executing notebook $$file"; \
		jupyter execute --inplace $$file; \
	done

.PHONY: lint
lint:
	ruff check --exit-zero .
	ruff format --check .
	pyright --project pyproject.toml .

.PHONY: format
format:
	ruff check --fix .
	ruff format .

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
# so we need to pass it explicitly in the `publish` command.
.PHONY: test-publish
test-publish: build
	poetry publish \
		--repository pypi_test \
		--username __token__ \
		--password ${POETRY_PYPI_TOKEN_PYPI_TEST}

.PHONY: publish
publish: build
	poetry publish \
		--username __token__ \
		--password ${POETRY_PYPI_TOKEN_PYPI}
