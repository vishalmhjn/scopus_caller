# SCOPUS Caller 

## Install the dependencies
`pip install requirements.txt`

## Add the API_KEY
Paste api_key from SCOPUS to input/API

## Using Keywords
Create a file keywords.csv. The file should have two columns "First term" and "Second term". Then run ``python scrapper.py location_of_keywords.csv`` 

## Unrestricted search
``python apiCaller.py SEARCH_TERMS`` 
e.g. ``python apiCaller.py transportation "road safety" "machine learning"``
- When a seacrh terms has a space ("machine learning"), use double quotations to enclose it (safety "machine learning")
