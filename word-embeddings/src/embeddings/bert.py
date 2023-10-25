import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer, FeatureExtractionPipeline

from device import device

CONTEXT_SIZE = 512

class BERTTokenizer:
    def __init__(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.padding = {"input_ids": self.tokenizer.pad_token_id, "token_type_ids": 0, "attention_mask": 0}

    def pad(self, name, tensor):
        _, length = tensor.size()
        pad_size = (0, (CONTEXT_SIZE - (length % CONTEXT_SIZE)) % CONTEXT_SIZE)
        return torch.nn.functional.pad(tensor, pad_size, "constant", self.padding[name])

    def __call__(self, *args, **kwargs):
        tokens = self.tokenizer(*args, **kwargs)

        tokens = {name: self.pad(name, tensor) for name, tensor in tokens.items()}
        tokens = {name: torch.split(tensor, CONTEXT_SIZE, -1) for name, tensor in tokens.items()}
        tokens = {name: torch.cat(tensors) for name, tensors in tokens.items()}
        return tokens

class BERT:
    def __init__(self, model, pooling=""):
        self.model = AutoModel.from_pretrained(model).to(device)
        self.tokenizer = BERTTokenizer(model)

    def embed(self, text):
        feature_extraction = FeatureExtractionPipeline(self.model, self.tokenizer, device=device)
        embedding = feature_extraction(text)

        return [np.array(instance[0]) for instance in embedding]
