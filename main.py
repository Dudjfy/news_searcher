import urllib
import requests as req
from bs4 import BeautifulSoup
from PIL import Image


class NewsSearcher:
    sources = {
        "expressen": "https://www.expressen.se/",
        "svt": "https://www.svt.se/",
        "aftonbladet": "https://www.aftonbladet.se/",
        "dn": "https://www.dn.se/",
    }
    topics_and_links = {
        "expressen": dict(),
        "svt": dict(),
        "aftonbladet": dict(),
        "dn": dict(),
    }
    common_topics_and_links = {
        "expressen": dict(),
        "svt": dict(),
        "aftonbladet": dict(),
        "dn": dict(),
    }
    display_names = {
        "expressen": "Expressen",
        "svt": "SVT",
        "aftonbladet": "Aftonbladet",
        "dn": "DN",
    }

    def find_topics_and_links(self):
        for news_outlet, website in self.sources.items():
            url = req.get(website)
            soup = BeautifulSoup(url.text, "html.parser")

            for a_tag in soup.find_all("a"):
                if a_tag.has_attr("href") and isinstance(a_tag.string, str):
                    self.topics_and_links[news_outlet][a_tag.string.lower().strip()] = a_tag["href"]

    def find_common_topics_and_links(self):
        for topic, link in self.topics_and_links["expressen"].items():
            if topic not in self.topics_and_links["svt"]:
                continue
            if topic not in self.topics_and_links["aftonbladet"]:
                continue
            if topic not in self.topics_and_links["dn"]:
                continue

            for news_outlet, topic_collection in self.common_topics_and_links.items():
                self.common_topics_and_links[news_outlet][topic] = self.topics_and_links[news_outlet][topic]

    def create_common_topics_and_links(self):
        self.find_topics_and_links()
        self.find_common_topics_and_links()
        self.transform_relative_links_to_absolute()

    def transform_relative_links_to_absolute(self):
        for news_outlet, topic_collection in self.common_topics_and_links.items():
            for topic, link in topic_collection.items():
                if "https://" not in link:
                    self.common_topics_and_links[news_outlet][topic] = f"{self.sources[news_outlet][:-1]}{link}"


ns = NewsSearcher()
ns.create_common_topics_and_links()
print(ns.common_topics_and_links)
