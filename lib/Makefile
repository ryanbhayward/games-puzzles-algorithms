.PHONY: test
test: test-python
test-%:
	$* setup.py -q test --addopts '-x $(ARGS)'

.PHONY: install
install: install-pip
install-%:
	$* install -r requirements.txt

.PHONY: dev-install
dev-install: dev-install-python-pip
dev-install-%:
	$(eval TOOLS = $(subst -, ,$*))
	$(eval INTERPRETER = $(word 1, $(TOOLS)))
	$(eval INSTALLER = $(word 2, $(TOOLS)))
	$(MAKE) install-$(INSTALLER)
	$(INTERPRETER) setup.py test

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .cache .eggs *.egg-info build
