import re
import emoji
from pymorphy3 import MorphAnalyzer


def preprocess_text(text: str, morph: MorphAnalyzer, lemma: bool = False) -> str:
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'httpS+|wwwS+|httpsS+', '', text)

    text = re.sub(r'[^а-яА-ЯёЁ0-9!?.:;()\s]', '', text)
    text = emojis_words(text)

    if lemma:
        lemmatized_words = [morph.parse(word)[0].normal_form for word in text.split()]
        text = ' '.join(lemmatized_words)

    return text


def emojis_words(text: str) -> str:
    clean_text = emoji.demojize(text, delimiters=(" ", " "))
    clean_text = clean_text.replace(":", "").replace("_", " ")
    return clean_text
