import torch

from supporter.summarizer.base_summarizer import BaseSummarizer
from transformers.models.bart.modeling_bart import BartForConditionalGeneration
from transformers.models.bart.tokenization_bart import BartTokenizer


class BartSummarizer(BaseSummarizer):
    RESOURCE_MODEL_ROOT = 'resources/models'

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = BartForConditionalGeneration.from_pretrained(
            'facebook/bart-large-cnn',
            cache_dir=self.RESOURCE_MODEL_ROOT
        ).to(self.device)
        self.tokenizer = BartTokenizer.from_pretrained(
            'facebook/bart-large-cnn',
            cache_dir=self.RESOURCE_MODEL_ROOT,
            clean_up_tokenization_spaces=True,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def summarize(self, article: str) -> str:
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.config.pad_token_id = self.tokenizer.pad_token_id
        input_ids = self.tokenizer(article, return_tensors="pt", truncation=True, padding=True,
                                   max_length=1024).input_ids.to(self.device)
        summary_ids = self.model.generate(input_ids, max_length=200, min_length=2, length_penalty=2.0, num_beams=3,
                                          early_stopping=False).cpu()
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
