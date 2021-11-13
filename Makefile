.PHONY: venv help test run-all-tests run-all-tests-w-coverage check-pylint check-mypy

.default: help

help:
	@echo "usage:"

PLATFORM := ${shell uname -o}
INVENV_PATH = ${shell which invenv}

ifeq (${VIRTUAL_ENV},)
  VENV_NAME = .venv
else
  VENV_NAME = ${VIRTUAL_ENV}
endif

${info Platform: ${PLATFORM}}
${info Using ${VENV_NAME}}
${info invenv: ${INVENV_PATH}}

VENV_BIN = ${VENV_NAME}/bin

ifeq (${INVENV_PATH},)
  INVENV = export VIRTUAL_ENV="${VENV_NAME}"; export PATH="${VENV_BIN}:${PATH}"; unset PYTHON_HOME;
else
  INVENV = invenv -C ${VENV_NAME}
endif

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
	poetry run pytest -vv tests

run-all-tests-w-coverage:
	poetry run pytest -vv --cov=json_streams  --cov-report=term-missing tests

check-mypy: install-dev
	poetry run mypy json_streams tests

check-pylint: install-dev
	poetry run  pylint --rcfile=.pylintrc json_streams tests

check-pylint-refactorings: install-dev
	poetry run pylint --disable=C,W,E --enable=R json_streams tests

bumpversion-major: install-dev
	poetry run bump2version major

bumpversion-minor: install-dev
	poetry run bump2version minor

bumpversion: install-dev
	poetry run bump2version patch
