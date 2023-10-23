
.default: help

.PHONY: help
help:
	@echo "usage:"
	@echo "dev | install-dev"
	@echo "   setup development environment"
	@echo ""
	@echo "install-orjson"
	@echo "   install orjson also"
	@echo ""
	@echo "test | run-all-tests"
	@echo "   run all tests"
	@echo ""
	@echo "run-all-tests-w-coverage"
	@echo "   run all tests with coverage collection"
	@echo ""
	@echo "lint"
	@echo "   lint the code"
	@echo ""
	@echo "type-check"
	@echo "   check types"
	@echo ""

PLATFORM := ${shell uname -o}

ifeq (${VIRTUAL_ENV},)
  VENV_NAME = .venv
  INVENV = rye run
else
  VENV_NAME = ${VIRTUAL_ENV}
  INVENV =
endif

${info Platform: ${PLATFORM}}
${info Using ${VENV_NAME}}

VENV_BIN = ${VENV_NAME}/bin


ifeq (${PLATFORM}, Android)
  FLAKE8_FLAGS = --jobs=1
else
  FLAKE8_FLAGS = --jobs=auto
endif

PYTHON = ${VENV_BIN}/python


dev: install-dev
install-dev:
	rye sync

install-ci:
	rye sync --features=ci

install-dev-orjson:
	rye sync --features=orjson,ci

default_cov := "--cov=src/json_streams"
cov_report := "term-missing"
cov := ${default_cov}

all_tests := tests
tests := tests

.PHONY: test
test: run-all-tests
.PHONY: run-all-tests
run-all-tests:
	${INVENV} pytest -vv ${tests}

.PHONY: test-w-coverage
test-w-coverage:
	${INVENV} pytest -vv ${cov} --cov-report=${cov_report} ${all_tests}

.PHONY: type-check
type-check:
	${INVENV} mypy --config-file mypy.ini src

.PHONY: lint
lint:
	${INVENV} ruff src tests

part := "patch"
bumpversion: install-dev
	${INVENV} bump2version ${part}

.PHONY: fmt
fmt:
	${INVENV} black src tests

.PHONY: fmt-check check-fmt
fmt-check: check-fmt
check-fmt:
	${INVENV} black --check src tests

.PHONY: tests/requirements.txt
tests/requirements.txt: pyproject.toml
	rye lock --features=orjson && cp requirements-dev.lock $@
