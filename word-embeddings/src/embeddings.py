from sentence_transformers import SentenceTransformer

from device import device

sbert_model = SentenceTransformer('all-mpnet-base-v2').to(device)

def embed_sbert(sentence):
    return sbert_model.encode(sentence, show_progress_bar=True)

embeddings = {"sbert": embed_sbert,
              "fasttext": None}
