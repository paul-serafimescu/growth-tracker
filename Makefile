PYTHON := python3

SHELL := /bin/bash

MANAGE := $(PYTHON) manage.py

SUBDIR_ROOTS := . tests growth_tracker tracker authentication api
DIRS := . $(shell find $(SUBDIR_ROOTS) -type d)
GARBAGE_PATTERNS := __pycache__ db.sqlite3 migrations graphs
GARBAGE := $(foreach DIR,$(DIRS),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

NO_MIGRATIONS := No changes detected

MODEL_MODULES := tracker
MIGRATION_DIR := migrations

.PHONY := help bot migrations test

.DEFAULT_GOAL := help

help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project run 'make setup'"
	@echo "To test the project run 'make test'"
	@echo "To run the project run 'make run'"
	@echo "------------------------------------"

setup:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(MANAGE) test -v 2

run: migrations
	$(shell mkdir -p graphs)
	$(MANAGE) runserver

migrations:
	$(foreach MODULE,$(MODEL_MODULES),$(shell mkdir -p $(MODULE)/$(MIGRATION_DIR) && touch $(MODULE)/$(MIGRATION_DIR)/__init__.py))
	$(MANAGE) makemigrations && $(MANAGE) migrate

bot:
	$(PYTHON) -m bot

clean:
	rm -vrf $(GARBAGE)
