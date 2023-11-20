import torch
import numpy as np
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer, FeatureExtractionPipeline

from device import device

CONTEXT_SIZE = 512
STRIDE = 384

class BERTTokenizer:
    def __init__(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.padding_token = {"input_ids": self.tokenizer.pad_token_id, "token_type_ids": 0, "attention_mask": 0}

    def pad(self, name, tensor):
        _, length = tensor.size()
        pad_size = (0, (STRIDE - (length - CONTEXT_SIZE) % STRIDE) % STRIDE)
        return torch.nn.functional.pad(tensor, pad_size, "constant", self.padding_token[name])

    def add_window(self, tensor):
        _, length = tensor.size()
        window_starts = [STRIDE * (start + 1) for start in range((length - CONTEXT_SIZE) // STRIDE)]
        for start in reversed(window_starts):
            tensor = torch.cat((tensor[:, :start], tensor[:, start:start + CONTEXT_SIZE - STRIDE], tensor[:, start:]), dim=1)
        return tensor
    
    def print_tokens(self, tokens):
        print([self.tokenizer.convert_ids_to_tokens(line) for line in tokens["input_ids"]])

    def __call__(self, *args, **kwargs):
        tokens = self.tokenizer(*args, **kwargs).to(device)

        tokens = {name: self.pad(name, tensor) for name, tensor in tokens.items()}
        tokens = {name: self.add_window(tensor) for name, tensor in tokens.items()}
        tokens = {name: torch.split(tensor, CONTEXT_SIZE, -1) for name, tensor in tokens.items()}
        tokens = {name: torch.cat(tensors) for name, tensors in tokens.items()}
        return tokens

class BERT:
    def __init__(self, model):
        self.model = AutoModel.from_pretrained(model).to(device)
        self.tokenizer = BERTTokenizer(model)

    def pool(self, embedding, pooling):
        match pooling:
            case "class":   return np.array(embedding[0][0])
            case "average": return np.average(np.average(np.array(embedding), axis=1), axis=0)
            case "max":     return np.max(np.max(np.array(embedding), axis=1), axis=0)

    def embed_document(self, documents, **kwargs):
        return self.embed([document["content"] for document in documents], **kwargs)

    def embed(self, texts, show_progress_bar=False, pooling="average", **kwargs):
        feature_extraction = FeatureExtractionPipeline(self.model, self.tokenizer, device=device)

        if show_progress_bar: texts = tqdm(texts)
        return [self.pool(feature_extraction(text), pooling) for text in texts]
