import json

from loguru import logger

from embeddings import embeddings
from similarities import similarities
from fields_of_interest_v1 import _FIELDS_OF_INTEREST

def rank_article(article, embedding, similarity):
    fields = list(_FIELDS_OF_INTEREST.values())

    article_embedding = embedding(article)
    fields_embedding = embedding(fields)

    compute_pair = lambda field, embedding: (similarity(article_embedding, embedding), field)
    similarities = [compute_pair(field, embedding) for field, embedding in zip(fields, fields_embedding)]
    return sorted(similarities, reverse=True)

@logger.catch
def main():
    with open("data/article_export.json", "r") as file:
        articles = json.load(file)
    print(rank_article(articles[0]["article"]["content"], embeddings["sbert"], similarities["cosine"]))

if __name__ == "__main__":
    main()