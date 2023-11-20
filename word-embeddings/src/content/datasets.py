import json
import pandas
from content.fields_of_interest_v1 import _FIELDS_OF_INTEREST

class ArticleExportJSON:
    def __init__(self, id, filename=None, data=None):
        if filename:
            with open(filename, "r") as file:
                self.data = json.load(file)
        elif not isinstance(data, json.JSONDecoder):
            self.data = json.loads(data)
        else:
            self.data = data
        self.data = {
            "id": id,
            "filename": filename,
            "articles": [article["article"] for article in self.data]
        }

class ArticlesDumpJSON:
    def __init__(self, id, filename=None, data=None):
        if filename:
            with open(filename, "r") as file:
                self.data = json.load(file)
        elif not isinstance(data, json.JSONDecoder):
            self.data = json.loads(data)
        else:
            self.data = data
        self.data = {
            "id": id,
            "filename": filename,
            "articles": [self.adjust_article(article) for article in self.data]
        }

    def adjust_article(self, article):
        return {
            **article,
            **self.adjust_fields(article),
            "title": f"{article['content'][:75]}...",
            "subTitle": None
        }
    
    def adjust_fields(self, article):
        if len(article["keywords"]) == 0:
            return dict()
        return {
            "keywords": article["keywords"][0],
            "fieldsOfInterest": _FIELDS_OF_INTEREST[article["fieldsOfInterest"][0]],
        }

def prepare_dataset(dataset_path):
    unpack = lambda list: list[0]

    articles = pandas.read_json(dataset_path)
    articles = articles[articles["keywords"].apply(len) == 1]
    articles[["keywords", "fieldsOfInterest"]] = articles[["keywords", "fieldsOfInterest"]].map(unpack)
    articles["fieldsOfInterest"] = articles["fieldsOfInterest"].map(lambda field: _FIELDS_OF_INTEREST[field])
    return articles

datasets = {
    "article_export.json": ArticleExportJSON("article_export.json", filename="data/article_export.json"),
    "articles_dump.json": ArticlesDumpJSON("articles_dump.json", filename="data/articles_dump.json")
}

dataset_templates = {
    "ArticleExportJSON": ArticleExportJSON,
    "ArticlesDumpJSON": ArticlesDumpJSON,
}