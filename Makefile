include .env

.PHONY: lint
lint:
	ruff check --exit-zero .

.PHONY: format
format:
	ruff --fix .
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
