import numpy as np
import fasttext.util
from utilities import Directory

class Fasttext:
    def __init__(self):
        with Directory("models"):
            fasttext.util.download_model("nl", if_exists="ignore")
            self.model = fasttext.load_model("cc.nl.300.bin")

    def embed_document(self, documents, **kwargs):
        return self.embed([document["content"] for document in documents], **kwargs)

    def embed(self, text, **kwargs):
        return np.array([self.model.get_sentence_vector(subtext.replace("\n", "")) for subtext in text])