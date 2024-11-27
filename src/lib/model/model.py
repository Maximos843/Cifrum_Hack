import torch
import torch.nn.functional as F
from transformers import BertTokenizer, BertForSequenceClassification
from typing import Any


class Model:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
        self.model = BertForSequenceClassification.from_pretrained(
            'DeepPavlov/rubert-base-cased',
            num_labels=3,
            ignore_mismatched_sizes=True
        )

    def _preprocess_input(self, text: str) -> Any:
        return self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )

    def _classify_text(self, **inputs) -> list[tuple[str, float]]:

        outputs = self.model(**inputs)

        # Apply softmax to get probabilities
        probabilities = F.softmax(outputs.logits, dim=-1)

        # Get the predicted class index and its confidence score for each input
        results = []
        for probs in probabilities:
            predicted_class_idx = torch.argmax(probs).item()
            confidence_score = probs[predicted_class_idx].item()
            predicted_label = self.model.config.id2label[predicted_class_idx]
            results.append((predicted_label, confidence_score))

        return results

    def _predict(self, text: str) -> list[tuple[str, float]]:
        """
        Private method to preprocess, classify, and decode user input.
        """
        tokenized_inputs = self._preprocess_input(text)

        results = self._classify_text(
            input_ids=tokenized_inputs["input_ids"],
            attention_mask=tokenized_inputs["attention_mask"],
        )
        return results
