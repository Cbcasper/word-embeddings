import json

from loguru import logger

from embeddings.embeddings import models
from similarities import similarity_functions, similarity_parameters
from fields_of_interest_v1 import _FIELDS_OF_INTEREST

def rank_article(article, embedding, similarity):
    fields = list(_FIELDS_OF_INTEREST.values())
    model = models[embedding]
    similarity_function = similarity_functions[similarity]

    article_embedding, = model.embed([article])
    field_embeddings = model.embed(fields)

    similarities = []
    for field, field_embedding in zip(fields, field_embeddings):
        field_similarity = similarity_function(article_embedding, field_embedding)
        similarities.append((field_similarity, field))
    return sorted(similarities, reverse=similarity_parameters[similarity]["reverse"])

@logger.catch
def main():
    with open("data/article_export.json", "r") as file:
        articles = json.load(file)
    article = articles[0]["article"]["content"]
    # print(rank_article(article, "sbert", "cosine"))
    print(models["BERTje"].embed([article]))

if __name__ == "__main__":
    main()