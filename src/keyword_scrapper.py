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

import requests
import pandas as pd
import pickle
import time
import sys

# FIRST_TERM = os.environ.get("FIRST_TERM")
# SECOND_TERM = os.environ.get("SECOND_TERM")
API_FILE = "../input/API"
KEYWORDS = sys.argv[1]


def create_article_dataframe(all_entries):
    "create data frame from the extracted json from API response"
    articles = pd.DataFrame(
        columns=["title", "creator", "publisher", "date", "doi", "citations"]
    )
    publicationTitle = []
    publicationAuthor = []
    publicationName = []
    publicationDate = []
    publicationDoi = []
    publicationCitations = []

    for entry in all_entries:
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
    # %store articles
    return articles


def query_scopus(FIRST_TERM, SECOND_TERM):
    """
    To quert scopus using API and cetrain keywords.
    This returns approximate matches with the keywords
    """

    API_KEY = open(API_FILE, "r").readline().rstrip()

    X_ELS_APIKey = API_KEY  # API Key
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": X_ELS_APIKey}

    # Enter the keyword inside the double quotations for approximate phrase match
    query = '?query=TITLE-ABS-KEY("' + FIRST_TERM + '"+AND+"' + SECOND_TERM + '")'
    query += "&date=1950-" + str(CURRENT_YEAR)
    query += "&sort=relevance"
    query += "&start=0"
    r = requests.get(url + query, headers=headers)
    result_len = int(r.json()["search-results"]["opensearch:totalResults"])
    print(result_len)
    all_entries = []

    for start in range(0, result_len, 25):
        if start < 5000:  # Scopus throws an error above this value
            entries = []
            # Enter the keyword inside the braces for exact phrase match
            # query = '?query={'+first_term+'}+AND+{'+second_term+'}'
            # Enter the keyword inside the double quotations for approximate phrase match
            query = (
                '?query=TITLE-ABS-KEY("' + FIRST_TERM + '"+AND+"' + SECOND_TERM + '")'
            )
            query += "&date=1950-" + str(CURRENT_YEAR)
            query += "&sort=relevance"
            # query += '&subj=ENGI' # This is commented because many results might not be covered under ENGI
            query += "&start=%d" % (start)
            # query += '&count=%d' % (count)
            r = requests.get(url + query, headers=headers)
            if "entry" in r.json()["search-results"]:
                if "error" in r.json()["search-results"]["entry"][0]:
                    continue
                else:
                    entries += r.json()["search-results"]["entry"]
            if len(entries) != 0:
                all_entries.extend(entries)
            else:
                break

    articles = create_article_dataframe(all_entries)
    articles.to_csv(
        "../data/Results_" + FIRST_TERM + "_" + SECOND_TERM + ".csv",
        sep=",",
        encoding="utf-8",
    )
    print("Extraction for %s and %s completed" % (FIRST_TERM, SECOND_TERM))
    return all_entries


if __name__ == "__main__":
    print(KEYWORDS)
    keywords = pd.read_csv(KEYWORDS)
    print(keywords)
    print(keywords.columns)

    CURRENT_YEAR = 2022
    print(f"Current year is set to {CURRENT_YEAR}")

    first_keywords = list(keywords["term1"])
    second_keywords = list(keywords["term2"])
    second_keywords = [x for x in second_keywords if str(x) != "nan"]

    # comment these if running all the new keywords
    # second_keywords = second_keywords[-1]
    # first_keywords = first_keywords[-1]

    # Store the resonses in a list to check for Abstract avaiability later
    entries_hrefs = []

    if len(first_keywords[0]) == 1:
        first_keywords = [first_keywords]
    if len(second_keywords[0]) == 1:
        second_keywords = [second_keywords]

    for first_term in first_keywords:
        for second_term in second_keywords:
            entries_hrefs.extend(query_scopus(first_term, second_term))

    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open("../data/href_entries_pickle" + timestr, "wb") as fp:
        pickle.dump(entries_hrefs, fp)
        print("Done")
