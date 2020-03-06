## How to use:
- Place the API key in /input/API
- Create a keywords.csv and save the keywords in two column format with "First term" and "Second term" as the two columns.
- Run scrapper.py to Query Scopus using API and Keywords.csv. This also saves the hrefs. 
- Run apiCaller.py to get the results with unrestricted keywords i.e., using as many terms as possible. python apiCaller.py mobility "machine learning" "random forest"
- The data is saved in /data folder

