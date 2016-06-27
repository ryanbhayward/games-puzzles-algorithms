.PHONY: default
default: venv install

VENV_DIR :=$(shell pwd)/.venv
SYS_PYTHON :=python3

VENV_ACTIVATE =$(VENV_DIR)/bin/activate
$(VENV_ACTIVATE):
	virtualenv -p $(SYS_PYTHON) $(VENV_DIR)

VENV_PYTHON =$(VENV_DIR)/bin/python
$(VENV_PYTHON): $(VENV_ACTIVATE)

VENV_PIP =$(VENV_DIR)/bin/pip
$(VENV_PIP): $(VENV_ACTIVATE)

PYTHON :=$(VENV_PYTHON)
PIP :=$(VENV_PIP)

.PHONY: venv
venv: $(VENV_ACTIVATE)

.PHONY: test
test: lib/Makefile
	cd lib && make test PYTHON=$(PYTHON) ARGS=$(ARGS)

.PHONY: install
install: lib/Makefile
	cd lib && make install PIP=$(PIP)

clean:
	rm -rf $(VENV_DIR) 2> /dev/null
	cd lib && make clean
