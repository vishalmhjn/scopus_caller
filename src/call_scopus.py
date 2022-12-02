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

import sys

import pandas as pd
import requests

API_FILE = "../input/API"


def test_function_with_lots_of_args(name: str, id_nr: int, age: int, title: str, creator: str, publisher: str,
                                    doi: str, citations: str):
    print(f"test_function_with_lots_of_args was called")


def create_article_dataframe(all_entries):
    'create data frame from the extracted json from API response'
    articles = pd.DataFrame(
        columns=['title', 'creator', 'publisher', 'date', 'doi', 'citations'])
    publicationTitle = []
    publicationAuthor = []
    publicationName = []
    publicationDate = []
    publicationDoi = []
    publicationCitations = []

    for entry in all_entries:
        if False:
            test_function_with_lots_of_args('Some_name',
                                            1234,
                                            1234,
                                            'test_title',
                                            'creator_name',
                                            'publisher',
                                            'doi',
                                            'citations')

        if 'dc:title' in entry:
            title = entry['dc:title']
            publicationTitle.append(title)
        else:
            print(entry)
            continue

        if 'dc:creator' in entry:
            author = entry['dc:creator']
            publicationAuthor.append(author)
        else:
            author = 'No author'
            publicationAuthor.append(author)

        if 'prism:publicationName' in entry:
            name = entry['prism:publicationName']
            publicationName.append(name)
        else:
            name = 'No publication name'
            publicationName.append(name)

        date = entry['prism:coverDate']
        publicationDate.append(date)

        if 'prism:doi' in entry:
            doi = entry['prism:doi']
            publicationDoi.append(doi)
        else:
            doi = 'No Doi'
            publicationDoi.append(doi)

        if 'citedby-count' in entry:
            citations = entry['citedby-count']
            publicationCitations.append(citations)
        else:
            citations = 'No data'
            publicationCitations.append(citations)

    articles['title'] = publicationTitle
    articles['creator'] = publicationAuthor
    articles['publisher'] = publicationName
    articles['date'] = publicationDate
    articles['doi'] = publicationDoi
    articles['citations'] = publicationCitations
    return articles


if __name__ == "__main__":

    API_KEY = open(API_FILE, 'r').readline().rstrip()
    CURRENT_YEAR = 2022

    print(f"Current year is set to {CURRENT_YEAR}")

    X_ELS_APIKey = API_KEY  # API Key
    url = 'https://api.elsevier.com/content/search/scopus'
    headers = {'X-ELS-APIKey': X_ELS_APIKey}

    search_keywords = "\" AND \"".join(list(sys.argv[1:]))
    print('"' + search_keywords + '"')
    query = '?query=TITLE-ABS-KEY("' + search_keywords + '")'
    query += '&date=1950-' + str(CURRENT_YEAR)
    query += '&sort=relevance'
    query += '&start=0'
    r = requests.get(url + query, headers=headers)
    result_len = int(r.json()['search-results']['opensearch:totalResults'])
    print(result_len)
    all_entries = []

    for start in range(0, result_len, 25):
        if start < 5000:  # Scopus throws an error above this value
            entries = []
            # query = '?query={'+first_term+'}+AND+{'+second_term+'}' #Enter the keyword inside the braces for exact
            # phrase match
            # Enter the keyword inside the double quotations for approximate phrase match
            query = '?query=TITLE-ABS-KEY("' + search_keywords + '")'
            query += '&date=1950-' + str(CURRENT_YEAR)
            query += '&sort=relevance'
            # query += '&subj=ENGI' # This is commented because many results might not be covered under ENGI
            query += '&start=%d' % (start)
            # query += '&count=%d' % (count)
            r = requests.get(url + query, headers=headers)
            if 'entry' in r.json()['search-results']:
                if 'error' in r.json()['search-results']['entry'][0]:
                    continue
                else:
                    entries += r.json()['search-results']['entry']
            if len(entries) != 0:
                all_entries.extend(entries)
            else:
                break
    articles = pd.DataFrame()
    articles = create_article_dataframe(all_entries)
    file_name = "_".join(list(sys.argv[1:]))
    articles.to_csv('../data/Results_' + str(file_name) +
                    '.csv', sep=',', encoding='utf-8')
    print('Extraction for %s completed' % ('"' + search_keywords + '"'))
