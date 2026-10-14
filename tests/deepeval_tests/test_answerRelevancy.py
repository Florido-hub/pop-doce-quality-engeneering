import json
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from utils.juiz import obter_juiz
from src.chatbot import perguntar
from utils.preparar_input import preparar_input_avaliacao

caminho_json = (Path(__file__).resolve().parents[2]/ "data"/ "golden_dataset.json")

dataset = json.loads(caminho_json.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def juiz():
    return obter_juiz()


@pytest.mark.parametrize(
    "caso",
    dataset,
    ids=lambda caso: caso["id"]
)
def test_answer_relevancy(caso, juiz):

    if "turnos" in caso:
        entrada_agente = [
            turno["entrada"]
            for turno in caso["turnos"]
        ]
    else:
        entrada_agente = caso["entrada"]

    resposta = perguntar(entrada_agente)

    input_avaliacao = preparar_input_avaliacao(caso)

    test_case = LLMTestCase(
        input=input_avaliacao,
        actual_output=resposta
    )

    metric = AnswerRelevancyMetric(
        threshold=0.7,
        model=juiz,
        verbose_mode=True
    )

    assert_test(
        test_case,
        metrics=[metric]
    )
