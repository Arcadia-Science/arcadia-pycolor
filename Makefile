include .env

.PHONY: lint
lint:
	ruff check --exit-zero .

.PHONY: format
format:
	ruff check --fix .
	ruff format .

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

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
		--repository pypi \
		--username __token__ \
		--password ${POETRY_PYPI_TOKEN_PYPI}
