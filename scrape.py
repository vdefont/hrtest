from typing import List

import requests
from bs4 import BeautifulSoup

def search(query: str) -> List[str]:
    query_fmt = "%20".join(query.split())
    txt = requests.get(f"https://sfbay.craigslist.org/search/bia?postedToday=1&query={query_fmt}#search=1~list~0~0").text
    soup = BeautifulSoup(txt, "html.parser")
    results = soup.find_all(class_="cl-static-search-result")
    links = [r.find("a").get("href") for r in results]
    return links

print(search("giant"))
print(search("surly ice cream truck"))
print(search("surly wednesday"))