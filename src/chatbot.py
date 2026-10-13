import os
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("LIA_API_KEY")

URL = (
    "https://rm4naioqykxiti2srofnqz6hqa0ctlav"
    ".lambda-url.us-east-1.on.aws/"
)

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}


def perguntar(input_data, prompt=None, retornar_json=False):

    if isinstance(input_data, str):
        turnos = [input_data]
    else:
        turnos = input_data

    sessao = None
    resposta = ""
    resultado = None

    for turno in turnos:

        payload = {
            "mensagem": turno
        }

        if sessao:
            payload["sessao"] = sessao

        if prompt is not None:
            payload["prompt_sistema"] = prompt

        response = requests.post(
            URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        resultado = response.json()

        resposta = resultado["resposta"]
        sessao = resultado.get("sessao")

    if retornar_json:
        return resultado

    return resposta
