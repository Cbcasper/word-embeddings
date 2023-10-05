import json

from loguru import logger
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

from baselines import rank_article
from embeddings import embedding_functions
from similarities import similarity_parameters, similarity_functions

app = Flask(__name__)
api = Api(app)
CORS(app)

Resource.method_decorators.append(logger.catch)

with open("data/article_export.json", "r") as file:
    articles = json.load(file)
    articles = {article["article"]["id"]: article["article"] for article in articles}

class Articles(Resource):
    def get(self):
        with open("data/article_export.json", "r") as file:
            return json.load(file)

class Embeddings(Resource):
    def get(self):
        return list(embedding_functions.keys())

class Similarities(Resource):
    def get(self):
        return list(similarity_functions.keys())

class Ranking(Resource):
    def get(self):
        article_id = request.args["id"]
        embedding = request.args["embedding"]
        similarity = request.args["similarity"]

        article = articles[article_id]["content"]
        ranking = rank_article(article, embedding, similarity)
        return {"ranking": [{"score": score, "field": field} for score, field in ranking],
                "similarity_parameters": similarity_parameters[similarity]}

api.add_resource(Articles, '/articles')
api.add_resource(Embeddings, '/embeddings')
api.add_resource(Similarities, '/similarities')
api.add_resource(Ranking, '/ranking')

if __name__ == '__main__':
    app.run(debug=True)