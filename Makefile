.ONESHELL:

.DEFAULT_GOAL := venv

PYTHON = ./venv/bin/python
PIP = ./venv/bin/pip

venv/bin/activate:
	@/usr/local/bin/python3.11 -m venv venv
	@. ./venv/bin/activate
	@$(PIP) install -U pip

venv: venv/bin/activate requirements.txt
	@$(PIP) install -qr requirements.txt

task001: venv .env
	@${PYTHON} task_001_helloapi.py
