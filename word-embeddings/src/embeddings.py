import numpy as np
import fasttext.util
from sentence_transformers import SentenceTransformer

from device import device
from utilities import Directory

sbert_model = SentenceTransformer('all-mpnet-base-v2').to(device)

with Directory("pretrained_models"):
    fasttext.util.download_model("nl", if_exists="ignore")
    fasttext_model = fasttext.load_model("cc.nl.300.bin")

def embed_sbert(text):
    return sbert_model.encode(text, show_progress_bar=True)

def embed_fasttext(text):
    return np.array([fasttext_model.get_sentence_vector(subtext) for subtext in text])

embedding_functions = {"sbert": embed_sbert,
                       "fasttext": embed_fasttext}
