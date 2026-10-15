
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.chatbot import perguntar


def call_api(prompt, options, context):
    try:
        resultado = perguntar(
            prompt,
            retornar_json=True
        )

        return {
            "output": resultado["resposta"],
            "metadata": {
                "ferramentas": resultado.get("ferramentas", []),
                "versao": resultado.get("versao"),
                "metricas": resultado.get("metricas", {})
            }
        }

    except Exception as erro:
        return {"error": str(erro)}
