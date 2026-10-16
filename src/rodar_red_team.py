# -*- coding: utf-8 -*-

import argparse
import csv
import json
import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from casos_red_team import CASOS, CATEGORIAS


BASE_DIR = Path(__file__).resolve().parent.parent

URL = os.environ.get(
    "LIA_URL",
    "https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/"
)

RESULTADOS_DIR = BASE_DIR / "data" / "red_team" / "resultados"


def carregar_env():
    """
    Carrega as variáveis do arquivo .env sem exibir a chave.
    """
    env_path = BASE_DIR / ".env"

    if not env_path.exists():
        return

    with open(env_path, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if not linha or linha.startswith("#") or "=" not in linha:
                continue

            nome, valor = linha.split("=", 1)
            os.environ.setdefault(nome.strip(), valor.strip())

def chamar(chave, mensagem, sessao=None, prompt=None, tentativas=4):
    corpo = {
        "mensagem": mensagem
    }

    if sessao:
        corpo["sessao"] = sessao

    if prompt:
        corpo["prompt_sistema"] = prompt

    headers = {
        "Content-Type": "application/json",
        "x-api-key": chave
    }

    for tentativa in range(tentativas):
        try:
            resposta = requests.post(
                URL,
                headers=headers,
                json=corpo,
                timeout=120
            )

            # Tenta novamente em erros temporários
            if (
                resposta.status_code in (429, 502)
                and tentativa < tentativas - 1
            ):
                time.sleep(5 * (tentativa + 1))
                continue

            resposta.raise_for_status()

            return resposta.json()

        except requests.RequestException as erro:
            if tentativa < tentativas - 1:
                time.sleep(5)
                continue

            return {
                "erro": str(erro)
            }

        except ValueError as erro:
            return {
                "erro": f"Resposta inválida da API: {erro}"
            }

def executar_caso(chave, caso, execucao, prompt):

    sessao = None
    turnos_log = []

    for mensagem in caso["turnos"]:

        retorno = chamar(
            chave,
            mensagem,
            sessao,
            prompt
        )

        sessao = retorno.get(
            "sessao",
            sessao
        )

        turnos_log.append({
            "mensagem": mensagem,
            **retorno
        })

        if "erro" in retorno:
            break

    ultimo = turnos_log[-1]

    latencia = sum(
        metrica.get("metrics", {}).get(
            "latencyMs",
            0
        )
        for turno in turnos_log
        for metrica in (turno.get("metricas") or [])
    )

    tokens = sum(
        metrica.get("usage", {}).get(
            "totalTokens",
            0
        )
        for turno in turnos_log
        for metrica in (turno.get("metricas") or [])
    )

    ferramentas = [
        ferramenta
        for turno in turnos_log
        for ferramenta in (
            turno.get("ferramentas") or []
        )
    ]

    status = (
        "ERRO"
        if "erro" in ultimo
        else "ok"
    )

    print(
        f"{caso['id']} - execução {execucao}: {status}",
        flush=True
    )

    return {
        "id": caso["id"],
        "categoria": caso["categoria"],
        "categoria_descricao": CATEGORIAS[
            caso["categoria"]
        ],
        "objetivo": caso["objetivo"],
        "tecnica": caso["tecnica"],
        "execucao": execucao,

        "versao": ultimo.get(
            "versao",
            "corrigida" if prompt else "original"
        ),

        "entrada": " || ".join(
            caso["turnos"]
        ),

        "resposta_final": ultimo.get(
            "resposta",
            ultimo.get("erro", "")
        ),

        "todas_respostas": " || ".join(
            turno.get(
                "resposta",
                turno.get("erro", "")
            )
            for turno in turnos_log
        ),

        "esperado": caso["esperado"],

        "severidade_se_falhar":
            caso["severidade_se_falhar"],

        "ferramentas": json.dumps(
            ferramentas,
            ensure_ascii=False
        ),

        "latencia_ms_total": latencia,
        "tokens_total": tokens,

        # Campos preenchidos após revisão humana
        "resultado": "PENDENTE_REVISAO",
        "severidade": "",
        "evidencia": "",
        "observacoes": "",

        # Mantido no JSON, removido do CSV
        "_bruto": turnos_log,
    }


def main():

    carregar_env()

    parser = argparse.ArgumentParser(
        description="Executa os testes de Red Teaming da Lia."
    )

    parser.add_argument(
        "--casos",
        nargs="*",
        help="IDs específicos, ex.: RT-PI-01 RT-CM-03"
    )

    parser.add_argument(
        "--categoria",
        nargs="*",
        help="Categorias específicas, ex.: RT1 RT4"
    )

    parser.add_argument(
        "--repeticoes",
        type=int,
        default=3
    )

    parser.add_argument(
        "--paralelo",
        type=int,
        default=2,
        help="Máximo 4 pelas regras do desafio."
    )

    parser.add_argument(
        "--prompt",
        help="Arquivo com o prompt corrigido."
    )

    args = parser.parse_args()

    # Aceita o nome usado pelo chatbot.py
    # e também o padrão do script exploratório.
    chave = (
        os.environ.get("LIA_API_KEY")
        or os.environ.get("LIA_KEY")
    )

    if not chave:
        raise SystemExit(
            "Chave não encontrada. "
            "Confira LIA_API_KEY no arquivo .env."
        )

    paralelo = max(
        1,
        min(args.paralelo, 4)
    )

    prompt = None

    if args.prompt:
        with open(
            args.prompt,
            "r",
            encoding="utf-8"
        ) as arquivo:
            prompt = arquivo.read()

    casos = CASOS

    if args.casos:
        casos = [
            caso
            for caso in casos
            if caso["id"] in args.casos
        ]

    if args.categoria:
        casos = [
            caso
            for caso in casos
            if caso["categoria"] in args.categoria
        ]

    tarefas = [
        (caso, execucao)
        for caso in casos
        for execucao in range(
            1,
            args.repeticoes + 1
        )
    ]

    versao = (
        "corrigida"
        if prompt
        else "original"
    )

    print()
    print("========================================")
    print("RED TEAMING - LIA")
    print("========================================")
    print(f"Versão: {versao}")
    print(f"Casos: {len(casos)}")
    print(f"Repetições: {args.repeticoes}")
    print(f"Execuções totais: {len(tarefas)}")
    print(f"Paralelismo: {paralelo}")
    print("========================================")
    print()

    with ThreadPoolExecutor(
        max_workers=paralelo
    ) as executor:

        resultados = list(
            executor.map(
                lambda tarefa: executar_caso(
                    chave,
                    tarefa[0],
                    tarefa[1],
                    prompt
                ),
                tarefas
            )
        )

    resultados.sort(
        key=lambda resultado: (
            resultado["id"],
            resultado["execucao"]
        )
    )

    RESULTADOS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    base = (
        RESULTADOS_DIR
        / f"red_team_{versao}_{timestamp}"
    )

    # JSON completo
    with open(
        str(base) + ".json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            {
                "categorias": CATEGORIAS,
                "versao": versao,
                "repeticoes": args.repeticoes,
                "resultados": resultados
            },
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    # CSV para análise
    campos = [
        chave
        for chave in resultados[0]
        if not chave.startswith("_")
    ] if resultados else []

    with open(
        str(base) + ".csv",
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        writer = csv.DictWriter(
            arquivo,
            fieldnames=campos,
            delimiter=";",
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(resultados)

    print()
    print("========================================")
    print("EXECUÇÃO FINALIZADA")
    print("========================================")
    print(f"Resultados: {len(resultados)}")
    print(f"JSON: {base}.json")
    print(f"CSV:  {base}.csv")


if __name__ == "__main__":
    main()