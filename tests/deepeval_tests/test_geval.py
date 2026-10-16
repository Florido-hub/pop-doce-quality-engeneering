import json
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

from utils.juiz import obter_juiz
from src.chatbot import perguntar
from utils.preparar_input import preparar_input_avaliacao
from utils.versao_lia import obter_prompt

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
def test_geval(caso, juiz):

    if "turnos" in caso:
        entrada_agente = [
            turno["entrada"]
            for turno in caso["turnos"]
        ]
    else:
        entrada_agente = caso["entrada"]

    #resposta = perguntar(entrada_agente)
    prompt = obter_prompt()

    resposta = perguntar(
        entrada_agente,
        prompt=prompt
)

    input_avaliacao = preparar_input_avaliacao(caso)

    test_case = LLMTestCase(
        input=input_avaliacao,
        actual_output=resposta
    )

    criterio = caso.get("criterio_esperado") or caso.get("llm_rubric")

    if not criterio:
        raise ValueError(
            f"Caso {caso['id']} não possui criterio_esperado nem llm_rubric."
    )

    metric = GEval(
        name="Conformidade de Claims",
        criteria=criterio,
        evaluation_params=[
                SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT
        ],
        threshold=0.8,
        model=juiz
)

    assert_test(test_case, metrics=[metric])
