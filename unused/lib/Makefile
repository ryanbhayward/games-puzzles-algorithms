PIP :=pip3
PYTHON :=python3


.PHONY: default
default: install

.PHONY: test
test: setup.py
	$(PYTHON) setup.py -q test --addopts '-x $(ARGS)'

.PHONY: test-cov
test-cov: ARGS=--cov games_puzzles_algorithms --cov-report term:skip-covered
test-cov: test

.PHONY: install
install: requirements.txt
	$(PIP) install -r requirements.txt $(ARGS)

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find games_puzzles_algorithms -name "*.so" -delete
	rm -rf .cache *.egg .eggs *.egg-info build 2> /dev/null
