import json

from loguru import logger

from fields_of_interest_v1 import _FIELDS_OF_INTEREST

def compute_embedding_sbert():
    pass

@logger.catch
def main():
    with open("data/article_export.json", "r") as file:
        articles = json.load(file)
    articles = {article["article"]["id"]: article["article"] for article in articles}
    print(articles)

if __name__ == "__main__":
    main()