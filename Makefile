run_tests:
	python3 -m unittest discover . -b

generate_coverage:
	coverage run -m unittest discover .
	coverage report -m ./*/*.py ./*.py 

generate_coverage_html:
	coverage run -m unittest discover .
	coverage html ./*/*.py ./*.py

clean:
	rm -rf .coverage htmlcov