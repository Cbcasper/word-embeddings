import numpy as np
import fasttext.util
from utilities import Directory

class Fasttext:
    def __init__(self):
        with Directory("pretrained_models"):
            fasttext.util.download_model("nl", if_exists="ignore")
            self.model = fasttext.load_model("cc.nl.300.bin")

    def embed(self, text):
        return np.array([self.model.get_sentence_vector(subtext) for subtext in text])