from sentence_transformers import SentenceTransformer
from device import device


class SBert:
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2').to(device)

    def embed_document(self, documents, **kwargs):
        return self.embed([document["content"] for document in documents], **kwargs)

    def embed(self, text, show_progress_bar=False, **kwargs):
        return self.model.encode(text, show_progress_bar=show_progress_bar)