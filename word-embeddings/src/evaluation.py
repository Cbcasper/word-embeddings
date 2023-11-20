import pandas
from tqdm import tqdm
from sklearn.metrics import accuracy_score

from ranker import Ranker
from content.fieldsets import fieldsets
from content.datasets import prepare_dataset
from parameters.embeddings import embeddings

def evaluate(dataset_path, embedding_id, similarity_id):
    embedding = embeddings[embedding_id]
    articles = prepare_dataset(dataset_path)
    content = embedding.embed(articles["content"].to_list(), show_progress_bar=True)

    ranker = Ranker(embedding_id, similarity_id, fieldsets["v1"])

    predictions = [ranker.rank(article)[0][1] for article in tqdm(content)]
    return accuracy_score(articles["fieldsOfInterest"], predictions)