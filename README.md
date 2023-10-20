# SCOPUS Caller

[![linux](https://github.com/vishalmhjn/scopus_caller/actions/workflows/main.yml/badge.svg?branch=master&event=push)](https://github.com/vishalmhjn/scopus_caller/actions/workflows/main.yml)
[![mac](https://github.com/vishalmhjn/scopus_caller/actions/workflows/mac.yml/badge.svg?branch=master&event=push)](https://github.com/vishalmhjn/scopus_caller/actions/workflows/mac.yml)
[![windows](https://github.com/vishalmhjn/scopus_caller/actions/workflows/windows.yml/badge.svg?branch=master&event=push)](https://github.com/vishalmhjn/scopus_caller/actions/workflows/windows.yml)

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
specifying the DOI of the article. Abstracts for all SCOPUS database articles are not available from Semantic Scholar database.

## Installation

1. Create a virtual environment to install all packages in and activate the environment:  
   _(Make sure you are in the parent folder of this project)_

   ```sh
   # create an environment called scopuscaller in this project
   python3 -m venv ~/.scopuscaller
   # activate the environment
   source ~/.scopuscaller/bin/activate
   ```

2. Install the package

   ```sh
   pip install scopus-caller
   ```

## Obtain the API Key

1. If you haven't created an account on [SCOPUS](https://dev.elsevier.com) yet, got to
   [SCOPUS](https://www.elsevier.com/solutions/scopus) and create a private account or one via your university.
2. After being logged in, create a new API key [here](https://dev.elsevier.com/apikey/manage), name the label to your
   likings and leave the website input field empty _(it is not important)_.  
   Carefully read and understand the "API
   SERVICE AGREEMENT" and "Text and Data Mining (TDM) Provisions", before using the API and the retrieved data. These
   will be presented to the user while generating the API.
3. Copy you API key and store it in a text file.

## Usage

Import the library and paste the API key. Then run the following code in **Python3** terminal or Jupyter notebook.

```sh
# import the module
import scopuscaller as sc

# paste the api here
api_key = ""
```

**Parameters of function get*titles.py***:

Parameters:

- api_key (str): Your Elsevier API key for authentication.
- keywords (list of str): Keywords to search for in article titles and abstracts.
- year (int, optional): The cut-off year, upto which articles which be retrieved. Default is 2023.

**Example**:

The following command will search for articles with the search terms `transportation`, `road safety` and `transfer learning` published before 2023 (inclusive).

```sh
# Obtain the articles
df = sc.get_titles(api_key, ["transportation", "road safety", "transfer learning"], 2023)

# Obtain the abstracts of the above articles. For abstracts, you need to specify the output of previous step as input and then run the following

df = sc.get_abstracts(df)
```

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
