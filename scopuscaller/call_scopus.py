# MIT License
# Copyright (c) 2021 Santhanakrishnan Narayanan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pandas as pd
import requests


def create_article_dataframe(allentries):
    "create data frame from the extracted JSON from API response"
    articles = pd.DataFrame(
        columns=["title", "creator", "publisher", "date", "doi", "citations"]
    )
    publicationTitle = []
    publicationAuthor = []
    publicationName = []
    publicationDate = []
    publicationDoi = []
    publicationCitations = []

    for entry in allentries:
        if "dc:title" in entry:
            title = entry["dc:title"]
            publicationTitle.append(title)
        else:
            print(entry)
            continue

        if "dc:creator" in entry:
            author = entry["dc:creator"]
            publicationAuthor.append(author)
        else:
            author = "No author"
            publicationAuthor.append(author)

        if "prism:publicationName" in entry:
            name = entry["prism:publicationName"]
            publicationName.append(name)
        else:
            name = "No publication name"
            publicationName.append(name)

        date = entry["prism:coverDate"]
        publicationDate.append(date)

        if "prism:doi" in entry:
            doi = entry["prism:doi"]
            publicationDoi.append(doi)
        else:
            doi = "No Doi"
            publicationDoi.append(doi)

        if "citedby-count" in entry:
            citations = entry["citedby-count"]
            publicationCitations.append(citations)
        else:
            citations = "No data"
            publicationCitations.append(citations)

    articles["title"] = publicationTitle
    articles["creator"] = publicationAuthor
    articles["publisher"] = publicationName
    articles["date"] = publicationDate
    articles["doi"] = publicationDoi
    articles["citations"] = publicationCitations
    return articles


def get_titles(api_key, keywords, year=2023):
    """
    Retrieve academic articles from Scopus based on specified keywords and publication year.

    Parameters:
    - api_key (str): Your Elsevier API key for authentication.
    - keywords (list of str): Keywords to search for in article titles and abstracts.
    - year (int, optional): The publication year to filter the articles. Default is 2023.

    Returns:
    - pd.DataFrame: A DataFrame containing the retrieved academic articles.
    """

    # Define the base URL and headers
    base_url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": api_key}

    # Construct the search query
    search_keywords = " AND ".join(f'"{w}"' for w in keywords)
    query = f"?query=TITLE-ABS-KEY({search_keywords})&date=1950-{year}&sort=relevance&start=0"

    # Send the initial request to get the total result count
    response = requests.get(base_url + query, headers=headers, timeout=20)
    result_len = int(response.json()["search-results"]["opensearch:totalResults"])

    # Initialize a list to store all entries
    all_entries = []

    for start in range(0, result_len, 25):
        if start >= 5000:  # Scopus throws an error above this value
            break

        # Construct the query with pagination
        query = f"?query=TITLE-ABS-KEY({search_keywords})&date=1950-{year}&sort=relevance&start={start}"

        # Send the request for the current page
        response = requests.get(base_url + query, headers=headers, timeout=30)

        if "entry" in response.json()["search-results"]:
            if "error" in response.json()["search-results"]["entry"][0]:
                continue
            else:
                all_entries.extend(response.json()["search-results"]["entry"])
        else:
            break

    # Create a DataFrame from the collected entries
    articles_loaded = create_article_dataframe(all_entries)

    print(f"Extraction for {keywords} completed")
    return articles_loaded
