from sentence_transformers import SentenceTransformer
from device import device


class SBert:
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2').to(device)

    def embed(self, text):
        return self.model.encode(text, show_progress_bar=True)