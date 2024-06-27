import json

from loguru import logger
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

from ranker import Ranker
from evaluation import evaluate
from baseline.baseline import classify
from content.datasets import datasets, dataset_templates
from content.fieldsets import fieldsets
from parameters.embeddings import embeddings
from parameters.similarities import similarities

app = Flask(__name__)
api = Api(app)
CORS(app)

Resource.method_decorators.append(logger.catch)

class Datasets(Resource):
    def get(self):
        return list(datasets.keys())

class DatasetTemplates(Resource):
    def get(self):
        return list(dataset_templates.keys())

class Dataset(Resource):
    def get(self):
        dataset = request.args["dataset"]
        return datasets[dataset].data
    
    def post(self):
        id = request.args["id"]
        template = request.args["template"]
        dataset = request.files["dataset"].read()

        datasets[id] = dataset_templates[template](id, data=dataset)

class Fields(Resource):
    def get(self):
        return list(fieldsets.keys())

class Embeddings(Resource):
    def get(self):
        return list(embeddings.keys())

class Similarities(Resource):
    def get(self):
        return list(similarities.keys())

class FieldRanking(Resource):
    def get(self):
        pass

    def post(self):
        article = request.json["article"]
        fieldset_id = request.args["fields"]
        embedding_id = request.args["embedding"]
        similarity_id = request.args["similarity"]

        ranker = Ranker(embedding_id, similarity_id, fieldsets[fieldset_id])
        ranking = ranker.rank_query(article)
        return {"ranking": [{"score": score, "field": field} for score, field in ranking],
                "similarity_parameters": similarities[similarity_id]["parameters"]}

computed_document_rankers = dict()

class DocumentRanking(Resource):
    def get(self):
        pass

    def post(self):
        article = request.json["article"]
        dataset_id = request.args["dataset"]
        embedding_id = request.args["embedding"]
        similarity_id = request.args["similarity"]

        parameters = (dataset_id, embedding_id, similarity_id)
        if parameters in computed_document_rankers:
            ranker = computed_document_rankers[parameters]
        else:
            ranker = Ranker(embedding_id, similarity_id, datasets[dataset_id].data["articles"], show_progress_bar=True)
            computed_document_rankers[parameters] = ranker

        ranking = ranker.rank_query(article, show_progress_bar=True)
        return {"ranking": [{"score": score, "field": field} for score, field in ranking],
                "similarity_parameters": similarities[similarity_id]["parameters"]}

class Evaluation(Resource):
    def get(self):
        pass

    def post(self):
        dataset_id = request.args["dataset"]
        embedding_id = request.args["embedding"]
        similarity_id = request.args["similarity"]

        dataset_path = datasets[dataset_id].data["filename"]
        return {"accuracy": evaluate(dataset_path, embedding_id, similarity_id)}

class Classification(Resource):
    def get(self):
        pass

    def post(self):
        article = request.json["article"]
        classification, = classify(article)
        return {"classification": classification}

api.add_resource(Datasets, '/datasets')
api.add_resource(DatasetTemplates, '/dataset-templates')
api.add_resource(Dataset, '/dataset')
api.add_resource(Embeddings, '/embeddings')
api.add_resource(Similarities, '/similarities')
api.add_resource(FieldRanking, '/field-ranking')
api.add_resource(DocumentRanking, '/document-ranking')
api.add_resource(Evaluation, '/evaluation')
api.add_resource(Classification, '/classification')

if __name__ == '__main__':
    app.run(debug=True)