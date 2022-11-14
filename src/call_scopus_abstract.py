import requests
import xml.etree.ElementTree as ET

import json
import pandas as pd
import numpy as np
import os, re, pickle, sys

#articles.StoreMagics.autorestore = True
FOLDER = sys.argv[1]
API_FILE = "../input/API"
READ_ALL = sys.argv[2]
PICKLE_FILE = str(sys.argv[3])

def get_full_text_links(scopus_hrefs):
    hrefs = []
    for entry in scopus_hrefs:
        #title = entry['dc:title']
        #creator = entry['dc:creator']
        #publicationName = entry['prism:publicationName']
        links = entry['link']
        for link in links:
            if link['@ref'] == 'full-text':
                href = link['@href']
                hrefs.append(href)
    print(len(hrefs))
    return hrefs

def abstract_dataframe(hrefs):
    articlesFull = pd.DataFrame(columns=['url', 'title', 'creators', 'subjects', 'description', 'publicationName'])
    for i in range(0, len(hrefs)):
        sys.stdout.write('\r'+str(hrefs[i]))
        # the exact output you're looking for:
        sys.stdout.write("[%-100s] %d%%" % ('='*int(np.round(100*i/len(hrefs))), int(np.round(100*i/len(hrefs)))))
        sys.stdout.flush()
        
        url = hrefs[i]
        article = {}
        article['url'] = url
        r = requests.get(url, headers=headers)
        
        json_obj = json.loads(r.text)
        try:
            article['title'] = json_obj['full-text-retrieval-response']['coredata']['dc:title']
        except:
            pass

        try:
            article['creators'] = [i['$'] for i in json_obj['full-text-retrieval-response']['coredata']['dc:creator']]
        except KeyError:
            article['creators'] = 0
        except TypeError:
            article['creators'] = json_obj['full-text-retrieval-response']['coredata']['dc:creator']['$']

        try:
            article['subjects'] = [i['$'] for i in json_obj['full-text-retrieval-response']['coredata']['dcterms:subject']]
        except KeyError:
            article['subjects'] = 0
        except TypeError:
            article['subjects'] = json_obj['full-text-retrieval-response']['coredata']['dcterms:subject']['$']
        
        try:
            article['description'] = json_obj['full-text-retrieval-response']['coredata']['dc:description']
        except KeyError:
            article['description'] = 0
        
        try:
            article['publicationName'] = json_obj['full-text-retrieval-response']['coredata']['prism:publicationName']
        except KeyError:
            article['description'] = 0

        try:
            article['date'] = json_obj['full-text-retrieval-response']['coredata']['prism:coverDate']
        except KeyError:
            article['date'] = 0
        
        if article['description']:
            articlesFull = articlesFull.append(article, ignore_index=True)
    return articlesFull

if __name__ == '__main__':
    
    API_KEY = open(API_FILE, 'r').readline().rstrip()
    X_ELS_APIKey = API_KEY 
    url = 'https://api.elsevier.com/content/search/scopus'
    headers = {'X-ELS-APIKey': X_ELS_APIKey, 'Accept': 'application/json'}

    entries_href = []
    if READ_ALL == 1:
        for f in os.listdir(FOLDER):
            if re.match('href_entries_pickle', f):
                with open(FOLDER+f, 'rb') as fp:
                    entries_href.extend(pickle.load(fp))
    else:
        with open('../data/'+PICKLE_FILE, 'rb') as fp:
            entries_href.extend(pickle.load(fp))

    print('Links Read')
    abstract_text_hrefs = get_full_text_links(entries_href)
    df_abstract_text = abstract_dataframe(abstract_text_hrefs)
    df_abstract_text.to_csv('../data/abstracts_2201.csv', sep=',', encoding='utf-8')