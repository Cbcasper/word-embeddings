from sklearn.metrics import pairwise

def cosine_similarity(article, field):
    return pairwise.cosine_similarity(article.reshape(1, -1), field.reshape(1, -1)).item()

similarities = {"cosine": cosine_similarity,
                "euclidean": None}