.PHONY: test
test: test-python
test-%:
	$* -m py.test ./ -svx
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .cache .eggs *.egg-info build
