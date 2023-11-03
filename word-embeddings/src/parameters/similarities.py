from sklearn.metrics import pairwise

def cosine_similarity(article, field):
    return pairwise.cosine_similarity(article.reshape(1, -1), field.reshape(1, -1)).item()

def euclidean_distance(article, field):
    return pairwise.euclidean_distances(article.reshape(1, -1), field.reshape(1, -1)).item()

def manhattan_distance(article, field):
    return pairwise.manhattan_distances(article.reshape(1, -1), field.reshape(1, -1)).item()

similarities = {"cosine": {"function": cosine_similarity, "parameters": {"reverse": False}},
                "euclidean": {"function": euclidean_distance, "parameters": {"reverse": True}},
                "manhattan": {"function": manhattan_distance, "parameters": {"reverse": True}}}