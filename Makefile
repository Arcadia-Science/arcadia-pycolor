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

.PHONY: test-publish
test-publish: clean
	poetry --build publish --repository testpypi

.PHONY: publish
publish: clean
	poetry --build publish --repository pypi
