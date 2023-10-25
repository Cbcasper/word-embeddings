import pandas
from loguru import logger

from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords

from vectorizers import LemmaVectorizer, StemVectorizer

@logger.catch
def main():
    unpack = lambda list: list[0]

    articles = pandas.read_json("../data/articles_dump.json")
    articles = articles[articles["keywords"].apply(len) == 1]
    articles[["keywords", "fieldsOfInterest"]] = articles[["keywords", "fieldsOfInterest"]].map(unpack)

    train, test = train_test_split(articles, test_size=.3)

    tfidf_vectorizer = StemVectorizer(stop_words=stopwords.words("dutch"), max_features=5000, strip_accents="unicode")
    tfidf_vectorizer.fit(articles["content"])

    train_content = tfidf_vectorizer.transform(train["content"])
    test_content = tfidf_vectorizer.transform(test["content"])

    svm = LinearSVC(dual="auto")
    svm.fit(train_content, train["fieldsOfInterest"])

    print(accuracy_score(svm.predict(test_content), test["fieldsOfInterest"]))

if __name__ == "__main__":
    main()