import pytest
from src.lib.model.model import Model
from src.lib.utils.config import Consts


tests = [
    (
        "Качество - синтетика. Ожидала хлопок. Очень жаль и ожидания не оправдались",
        Consts.id2label[0]
    ),
    (
        """качество плохое пошив ужасный (горловина наперекос) Фото не соответствует Ткань 
        ужасная рисунок блеклый маленький рукав не такой УЖАС!!!!! не стоит за такие деньги г.......""",
        Consts.id2label[0]
    ),
    (
        "наушник просто супер",
        Consts.id2label[2]
    ),
    (
        "парфюм оригинальный . все ,  профессиональный магазин .  :)  обожать их ! доставка город быстрый ! ",
        Consts.id2label[2]
    ),
    (
        """доставка быстрый ,  очень вежливый сервис . 
        качество сам товар сомневаться ,  запах немного отличаться оригинал . """,
        Consts.id2label[1]
    ),
    (
        """дисплей звук хорошо ,  iphone 8 время заряд расход батарея 
        ,  быстродействие наравне iphone 8 ,  большой тяжелый""",
        Consts.id2label[1]
    )
]


@pytest.fixture(scope="module")
def classifier() -> Model:
    return Model()


@pytest.mark.parametrize("test", tests)
def test_predict(classifier: Model, test: tuple) -> None:
    text, values = test
    guess = classifier.predict(text)[1][0] # [1][0] to take res of best result
    assert guess == values
