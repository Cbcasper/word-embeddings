from tqdm import tqdm

from .bert import BERT
from .sbert import SBert
from .fasttext import Fasttext
from .word2vec import Word2Vec

from utilities import catch

class ModelSetup:
    def __init__(self, name, model, *parameters):
        self.name = name
        self.model = model
        self.parameters = parameters

    def create(self):
        return self.model(*self.parameters)

@catch
def create_models(*model_setups):
    models = dict()
    progress = tqdm(model_setups)
    for model_setup in progress:
        progress.set_description(model_setup.name)
        models[model_setup.name] = model_setup.create()
    return models

models = create_models(
    ModelSetup("sbert", SBert),
    ModelSetup("fasttext", Fasttext),
    # ModelSetup("word2vec_clips", Word2Vec, "clips-roularta-320.txt"),
    # ModelSetup("word2vec_nlpl", Word2Vec, "nlpl-conll17.txt"),
    ModelSetup("BERTje", BERT, "GroNLP/bert-base-dutch-cased"),
    ModelSetup("RobBERT", BERT, "DTAI-KULeuven/robbert-2022-dutch-base"),
)
