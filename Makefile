
# use this Makefile as base in your project by running
# git remote add make https://github.com/spraakbanken/python-pdm-make-conf
# git fetch make
# git merge --allow-unrelated-histories make/main
#
# To later update this makefile:
# git fetch make
# git merge make/main
#
.default: help

.PHONY: help
help:
	@echo "usage:"
	@echo "dev | install-dev"
	@echo "   setup development environment"
	@echo "install"
	@echo "   setup production environment"
	@echo ""
	@echo "info"
	@echo "   print info about the system and project"
	@echo ""
	@echo "test"
	@echo "   run all tests"
	@echo ""
	@echo "test-w-coverage [cov=] [cov_report=]"
	@echo "   run all tests with coverage collection. (Default: cov_report='term-missing', cov='--cov=${PROJECT_SRC}')"
	@echo ""
	@echo "lint"
	@echo "   lint the code"
	@echo ""
	@echo "lint-fix"
	@echo "   lint the code and try to fix it"
	@echo ""
	@echo "type-check"
	@echo "   check types"
	@echo ""
	@echo "fmt"
	@echo "   format the code"
	@echo ""
	@echo "check-fmt"
	@echo "   check that the code is formatted"
	@echo ""
	@echo "bumpversion [part=]"
	@echo "   bumps the given part of the version of the project. (Default: part='patch')"
	@echo ""
	@echo "bumpversion-show"
	@echo "   shows the bump path that is possible"
	@echo ""
	@echo "publish [branch=]"
	@echo "   pushes the given branch including tags to origin, for CI to publish based on tags. (Default: branch='main')"
	@echo "   Typically used after `make bumpversion`"
	@echo ""
	@echo "prepare-release"
	@echo "   run tasks to prepare a release"
	@echo ""

PLATFORM := `uname -o`
REPO := "json_arrays"
PROJECT_SRC := "src/json_arrays"

ifeq (${VIRTUAL_ENV},)
  VENV_NAME = .venv
  INVENV = pdm run
else
  VENV_NAME = ${VIRTUAL_ENV}
  INVENV =
endif

default_cov := "--cov=${PROJECT_SRC}"
cov_report := "term-missing"
cov := ${default_cov}

all_tests := tests
tests := tests

info:
	@echo "Platform: ${PLATFORM}"
	@echo "INVENV: '${INVENV}'"

dev: install-dev

# setup development environment
install-dev:
	pdm sync --dev --clean

pdm.dev.orjson.lock: pyproject.toml
	pdm lock --dev --group orjson --lockfile $@

.PHONY: install-dev-orjson
install-dev-orjson: pdm.dev.orjson.lock
	pdm install --lockfile $<

# setup production environment
install:
	pdm sync --prod

.PHONY: test
test:
	${INVENV} pytest -vv ${tests}

.PHONY: test-w-coverage
# run all tests with coverage collection
test-w-coverage:
	${INVENV} pytest -vv ${cov}  --cov-report=${cov_report} ${all_tests}

.PHONY: doc-tests
doc-tests:
	${INVENV} pytest ${cov} --cov-report=${cov_report} --doctest-modules ${PROJECT_SRC}

.PHONY: type-check
# check types
type-check:
	${INVENV} mypy ${PROJECT_SRC} ${tests}

.PHONY: lint
# lint the code
lint:
	${INVENV} ruff check ${PROJECT_SRC} ${tests}

.PHONY: lint-fix
# lint the code (and fix if possible)
lint-fix:
	${INVENV} ruff check --fix ${PROJECT_SRC} ${tests}

part := "patch"
bumpversion:
	${INVENV} bump-my-version bump ${part}

bumpversion-show:
	${INVENV} bump-my-version show-bump

# run formatter(s)
fmt:
	${INVENV} ruff format ${PROJECT_SRC} ${tests}

.PHONY: check-fmt
# check formatting
check-fmt:
	${INVENV} ruff format --check ${PROJECT_SRC} ${tests}

build:
	pdm build

branch := "main"
publish:
	git push -u origin ${branch} --tags


.PHONY: prepare-release
prepare-release: tests/requirements-testing.lock CHANGELOG.md

# we use lock extension so that dependabot doesn't pick up changes in this file
tests/requirements-testing.lock: pyproject.toml
	pdm export --dev --format requirements --output $@

.PHONY: CHANGELOG.md
CHANGELOG.md:
	git cliff --unreleased --prepend $@

.PHONY: snapshot-update
snapshot-update:
	${INVENV} pytest --snapshot-update