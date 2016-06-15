PIP :=pip3
PYTHON :=python3


.PHONY: default
default: install

.PHONY: test
test: $(PYTHON) setup.py
	$(PYTHON) setup.py -q test --addopts '-x $(ARGS)'

.PHONY: install
install: $(PIP) requirements.txt
	$(PIP) install -r requirements.txt

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .cache *.egg *.eggs *.egg-info build 2> /dev/null
