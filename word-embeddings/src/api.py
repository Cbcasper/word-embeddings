import json

from loguru import logger
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

from main import rank_article
from content.datasets import datasets
from content.fieldsets import fieldsets
from parameters.embeddings import embeddings
from parameters.similarities import similarities

app = Flask(__name__)
api = Api(app)
CORS(app)

Resource.method_decorators.append(logger.catch)

articles_file = "data/article_export.json"
with open(articles_file, "r") as file:
    articles = json.load(file)
    articles = {article["article"]["id"]: article["article"] for article in articles}

class Datasets(Resource):
    def get(self):
        return list(datasets.keys())

class Dataset(Resource):
    def get(self):
        dataset = request.args["dataset"]
        return datasets[dataset].data

class Fields(Resource):
    def get(self):
        return list(fieldsets.keys())

class Embeddings(Resource):
    def get(self):
        return list(embeddings.keys())

class Similarities(Resource):
    def get(self):
        return list(similarities.keys())

class Ranking(Resource):
    def post(self):
        article = request.json["article"]
        fields_id = request.args["fields"]
        embedding_id = request.args["embedding"]
        similarity_id = request.args["similarity"]

        ranking = rank_article(article, fields_id, embedding_id, similarity_id)
        return {"ranking": [{"score": score, "field": field} for score, field in ranking],
                "similarity_parameters": similarities[similarity_id]["parameters"]}

api.add_resource(Datasets, '/datasets')
api.add_resource(Dataset, '/dataset')
api.add_resource(Embeddings, '/embeddings')
api.add_resource(Similarities, '/similarities')
api.add_resource(Ranking, '/ranking')

if __name__ == '__main__':
    app.run(debug=True)