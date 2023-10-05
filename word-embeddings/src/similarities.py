from sklearn.metrics import pairwise

def cosine_similarity(article, field):
    return pairwise.cosine_similarity(article.reshape(1, -1), field.reshape(1, -1)).item()

def euclidean_distance(article, field):
    return pairwise.euclidean_distances(article.reshape(1, -1), field.reshape(1, -1)).item()

def manhattan_distance(article, field):
    return pairwise.manhattan_distances(article.reshape(1, -1), field.reshape(1, -1)).item()

similarity_parameters = {"cosine": {"reverse": False},
                         "euclidean": {"reverse": True},
                         "manhattan": {"reverse": True}}

similarity_functions = {"cosine": cosine_similarity,
                        "euclidean": euclidean_distance,
                        "manhattan": manhattan_distance}