# Run all unit tests
run_tests:
	python3 -m unittest discover . -b

# Generate coverage report in terminal
generate_coverage:
	coverage run -m unittest discover . -b
	coverage report -m ./*/*.py ./*.py 

# Generate coverage report in html format
generate_coverage_html:
	coverage run -m unittest discover . -b
	coverage html ./*/*.py ./*.py

# Clean coverage reports
clean:
	rm -rf .coverage htmlcov

# Show this message help
help:
	@cat $(MAKEFILE_LIST) | docker run --rm -i xanders/make-help