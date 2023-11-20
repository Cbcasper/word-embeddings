import os

import pandas
from loguru import logger
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from joblib import dump, load

from content.datasets import prepare_dataset
from baseline.vectorizers import LemmaVectorizer, StemVectorizer

def train():
    articles = prepare_dataset("data/articles_dump.json")
    train, test = train_test_split(articles, test_size=.3, random_state=2002)

    tfidf_vectorizer = StemVectorizer(stop_words=stopwords.words("dutch"), max_features=5000, strip_accents="unicode")
    tfidf_vectorizer.fit(articles["content"])

    train_content = tfidf_vectorizer.transform(train["content"])
    test_content = tfidf_vectorizer.transform(test["content"])

    svm = LinearSVC(dual="auto")
    svm.fit(train_content, train["fieldsOfInterest"])

    accuracy = accuracy_score(train["fieldsOfInterest"], svm.predict(train_content))
    print(f"SVM reached train accuracy of {accuracy}")
    accuracy = accuracy_score(test["fieldsOfInterest"], svm.predict(test_content))
    print(f"SVM reached test accuracy of {accuracy}")

    dump(tfidf_vectorizer, "models/vectorizer.joblib")
    dump(svm, "models/classifier.joblib")

def classify(text):
    if not os.path.exists("models/vectorizer.joblib") or not os.path.exists("models/classifier.joblib"):
        train()
    vectorizer = load("models/vectorizer.joblib")
    model = load("models/classifier.joblib")
    return model.predict(vectorizer.transform((text,)))
