import numpy as np

from supporter.embedder.base_embedder import BaseEmbedder
from transformers import BertModel, BertTokenizer
import torch

from supporter.utils import extract_sentence_by_word_position


class BertEmbedder(BaseEmbedder):
    RESOURCE_MODEL_ROOT = "resources/models"

    def __init__(self):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BertModel.from_pretrained(
            'bert-base-uncased', cache_dir=self.RESOURCE_MODEL_ROOT
        ).to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(
            'bert-base-uncased', cache_dir=self.RESOURCE_MODEL_ROOT
        )

    def embed(self, text: str) -> dict[str, any]:
        tokens = self.tokenizer.tokenize(text)
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        input_ids = torch.tensor(input_ids).unsqueeze(0).to(self.device)
        with torch.no_grad():
            outputs = self.model(input_ids)
            embeddings = outputs.last_hidden_state[0].cpu()
        result = {
            "tokens": tokens,
            "embeddings": embeddings.numpy()
        }
        return result

    def get_word_embedding(self, text: str, word_pos: tuple[int, int]) -> np.ndarray:
        sentence_start, sentence_end = extract_sentence_by_word_position(text, word_pos[0], word_pos[1])
        sentence = text[sentence_start:sentence_end]
        results = self.embed(sentence)
        tokens, embeddings = results["tokens"], results["embeddings"]

        word_start, word_end = word_pos[0] - sentence_start, word_pos[1] - sentence_start
        pre_word_sentence = sentence[:word_start]
        pre_word_tokens = self.tokenizer.tokenize(pre_word_sentence)
        token_start_idx = len(pre_word_tokens)
        token_end_idx = token_start_idx + 1
        for token_idx in range(token_end_idx, len(tokens)):
            if tokens[token_idx].startswith("##"):
                token_end_idx += 1
        word_embedding = embeddings[token_start_idx:token_end_idx].mean(axis=0)

        return word_embedding
