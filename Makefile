.PHONY: environment clean lint

#################################################################################
# GLOBALS                                                                       #
#################################################################################
# Default
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = estates-web

# Python
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh; conda activate $(PROJECT_DIR)/.venv; conda activate $(PROJECT_DIR)/.venv


#################################################################################
# COMMANDS                                                                      #
#################################################################################
## Initiate python environment
environment:
	conda env create -f environment.yaml -p $(PROJECT_DIR)/.venv
	($(CONDA_ACTIVATE); poetry install)

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using pylint
lint:
	pylint src