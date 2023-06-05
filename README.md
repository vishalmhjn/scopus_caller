# SCOPUS Caller

> ℹ️ _Scopus quickly finds relevant and authoritative research, identifies experts and provides access to reliable data,
> metrics and analytical tools. Be confident in progressing research, teaching or research direction and priorities
> — all from one database and with one subscription._

## What is _SCOPUS API_

_SCOPUS API_ allows the users to query its database for all the articles based on a specified keyword(s).  
A user needs to create an account on [SCOPUS](https://www.elsevier.com/solutions/scopus) using your university or
personal account and generate the SCOPUS key.   
The API specification can be seen at this [link](https://github.com/ElsevierDev/elsapy). Using this API, It is possible
to **retrieve title**,**authors**, **affiliation**, **DOI**, etc of the scientific articles. Further, depending on the
access level of the article and authorized API, the article's **abstract-text** can also be retrieved.

### Semantic Scholar API

Semantic Scholar also provides an API to retrieve the article's meta-data. It is possible to obtain abstracts by
specifying the DOI of the article.

## Install the dependencies

1) Create a virtual environment to install all packages in and activate the environment:  
   *(Make sure you are in the parrent folder of this project)*

```sh
# crate an environment called venv in this project
python3 -m venv ./venv
# activate the environment
source ./venv/bin/activate
```

2) Now install all the neccessary requirements for this project:

```sh
pip install -r requirements.txt
```

## Add the API_KEY

1) create a new file for the api key:

```sh
touch input/API   
```

2) If you haven't created an account on [SCOPUS](https://dev.elsevier.com) yet, got to 
  [SCOPUS](https://www.elsevier.com/solutions/scopus) and create a private account or one via your university.
3) After being logged in, create a new API key [here](https://dev.elsevier.com/apikey/manage), name the label to your
   likings and leave the website input field empty *(it is not important)*.  
   Carefully read and understand the "API
   SERVICE AGREEMENT" and "Text and Data Mining (TDM) Provisions", before using the API and the retrieved data. These
   will be presented to the user while generating the API.
4) Paste your newly generated `api_key` to the created `API` file in the `input` folder _(input/API)_.


## Unrestricted search using CLI

First make sure you are in the `scopus_caller/src` folder then run:

```sh
python call_scopus.py [--year YEAR] [--api API_KEY] [SEARCH_TERMS]
```

**Parameters**:  
- `--year` (Optional):
  The upper bound of publication year for searching. If not specified, the current year will be used.
- `--api` (Optional):
  The API key to use. If not specified, the API key in the `input/API` file will be used.
- `SEARCH_TERMS`: The search terms to use.
  Separate multiple search terms with spaces.
  ❗ When a search term has a space (e.g., "machine learning"), use **double quotations** to enclose it (safety "machine learning")

**Example**:

The following command will search for articles with the search terms `transportation`, `road safety` and `machine learning` published before 2023 (inclusive). 

```sh
python call_scopus.py --year 2023 transportation "road safety" "machine learning"
```

## Abstracts
For abstracts, you need to specify the output of previous step as input and then run the following

```sh
python call_semanticscholar.py path/to/scopus/results.csv output_filename
```
The results of the query then land in the `scopus_caller/data` folder as csv files.

Abstracts for all SCOPUS database articles are not available from Semantic Scholar database.
## Using Keywords
Here we read a set of keywords from a dataframe with two columns and then search exhaustively using combinations of the words from the first column with the words from the second column. This helps reduce the manual effort in case you have many words to search with. Currently, it is hard coded with a dataframe with two columns, but it can be made flexible. Please open a PR if someone is interested in doing this.

In the `input/keywords.csv` add you two search terms and replace the placeholders.
First make sure you are in the `scopus_caller/src` folder then run:

```sh
python keyword_scrapper.py ../data/keywords.csv
```
The terms in each column should be unique keywords and need not be repeated. There can different number of keywords in each column. This code will iterate over column 1 (outer loop) and then iterate over column 2 (innner loop).

## Other settings

You can change the specifics of the search in call_scopus such as connecting string by `OR` or `AND`, etc.

## Citing

This is based on the base script [Scopus-Query](https://github.com/nsanthanakrishnan/Scopus-Query), so kindly cite:

- Narayanan, S., & Antoniou, C. (2022). Electric cargo cycles - A comprehensive review. Transport Policy, 116 , 278–303.
  doi:10.1016/j.tranpol.2021.12.011.

Further, to see examples of how the keywords are used, you may see the Supplementary information in the following publication:

- Vishal Mahajan, Nico Kuehnel, Aikaterini Intzevidou, Guido Cantelmo, Rolf Moeckel & Constantinos Antoniou (2022) Data
  to the people: a review of public and proprietary data for transport models, Transport Reviews, 42:4, 415-440,
  DOI: [10.1080/01441647.2021.1977414](https://www.tandfonline.com/doi/full/10.1080/01441647.2021.1977414?scroll=top&needAccess=true)

## License

Distributed under the MIT License.

