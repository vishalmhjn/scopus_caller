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

def create_article_dataframe(all_entries):
    'create data frame from the extracted json from API response'
    articles = pd.DataFrame(columns=['title', 'creator', 'publisher', 'date', 'doi', 'citations' ])
    publicationTitle = []
    publicationAuthor = []
    publicationName = []
    publicationDate = []
    publicationDoi = []
    publicationCitations = []

    for entry in all_entries:
        
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
    #%store articles
    return articles

