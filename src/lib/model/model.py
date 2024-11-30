import torch
import joblib
from io import BytesIO
import torch.nn.functional as F
from transformers import BertTokenizer, BertForSequenceClassification
from typing import Any
from pymorphy3 import MorphAnalyzer
from utils.s3 import get_model_weights
from utils.preprocess import preprocess_text
from utils.config import Consts


class Model:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.morph = MorphAnalyzer()
        self.tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
        self.model = BertForSequenceClassification.from_pretrained(
            'DeepPavlov/rubert-base-cased',
            num_labels=3,
            ignore_mismatched_sizes=True
        )
        weights = get_model_weights()
        if weights is not None:
            self.model = joblib.load(BytesIO(weights))

        self.model = self.model.to(self.device)
        self.model.eval()

    def _preprocess_input(self, text: str) -> Any:
        text = preprocess_text(text, self.morph)
        return self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128,
            add_special_tokens=True
        )

    def _classify_text(self, **inputs) -> tuple[list[tuple[str, float]], tuple[str, float]]:
        outputs = self.model(**inputs)
        probabilities = F.softmax(outputs.logits, dim=-1)

        results = []
        for i, prob in enumerate(probabilities):
            results.append((Consts.id2label[i], prob))

        predicted_class_idx = torch.argmax(probabilities).item()

        best_result = (Consts.id2label[predicted_class_idx], probabilities[0][predicted_class_idx].item())
        return results, best_result

    def predict(self, text: str) -> tuple[list[tuple[str, float]], tuple[str, float]]:
        tokenized_inputs = self._preprocess_input(text)
        results = self._classify_text(
            input_ids=tokenized_inputs["input_ids"],
            attention_mask=tokenized_inputs["attention_mask"],
        )
        return results


model = Model()
