BOWER :=bower
PIP :=pip3
PYTHON :=python3


.PHONY: default
default: install

.PHONY: install
install:
	$(PIP) install -r requirements.txt
	$(BOWER) install

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf static/bower_components/ .cache *.egg *.eggs *.egg-info build 2> /dev/null
	bower cache clean
