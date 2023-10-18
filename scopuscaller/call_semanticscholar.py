import aiohttp
import asyncio
from random import choice
import nest_asyncio

nest_asyncio.apply()

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
    connector = aiohttp.TCPConnector(limit=1)

    list_doi = list(df["doi"])
    list_abstracts = []
    list_topics = []

    async with aiohttp.ClientSession(
        connector=connector, headers=random_headers(), timeout=timeout
    ) as session:  #
        tasks = [call_api_async(session, doi) for doi in list_doi]
        results = await asyncio.gather(*tasks, return_exceptions=False)

    for content in results:
        try:
            list_abstracts.append(content["abstract"])
            list_topics.append(content["topics"])
        except:
            list_abstracts.append("None")
            list_topics.append("None")

    return list_abstracts, list_topics


def get_abstracts(df):
    """
    Retrieve abstracts and topics for academic articles in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing academic articles.

    Returns:
    - pd.DataFrame: A DataFrame with abstracts and topics added.
    """

    # Print the total number of articles in the DataFrame
    print(f"Total articles: {len(df)}")

    # Filter out articles with no DOI
    df = df[df.doi != "No Doi"]

    # Run the asyncio event loop to fetch abstracts and topics asynchronously
    loop = asyncio.get_event_loop()
    list_abstracts, list_topics = loop.run_until_complete(fetch_articles_async(df))

    # Print the number of articles with abstracts
    print(f"Articles with abstracts: {len(list_abstracts)}")

    # Add abstracts and topics to the DataFrame
    df["abstract"] = list_abstracts
    df["topics"] = list_topics

    # Print a message indicating that the process is complete
    print(f"Done")

    return df
