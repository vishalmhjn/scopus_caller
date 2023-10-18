lint:
	pylint --disable=R,C scopus_caller/call_scopus.py
	pylint --disable=R,C scopus_caller/call_semanticscholar.py

format:
	black *.py

test:
	python tests/test_call_scopus.py