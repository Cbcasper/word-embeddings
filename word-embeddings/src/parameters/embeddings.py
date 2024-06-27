from tqdm import tqdm

from .bert import BERT
from .sbert import SBert
from .fasttext import Fasttext
# from .word2vec import Word2Vec
from .precomputed import Precomputed

from utilities import catch_exit

class EmbeddingSetup:
    def __init__(self, name, embedding, *parameters):
        self.name = name
        self.embedding = embedding
        self.parameters = parameters

    def create(self):
        return self.embedding(*self.parameters)

@catch_exit
def create_embeddings(*model_setups):
    embeddings = dict()
    progress = tqdm(model_setups)
    for embedding_setup in progress:
        progress.set_description(embedding_setup.name)
        embeddings[embedding_setup.name] = embedding_setup.create()
    return embeddings

embeddings = create_embeddings(
    EmbeddingSetup("sbert", SBert),
    EmbeddingSetup("fasttext", Fasttext),
    # EmbeddingSetup("word2vec_clips", Word2Vec, "clips-roularta-320.txt"),

    # download from http://vectors.nlpl.eu/repository/
    # EmbeddingSetup("word2vec_nlpl", Word2Vec, "nlpl-conll17.txt"),
    EmbeddingSetup("BERTje", BERT, "GroNLP/bert-base-dutch-cased"),
    EmbeddingSetup("RobBERT", BERT, "DTAI-KULeuven/robbert-2022-dutch-base"),
    EmbeddingSetup("Precomputed", Precomputed),
)
