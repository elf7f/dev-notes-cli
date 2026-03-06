PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin
RUN := PYTHONPATH=. $(BIN)/python -m devnotes.cli

.PHONY: help venv install templates smoke clean

help:
	@echo "Targets:"
	@echo "  make venv      - create virtual environment"
	@echo "  make install   - install project only (minimal download)"
	@echo "  make templates - list built-in templates"
	@echo "  make smoke     - run init/new/doctor end-to-end check"
	@echo "  make clean     - remove generated smoke workspace"

venv:
	$(PYTHON) -m venv $(VENV)

install:
	PYTHONDONTWRITEBYTECODE=1 $(BIN)/pip install .

templates:
	$(RUN) list-templates

smoke:
	rm -rf .smoke
	mkdir -p .smoke
	cd .smoke && PYTHONPATH=.. ../$(BIN)/python -m devnotes.cli init
	cd .smoke && PYTHONPATH=.. ../$(BIN)/python -m devnotes.cli new "Redis缓存设计" --tags redis,system --category 项目实践 --template project --summary "缓存分层方案总结"
	cd .smoke && PYTHONPATH=.. ../$(BIN)/python -m devnotes.cli doctor

clean:
	rm -rf .smoke
