import json

from loguru import logger

from content.fieldsets import fieldsets
from parameters.embeddings import embeddings
from parameters.similarities import similarities

def rank_article(article, fields_id, embedding_id, similarity_id):
    fields = fieldsets[fields_id]
    embedding = embeddings[embedding_id]
    similarity = similarities[similarity_id]["function"]
    reverse = similarities[similarity_id]["parameters"]["reverse"]

    article_embedding, = embedding.embed([article])
    field_embeddings = embedding.embed(fields)

    ranked_fields = []
    for field, field_embedding in zip(fields, field_embeddings):
        field_similarity = similarity(article_embedding, field_embedding)
        ranked_fields.append((field_similarity, field))
    return sorted(ranked_fields, reverse=reverse)

@logger.catch
def main():
    with open("data/article_export.json", "r") as file:
        articles = json.load(file)
    article = articles[0]["article"]["content"]
    # print(rank_article(article, "v1", "sbert", "cosine"))
    print(embeddings["BERTje"].embed([article]))

if __name__ == "__main__":
    main()