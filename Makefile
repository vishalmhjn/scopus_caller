install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C scopuscaller/call_scopus.py

format:
	black *.py

test:
	python tests/test_call_scopus.py