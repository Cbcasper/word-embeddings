from tqdm import tqdm

from parameters.embeddings import embeddings
from parameters.similarities import similarities

class Ranker:
    def __init__(self, embedding_id, similarity_id, documents, show_progress_bar=False):
        self.embedding = embeddings[embedding_id]
        self.similarity = similarities[similarity_id]

        self.documents = documents
        self.document_embeddings = self.embedding.embed_document(self.documents, show_progress_bar=show_progress_bar)

    def rank_query(self, query, show_progress_bar=False):
        query_embedding, = self.embedding.embed_document([query], show_progress_bar=show_progress_bar)
        return self.rank(query_embedding, show_progress_bar)

    def rank(self, query_embedding, show_progress_bar=False):
        similarity_function = self.similarity["function"]
        reverse = self.similarity["parameters"]["reverse"]

        ranking = []
        embeddings = zip(self.documents, self.document_embeddings)
        if show_progress_bar: embeddings = tqdm(embeddings)
        for item, item_embedding in embeddings:
            item_similarity = similarity_function(query_embedding, item_embedding)
            ranking.append((item_similarity, item))
        return sorted(ranking, reverse=reverse, key=lambda document: document[0])
