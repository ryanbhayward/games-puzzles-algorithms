.PHONY: default
default: install test

.PHONY: test
test: PYTHON :=python3
test: setup.py
	$(PYTHON) setup.py -q test --addopts '-x $(ARGS)'

.PHONY: install
install: PIP :=pip3
install: requirements.txt
	$(PIP) install -r requirements.txt

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .cache *.egg *.eggs *.egg-info build 2> /dev/null
