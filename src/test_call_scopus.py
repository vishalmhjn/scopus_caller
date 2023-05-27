import os
from src.call_scopus import wrapper

API_KEY = os.environ['API_KEY']

def test_caller():
    YEAR = 2023
    KEYWORDS = ['predicting', 'flows', 'speeds', 'transfer learning', 'open data']
    articles_loaded = wrapper(API_KEY, KEYWORDS, YEAR) 
    assert articles_loaded.title[0] == "Predicting network flows from speeds using open data and transfer learning"

