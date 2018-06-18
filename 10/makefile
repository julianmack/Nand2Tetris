.PHONY: help prepare-dev test lint run doc

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

.DEFAULT: help
help:
    @echo "make prepare-dev"
    @echo "       prepare development environment, use only once"
    @echo "make test"
    @echo "       run tests"
    @echo "make lint"
    @echo "       run pylint and mypy"
    @echo "make run"
    @echo "       run project"
    @echo "make doc"
    @echo "       build sphinx documentation"

prepare-dev:
    python3 -m pip install virtualenv
    make venv

# Requirements are in setup.py, so whenever setup.py is changed, re-run installation of dependencies.
venv: $(VENV_PATH)/bin/activate
$(VENV_NAME)/bin/activate: JackAnalyzer.py
    test -d $(VENV_PATH) || virtualenv -p python3 $(VENV_PATH)
    ${PYTHON} -m pip install -U pip
    ${PYTHON} -m pip install -e lxml
    touch $(VENV_PATH)/bin/activate


test: venv
    ${PYTHON} -m pytest

lint: venv
    ${PYTHON} -m pylint
    ${PYTHON} -m mypy

run: venv
    ${PYTHON} app.py

doc: venv
    $(VENV_ACTIVATE) && cd docs; make html
