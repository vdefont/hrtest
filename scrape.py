"""
TODO - upload to heroku
"""


from typing import List, NamedTuple

import requests
from bs4 import BeautifulSoup

from send_email import send_email

"""
TODO:
- Debug filter links
- Figure out how to email notif
"""


CL_CITIES = [["fresno", 93702], ["wichita", 67202], ["washingtondc", 20004]]


def fetch_links(url: str) -> List[str]:
    txt = requests.get(url).text
    soup = BeautifulSoup(txt, "html.parser")
    results = soup.find_all(class_="cl-static-search-result")
    links = [r.find("a").get("href") for r in results]
    return links

def link_has_words(link: str, title_words: List[str], words: List[str]) -> List[str]:
    txt = requests.get(link).text
    title = BeautifulSoup(txt, "html.parser").find('title').string.lower()
    return all(w in title for w in title_words) and all(w in txt.lower() for w in words)

def filter_links(links: List[str], title_words: List[str], words: List[str]) -> List[str]:

    return [l for l in links if link_has_words(l, title_words, words)]

class SearchInfo(NamedTuple):
    # Craigslist query
    query: str
    # Result must have all these words in the title
    title_words: List[str]
    # Result must have all these words anywhere in the listing
    words: List[str] = []

def search(search: SearchInfo) -> str:
    query_fmt = "%20".join(search.query.split())
    links = []
    for city, zip in CL_CITIES:
        url = f"https://{city}.craigslist.org/search/sss?bundleDuplicates=1" \
              f"&postal={zip}&postedToday=1&query={query_fmt}&search_distance=1000&sort=date#search=1~list~0~0"
        links.extend(fetch_links(url))
    links = filter_links(links, search.title_words, search.words)
    return "\n".join([search.query] + links)

def run_searches(searches: List[SearchInfo]) -> str:
    return "\n\n".join(search(s) for s in searches)

SEARCHES = [
    SearchInfo(
        query="surly ice cream truck",
        title_words=["surly"],
        words=["surly", "ice cream"],
    ),
    SearchInfo(
        query="surly wednesday",
        title_words=["surly"],
        words=["surly", "wednesday"],
    ),
    SearchInfo(
        query="leica m6",
        title_words=["leica"],
        words=["m6"],
    ),
]

results = run_searches(SEARCHES)
print("SEARCH RESULTS:\n\n", results)
send_email(results)
