import aiohttp
import asyncio
import requests
import sys
import time
import pandas as pd
from random import choice
from tqdm import tqdm

desktop_agents = [""]
BASE_API_URL = "http://api.semanticscholar.org/v1/paper/"


def random_headers():
    return {
        "User-Agent": choice(desktop_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }


async def call_api_async(session, doi):
    search_url = BASE_API_URL + doi + "?include_unknown_references=true"

    headers = random_headers()

    async with session.get(search_url, headers=headers) as response:
        content = await response.json()
        return content


async def fetch_articles_async(df):
    timeout = aiohttp.ClientTimeout(total=10 * 60)
    connector = aiohttp.TCPConnector(limit=5)

    list_doi = list(df["doi"])
    list_abstracts = []
    list_topics = []

    async with aiohttp.ClientSession(
        connector=connector, headers=random_headers(), timeout=timeout
    ) as session:  #
        tasks = [call_api_async(session, doi) for doi in list_doi]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for content in results:
        list_abstracts.append(content["abstract"])
        list_topics.append(content["topics"])

    return list_abstracts, list_topics


if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])

    print(f"Total articles: {len(df)}")

    df = df[df.doi != "No Doi"]
    print(f"Articles with abstracts: {len(df)}")

    loop = asyncio.get_event_loop()
    list_abstracts, list_topics = loop.run_until_complete(fetch_articles_async(df))

    df["abstract"] = list_abstracts
    df["topics"] = list_topics

    output_file = "../data/abstracts_" + sys.argv[1].split("/")[-1][:-4] + ".csv"
    df.to_csv(output_file, index=None)
