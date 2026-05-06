
# use this Makefile as base in your project by running
# git remote add make https://github.com/spraakbanken/python-uv-make-conf
# git fetch make
# git merge --allow-unrelated-histories make/main
#
# To later update this makefile:
# git fetch make
# git merge make/main
#
.default: help

.PHONY: help
# Taken from https://github.com/lightpanda/browser
## display this help screen
help:
	@printf "\033[36m%-35s %s\033[0m\n" "Command" "Usage"
	@sed -n -e '/^## /{'\
		-e 's/## //g;'\
		-e 'h;'\
		-e 'n;'\
		-e 's/:.*//g;'\
		-e 'G;'\
		-e 's/\n/ /g;'\
		-e 'p;}' Makefile | awk '{printf "\033[33m%-35s\033[0m%s\n", $$1, substr($$0,length($$1)+1)}'


PLATFORM := `uname -o`
PROJECT_SRC := src

ifeq (${VIRTUAL_ENV},)
  VENV_NAME = .venv
  INVENV = uv run
else
  VENV_NAME = ${VIRTUAL_ENV}
  INVENV =
endif


default_cov := "--cov=${PROJECT_SRC}"
cov_report := "term-missing"
cov := ${default_cov}

all_tests := tests
tests := tests

## print info about the system and project
info:
	@echo "Platform: ${PLATFORM}"
	@echo "INVENV: '${INVENV}'"

dev: install-dev-orjson

## setup development environment
install-dev: install-pre-commit
	uv sync --all-packages --dev

## install pre-commit hooks
install-pre-commit: .git/hooks/pre-commit
.git/hooks/pre-commit: .pre-commit-config.yaml
	if command -v prek > /dev/null; then prek install -f; else if command -v pre-commit > /dev/null; then pre-commit install; else echo "WARN: neither 'prek' nor 'pre-commit' is installed"; fi; fi

## setup production environment
install:
	uv sync --all-packages --no-dev --frozen

lock: uv.lock

uv.lock: pyproject.toml
	uv lock

.PHONY: test
## run all tests
test:
	${INVENV} pytest -vv ${tests}

.PHONY: test-w-coverage
## run all tests with coverage collection
test-w-coverage:
	${INVENV} pytest -vv ${cov} --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=lcov:coverage.lcov ${all_tests}

.PHONY: doc-tests
## run doc-tests
doc-tests:
	${INVENV} pytest ${cov} --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=lcov:coverage.lcov --doctest-modules ${PROJECT_SRC}

.PHONY: type-check
## check types
type-check:
	${INVENV} ty check ${PROJECT_SRC} ${tests}

.PHONY: lint
## lint the code
lint:
	${INVENV} ruff check ${PROJECT_SRC} ${tests}

.PHONY: lint-fix
## lint the code (and fix if possible)
lint-fix:
	${INVENV} ruff check --fix ${PROJECT_SRC} ${tests}

part := "patch"
## bump the given version of the version. (Default: part="patch") Override with 'make bumpversion part=minor'
bumpversion:
	${INVENV} bump-my-version bump ${part}

## show the next versions depending on part
bumpversion-show:
	${INVENV} bump-my-version show-bump

## run formatter(s)
fmt:
	${INVENV} ruff format ${PROJECT_SRC} ${tests}

.PHONY: check-fmt
## check formatting
check-fmt:
	${INVENV} ruff format --check ${PROJECT_SRC} ${tests}

## build distribution
build:
	uv build

branch := "main"
## pushes the given branch including tags to origin, for CI to publish based on tags. (Default: branch=main)
publish:
	git push -u origin ${branch} --tags


.PHONY: prepare-release
## prepare release: update changelog from git history, curate CHANGELOG.md manually and commit
prepare-release: update-changelog tests/requirements-testing.lock

# we use lock extension so that dependabot doesn't pick up changes in this file
tests/requirements-testing.lock: pyproject.toml
	uv export --dev --format requirements-txt --no-hashes --no-emit-project --output-file $@

.PHONY: update-changelog
## update changelog from git history
update-changelog: CHANGELOG.md

.PHONY: CHANGELOG.md
CHANGELOG.md:
	git cliff --unreleased --prepend $@

.PHONY: snapshot-update
## update snapshots for `syrupy`
snapshot-update:
	${INVENV} pytest --snapshot-update

### === project targets below this line ===
# setup development environment (with orjson)
install-dev-orjson: install-pre-commit
	uv sync --dev --extra orjson

run-benchmarks:
	${INVENV} pytest --benchmark-only benchmarks
