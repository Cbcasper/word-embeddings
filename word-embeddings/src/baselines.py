import json

from loguru import logger

from embeddings import embedding_functions
from similarities import similarity_functions, similarity_parameters
from fields_of_interest_v1 import _FIELDS_OF_INTEREST

def rank_field_embeddings(fields, field_embeddings, article_embedding, similarity):
    similarity_function = similarity_functions[similarity]

    similarities = []
    for field, field_embedding in zip(fields, field_embeddings):
        field_similarity = similarity_function(article_embedding, field_embedding)
        similarities.append((field_similarity, field))
    return sorted(similarities, reverse=similarity_parameters[similarity]["reverse"])

def rank_article(article, embedding, similarity):
    fields = list(_FIELDS_OF_INTEREST.values())
    embedding_function = embedding_functions[embedding]

    article_embedding = embedding_function([article])
    field_embeddings = embedding_function(fields)

    return rank_field_embeddings(fields, field_embeddings, article_embedding, similarity)

@logger.catch
def main():
    with open("data/article_export.json", "r") as file:
        articles = json.load(file)
    print(rank_article(articles[0]["article"]["content"], "sbert", "cosine"))

if __name__ == "__main__":
    main()