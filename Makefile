CI ?= false
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))

SOURCE_DIR = src
TEST_DIR = tests
INFRA_DIR = infrastructure
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)

PROJECT_VERSION ?= $(shell poetry version -s)
PROJECT_NAME ?= $(shell poetry version | cut -d' ' -f1)
PYTHON_VERSION ?= $(shell cat .python-version)
GIT_COMMIT_HASH ?= $(shell git rev-parse HEAD)

DOCKER_URI_PREFIX ?=
DOCKER_TAGS ?= ${PROJECT_VERSION}

ifeq ($(CI), false)
	-include $(PWD)/.env
	export
endif

export PROJECT_VERSION
export PROJECT_NAME
export GIT_COMMIT_HASH

## Target convention naming:
## <Action>[-<Identifier>] :: Examples:
### `install` -> Just the action because is a generic task may implies other tasks.
### `install-poetry` -> The action first, the name after.
### `build-docker` -> Action and identifier.
### `rm-build-docker` -> Action taken for a action result.
## Why?
# Because helps to find the correct targets using the Shell AutoCompletion.

.PHONY: install install-poetry install-pre-commit
install: | install-poetry install-pre-commit

install-poetry:
	poetry install --no-root

install-pre-commit:
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg

.PHONY: build-docker
build-docker:
	docker build \
		$(foreach tag,$(DOCKER_TAGS),-t "$(DOCKER_URI_PREFIX)$(PROJECT_NAME):$(tag)") \
		--build-arg "PYTHON_VERSION=${PYTHON_VERSION}" \
		--build-arg "PROJECT_VERSION=${PROJECT_VERSION}.${GIT_COMMIT_HASH}" \
		--build-arg "PROJECT_NAME=${PROJECT_NAME}" \
		"${PWD}"

.PHONY: rm-build-docker
rm-build-docker:
	docker image rm -f $(foreach tag,$(DOCKER_TAGS),"$(DOCKER_URI_PREFIX)$(PROJECT_NAME):$(tag)")

.PHONY: push-docker
push-docker:
	docker push "$(DOCKER_URI_PREFIX)$(PROJECT_NAME)" --all-tags

.PHONY: clean
clean:
	find "${PWD}/" -name "__pycache__" -type d -exec rm -rfv {} +

prune-git-untracked-branches:
	git checkout main
	git fetch --prune
	branches_without_remote=$$(git branch -vv | awk '/: gone]/{print $$1}'); \
	if [ -n "$$branches_without_remote" ]; then \
		echo "Deleting the following branches:"; \
		for branch in $$branches_without_remote; do \
			git branch -D "$$branch"; \
		done; \
	else \
		echo "No untracked branches to delete."; \
	fi


.PHONY: test
test:
ifeq ($(CI),true)
	poetry run pytest --cov=$(SOURCE_DIR) --cov-report xml -s --capture=no $(TEST_DIR)
else
	poetry run pytest --cov=$(SOURCE_DIR) --cov-report=term-missing $(TEST_DIR)
endif

.PHONY: pre-commit lint
lint: pre-commit
pre-commit:
	poetry run pre-commit run --all-files

.PHONY: info
info:
	@echo "${PROJECT_NAME};${PROJECT_VERSION};${PYTHON_VERSION}"

.PHONY: info-name
info-name:
	@echo "${PROJECT_NAME}"

.PHONY: info-version
info-version:
	@echo "${PROJECT_VERSION}"

.PHONY: serve
serve:
	poetry run uvicorn --host=0.0.0.0 --port=8000 'src.app.instances.api:api' --reload

.PHONY: serve-prod
serve-prod:
	poetry run gunicorn -k uvicorn_worker.UvicornWorker -b :8000 'src.app.instances.api:api' -w 4 --threads 4 --preload
