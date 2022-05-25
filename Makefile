.PHONY: venv help test run-all-tests run-all-tests-w-coverage check-pylint check-mypy

.default: help

help:
	@echo "usage:"

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

test: run-all-tests
run-all-tests:
	${INVENV} pytest -vv tests

run-all-tests-w-coverage:
	${INVENV} pytest -vv --cov=json_streams  --cov-report=xml tests

check-mypy: install-dev
	${INVENV} mypy json_streams tests

check-pylint: install-dev
	${INVENV}  pylint --rcfile=.pylintrc json_streams tests

check-pylint-refactorings: install-dev
	${INVENV} pylint --disable=C,W,E --enable=R json_streams tests

bumpversion-major: install-dev
	${INVENV} bump2version major

bumpversion-minor: install-dev
	${INVENV} bump2version minor

bumpversion: install-dev
	${INVENV} bump2version patch
