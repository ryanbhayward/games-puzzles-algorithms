.PHONY: default
default: venv install test

VENV_DIR =.venv

VENV_ACTIVATE =$(VENV_DIR)/bin/activate
$(VENV_ACTIVATE):
	virtualenv -p python3 $(VENV_DIR)

VENV_PYTHON =$(VENV_DIR)/bin/python
$(VENV_PYTHON): $(VENV_ACTIVATE)

VENV_PIP =$(VENV_DIR)/bin/pip
$(VENV_PIP): $(VENV_ACTIVATE)

.PHONY: venv
venv: $(VENV_ACTIVATE)

.PHONY: test
test: PYTHON :=../$(VENV_PYTHON)
test: lib/Makefile
	cd lib && make test PYTHON=$(PYTHON) ARGS=$(ARGS)

.PHONY: install
install: PIP :=../$(VENV_PIP)
install: lib/Makefile
	cd lib && make install PIP=$(PIP)

clean:
	rm -rf $(VENV_DIR) 2> /dev/null
	cd lib && make clean
