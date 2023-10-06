# Optional Makefile for easier development

VERSION = $(shell cat VERSION)

PYTHON = python
PIP = $(PYTHON) -m pip -v


install:
	$(PIP) install --upgrade .

check:
	ulimit -s 8192; $(PYTHON) -u tests/rundoctest.py
	ulimit -s 8192; $(PYTHON) tests/test_integers.py
	ulimit -s 8192; $(PYTHON) tests/test_backward.py

dist:
	chmod go+rX-w -R .
	$(PIP) install build
	umask 0022 && $(PYTHON) -m build --sdist


.PHONY: install check dist
