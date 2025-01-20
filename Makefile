SHELL := /bin/bash
BASE_DIR=.
ifeq ($(OS), Windows_NT)
VENV_ACTIVATOR='venv/Scripts/activate'
else
VENV_ACTIVATOR='venv/bin/activate'
endif


all: test flake8 build


# --- init project ---

venv:
	python3 -m venv venv

.PHONY: requirements
requirements: venv requirements.txt
	. $(VENV_ACTIVATOR); pip3 install -r requirements.txt

.PHONY: requirements_test
requirements_test: venv requirements_test.txt requirements
	. $(VENV_ACTIVATOR); pip3 install -r requirements_test.txt

.PHONY: requirements_deploy
requirements_deploy: venv requirements
	. $(VENV_ACTIVATOR); python3 -m pip install -U setuptools wheel build

.PHONY: requirements_all
requirements_all: requirements requirements_test requirements_deploy

# --- QA ---

.PHONY: test
test: requirements_test
	. $(VENV_ACTIVATOR); cd $(BASE_DIR); pytest -v -rs -n auto $(ARGS)

.PHONY: test1
test1: requirements_test
	# use test1 to run tests under single core
	. $(VENV_ACTIVATOR); cd $(BASE_DIR); pytest -v -rs $(ARGS)

.PHONY: flake8
flake8: requirements_test
	. $(VENV_ACTIVATOR); cd $(BASE_DIR); flake8 $(ARGS)

.PHONY: tox
tox: requirements_test
	. $(VENV_ACTIVATOR); cd $(BASE_DIR); tox

# --- run examples ---

.PHONY: run_examples
run_examples: requirements
	. $(VENV_ACTIVATOR); cd $(BASE_DIR)/usage_examples; python3 $(ARGS)

# --- build and push artifacts ---

.PHONY: build
build:
	. $(VENV_ACTIVATOR); python3 setup.py bdist_wheel sdist
