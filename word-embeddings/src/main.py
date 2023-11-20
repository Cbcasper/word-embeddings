import json

from tqdm import tqdm
from loguru import logger

from ranker import Ranker
from evaluation import evaluate
from baseline.baseline import train
from content.datasets import datasets
from content.fieldsets import fieldsets
from parameters.embeddings import embeddings
from parameters.similarities import similarities
from parameters.bert import BERTTokenizer

@logger.catch
def main():
    # [embeddings["BERTje"].embed([article["content"]]) for article in tqdm(datasets["labeled"].data["articles"])]
    # print(evaluate(datasets["labeled"].data["filename"], "sbert", "cosine"))

    # article = datasets["labeled"].data["articles"][0]["content"]
    # print(embeddings["BERTje"].embed([article], pooling="max"))

    train()

if __name__ == "__main__":
    main()