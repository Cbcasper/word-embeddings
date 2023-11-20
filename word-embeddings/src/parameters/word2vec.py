from gensim.models import KeyedVectors
from utilities import Directory

class Word2Vec:
    def __init__(self, model):
        with Directory("models"):
            self.model = KeyedVectors.load_word2vec_format(model)

    def embed_document(self, documents, **kwargs):
        return self.embed([document["content"] for document in documents], **kwargs)

    def embed(self, text, **kwargs):
        for word in text.lower().split():
            try:
                self.model[word]
            except KeyError:
                print(f"{word} embedding not available")