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
import argparse
from datetime import datetime


API_FILE = "../input/API"

def create_article_dataframe(allentries):
    'create data frame from the extracted json from API response'
    articles = pd.DataFrame(
        columns=['title', 'creator', 'publisher', 'date', 'doi', 'citations'])
    publicationTitle = []
    publicationAuthor = []
    publicationName = []
    publicationDate = []
    publicationDoi = []
    publicationCitations = []

    for entry in allentries:

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

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', default=-1, type=int,
                        help='Year to search for in Scopus (default: current year)')
    parser.add_argument('--api', default="", type=str,
                        help='API key to use for Scopus (default: read from file)')
    parser.add_argument('keywords', nargs='+',
                        help='Keywords to search for in Scopus')
    args = parser.parse_args()

    # Get year
    if args.year > 0:
        year = args.year
    else:
        year = datetime.now().year

    # Get API key
    if args.api != "":
        api_key = args.api
    else:
        api_key = open(API_FILE, 'rb').readline().rstrip()

    return year, api_key, args.keywords

if __name__ == "__main__":

    YEAR, API_KEY, KEYWORDS = get_arguments()

    print(f"Current year is set to {YEAR}")

    url = 'https://api.elsevier.com/content/search/scopus'
    headers = {'X-ELS-APIKey': API_KEY}

    search_keywords = " AND ".join(f'"{w}"' for w in KEYWORDS)
    print(search_keywords)
    query = f'?query=TITLE-ABS-KEY({search_keywords})'
    query += f'&date=1950-{YEAR}'
    query += '&sort=relevance'
    query += '&start=0'
    r = requests.get(url + query, headers=headers, timeout=20)
    result_len = int(r.json()['search-results']['opensearch:totalResults'])
    print(result_len)
    all_entries = []

    for start in range(0, result_len, 25):
        if start < 5000:  # Scopus throws an error above this value
            entries = []
            # query = '?query={'+first_term+'}+AND+{'+second_term+'}' #Enter the keyword inside the braces for exact phrase match
            # Enter the keyword inside the double quotations for approximate phrase match
            query = f'?query=TITLE-ABS-KEY({search_keywords})'
            query += f'&date=1950-{YEAR}&sort=relevance'
            # query += '&subj=ENGI' # This is commented because many results might not be covered under ENGI
            query += '&start=%d' % (start)
            #query += '&count=%d' % (count)
            r = requests.get(url + query, headers=headers, timeout=30)
            if 'entry' in r.json()['search-results']:
                if 'error' in r.json()['search-results']['entry'][0]:
                    continue
                else:
                    entries += r.json()['search-results']['entry']
            if len(entries) != 0:
                all_entries.extend(entries)
            else:
                break
    articles_loaded = pd.DataFrame()
    articles_loaded = create_article_dataframe(all_entries)
    file_name = "_".join(KEYWORDS)
    articles_loaded.to_csv(f'../data/Results_{file_name}.csv',
                    sep=',', encoding='utf-8')
    print(f'Extraction for {KEYWORDS} completed')
