install:
	pip install -r requirements.txt

lint:
	pylint --disable=R,C scopuscaller/call_scopus.py

format:
	black *.py

test:	python scopuscaller/test_call_scopus.py