.DEFAULT_GOAL := check

CHECK_TASKS := lint build
BUILD_OUTPUTS := dist
CONTAINER_BUILD_ARGS := PYTHON_VERSION=$(shell cat .python-version)

override COMMAND := $(value COMMAND)
override TEST_ARGS := $(value TEST_ARGS)

export CHECK_TASKS BUILD_OUTPUTS CONTAINER_BUILD_ARGS TEST_ARGS COMMAND
export CHECK_TIMEOUT_SECONDS CHECK_SCRATCH_SIZE CHECK_WORK_SIZE CHECK_TMP_SIZE CHECK_NETWORK_LINT CONTAINER_IMAGE

.PHONY: check check-info lint test build exec

check lint test build exec:
	@./tests/container/run $@

check-info:
	@./tests/container/run info
