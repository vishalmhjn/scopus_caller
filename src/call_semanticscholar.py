import json
import requests
import sys
import time
import pandas as pd


USER_AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) "
			  "AppleWebKit/537.36 (KHTML, like Gecko) "
			  "Chrome/54.0.2840.98 Safari/537.36"}


def call_api(doi):

	search_url = "http://api.semanticscholar.org/v1/paper/" + \
		doi+"?include_unknown_references=true"

	resp = requests.get(search_url, headers=USER_AGENT)
	content = resp.json()
	return content


if __name__ == '__main__':

	filename = sys.argv[2]
	df = pd.read_csv('../data/'+sys.argv[1])
	print(len(df))
	df = df[df.doi != "No Doi"]
	print(len(df))
	list_doi = list(df['doi'])
	list_abstracts = []
	list_topics = []
	i = 0
	for doi in list_doi:
		i = i+1
		print(i)
		try:
			content = call_api(doi)
			list_abstracts.append(content['abstract'])
			list_topics.append(content['topics'])
		except Exception as e:
			print(e)
			list_abstracts.append("None")
			list_topics.append("None")
		time.sleep(2)
	df['abstract'] = list_abstracts
	df['topics'] = list_topics
	df.to_csv('../data/abstracts_semantics'+filename+'.csv', index=None)

