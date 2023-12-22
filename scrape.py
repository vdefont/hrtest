from typing import List

import requests
from bs4 import BeautifulSoup

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

def link_has_words(link: str, req_words: List[str]) -> List[str]:
    txt = requests.get(link).text
    return all(word in txt for word in req_words)
def filter_links(links: List[str], req_words: List[str]) -> List[str]:

    return [l for l in links if link_has_words(l, req_words)]
def search(query: str, req_words: List[str]) -> List[str]:
    """

    :param query: What to search for on CL
    :param req_words: Each of these words must appear someplace in the listing (eg. title, body)
    :return:
    """
    query_fmt = "%20".join(query.split())
    links = []
    for city, zip in CL_CITIES:
        url = f"https://{city}.craigslist.org/search/sss?bundleDuplicates=1&postal={zip}&postedToday=1&query={query_fmt}&search_distance=1000&sort=date#search=1~gallery~0~0"
        links.extend(fetch_links(url))
    return filter_links(links, req_words)


print(search("surly ice cream truck", ["surly", "ice cream truck"]))
print(search("surly", ["surly", "pack rat"]))