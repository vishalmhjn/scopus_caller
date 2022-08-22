# SCOPUS Caller 

### SCOPUS API
SCOPUS API allows the users to query its database for all the articles based on a specified keyword(s). A user needs to create an account on SCOPUS using TUM ID and generate the SCOPUS key. The API specification can be seen at this link. Using this API, It is possible to retrieve title, authors, affiliation, DOI, etc of the scientific articles. Further, depending on the access level of the article and authorized API, the article's abstract-text can also be retrieved.
### Semantic Scholar API
Semantic Scholar also provides an API to retrieve the article's meta-data. It is possible to obtain abstracts by specifying the DOI of the article.
## Install the dependencies
```sh
pip install requirements.txt
```

## Add the API_KEY
Paste api_key from [SCOPUS](https://dev.elsevier.com) to input/API. Carefully read and understand the "API SERVICE AGREEMENT" and "Text and Data Mining (TDM) Provisions", before using the API and the retrieved data. These will be presented to the user while generating the API.

## Using Keywords
Create a file keywords.csv. The file should have two columns "First term" and "Second term". Then run the following
```sh
python keyword_scrapper.py location_of_keywords.csv
```

## Unrestricted search using CLI
``python call_scopus.py SEARCH_TERMS``. See the following example
```sh
python call_scopus.py transportation "road safety" "machine learning"
```

When a seacrh terms has a space ("machine learning"), use double quotations to enclose it (safety "machine learning")

For abstracts, you need to specify the output of previous step as input and then run the following
```sh
python call_semanticscholar.py path/to/acopus/results.csv output_filename
```


## Citing
This is based on the base script [Scopus-Query](https://github.com/nsanthanakrishnan/Scopus-Query), so kindly cite:
- Narayanan, S., & Antoniou, C. (2022). Electric cargo cycles - A comprehensive review. Transport Policy, 116 , 278–303. doi:10.1016/j.tranpol.2021.12.011.

Further, to see examples of how the keywords are used, kindly see and cite the supplementary material of the following publication:
- Vishal Mahajan, Nico Kuehnel, Aikaterini Intzevidou, Guido Cantelmo, Rolf Moeckel & Constantinos Antoniou (2022) Data to the people: a review of public and proprietary data for transport models, Transport Reviews, 42:4, 415-440, DOI: [10.1080/01441647.2021.1977414](https://www.tandfonline.com/doi/full/10.1080/01441647.2021.1977414?scroll=top&needAccess=true)
