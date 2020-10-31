# Optional Makefile for easier development

VERSION = $(shell cat VERSION)

PYTHON = python
PIP = $(PYTHON) -m pip -v


build:
	$(PYTHON) setup.py build

install:
	$(PIP) install --no-index --upgrade .

check:
	ulimit -s 8192; $(PYTHON) -u tests/rundoctest.py
	ulimit -s 8192; $(PYTHON) tests/test_integers.py
	ulimit -s 8192; $(PYTHON) tests/test_backward.py

dist:
	chmod go+rX-w -R .
	umask 0022 && $(PYTHON) setup.py sdist --formats=gztar


.PHONY: build install check dist
