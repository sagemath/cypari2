# Optional Makefile for easier development

VERSION = $(shell cat VERSION)

PYTHON = python
PIP = $(PYTHON) -m pip -v


build:
	$(PYTHON) setup.py build

install:
	$(PIP) install --no-index --ignore-installed .

dist:
	chmod go+rX-w -R .
	umask 0022 && $(PYTHON) setup.py sdist --formats=gztar


.PHONY: build install dist
