.PHONY: lint
lint:
	ruff --exit-zero check .

.PHONY: format
format:
	ruff --fix .
	ruff format .

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files
