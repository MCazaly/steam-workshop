import requests
from collections import OrderedDict
from bs4 import BeautifulSoup


WORKSHOP_URL = "https://steamcommunity.com/sharedfiles/filedetails/?id={0}"


class Collection(object):
    id = None
    url = None
    title = None
    author = None
    items = OrderedDict()
    collections = OrderedDict()

    def __init__(self, workshop_id: str, fetch: bool = True):
        self.id = workshop_id
        self.url = WORKSHOP_URL.format(workshop_id)
        if fetch:
            self.fetch()

    def fetch(self):
        print(f"Fetching Collection ID \"{self.id}\"")
        response = requests.get(self.url)
        response.raise_for_status()
        items = OrderedDict()
        collections = OrderedDict()

        soup = BeautifulSoup(response.text, "html.parser")
        for meta in soup.find_all("meta"):
            if "property" in meta:
                if meta["property"] == "twitter:title":
                    # Collection title
                    self.title = meta["content"][16::]  # Trimmed to remove "Steam Workshop::" qualifier
                    continue
        children = soup.find_all("div", {"class": "collectionChildren"})
        for div in children[0].find_all("div"):
            # Workshop items
            if "class" in div.attrs:
                if "collectionItemDetails" in div.attrs["class"]:
                    container = div.find_all("a")  # We can't assume only 2 <a> tags...
                    item = container[0]
                    author = container[1]
                    url = item["href"]
                    workshop_id = get_id(url)
                    title = item.text
                    author_profile = author["href"].split("/myworkshopfiles?")[0]
                    items[workshop_id] = {
                        "url": url,
                        "title": title,
                        "author": author_profile
                    }
        if len(children) > 1:
            for div in children[1].find_all("div"):
                # Linked collections
                if "class" in div.attrs:
                    if "workshopItem" in div.attrs["class"]:
                        url = div.find("a")["href"]
                        workshop_id = get_id(url)
                        collection = Collection(workshop_id)
                        collections[workshop_id] = collection

        self.items = items
        self.collections = collections

    def to_dict(self):
        collections = OrderedDict()
        for workshop_id in self.collections.keys():
            collections[workshop_id] = self.collections[workshop_id].to_dict()
        return OrderedDict({
            "items": self.items,
            "collections": collections
        })


def get_id(url: str):
    return url.split("id=")[1]
