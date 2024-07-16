test:
	poetry run pytest -v tests

coverage:
	poetry run coverage run -m pytest -v tests && \
	poetry run coverage report

coverage_dump_html:
	poetry run coverage run -m pytest --junitxml=reports/junit/junit.html tests && \
	poetry run coverage html -d reports/coverage/htmlcov

coverage_dump_xml:
	poetry run coverage run -m pytest --junitxml=reports/junit/junit.xml tests && \
	poetry run coverage xml -o reports/coverage/coverage.xml

generate_badges:
	poetry run genbadge coverage -o badges/coverage.svg ; \
	poetry run genbadge tests -o badges/tests.svg

coverage_dump_and_badge:
	make coverage_dump_xml && make generate_badges