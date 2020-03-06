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

