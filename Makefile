
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
  INVENV = poetry run
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
	poetry install

install-orjson:
	poetry install --extras orjson

upgrade-pip: venv
	${INVENV} pip install --upgrade pip

.PHONY: test
test: run-all-tests
.PHONY: run-all-tests
run-all-tests:
	${INVENV} pytest -vv tests

.PHONY: run-all-tests-w-coverage
run-all-tests-w-coverage:
	${INVENV} pytest -vv --cov=json_streams  --cov-report=xml tests

.PHONY: type-check
type-check:
	${INVENV} mypy json_streams

.PHONY: lint
lint:
	${INVENV}  pylint --rcfile=.pylintrc json_streams tests

.PHONY: lint-refactorings
lint-refactorings:
	${INVENV} pylint --disable=C,W,E --enable=R json_streams tests

bumpversion-major: install-dev
	${INVENV} bump2version major

bumpversion-minor: install-dev
	${INVENV} bump2version minor

bumpversion: install-dev
	${INVENV} bump2version patch
