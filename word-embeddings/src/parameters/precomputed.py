class Precomputed:
    def __init__(self):
        pass

    def embed_document(self, documents, **kwargs):
        return [document["embedding"] for document in documents]

    def embed(self, text, **kwargs):
        raise NotImplementedError("embedding method PreComputed only uses precomputed embeddings")