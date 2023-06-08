
lint-mypy:
	mypy --install-types --non-interactive storekit

TEST_DIR ?= tests
test:
	pytest --cov -s $(TEST_DIR)
