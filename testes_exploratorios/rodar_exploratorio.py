# -*- coding: utf-8 -*-
"""Roda os casos exploratórios contra a API da Lia e salva as evidências.

Uso (Windows PowerShell):
    $env:LIA_API_KEY = "sua-chave"      # ou use o .env da raiz do repositório (LIA_API_KEY=...)
    python rodar_exploratorio.py                    # todos os casos, 3 execuções, versão original
    python rodar_exploratorio.py --casos EXP-16 EXP-35 --repeticoes 1
    python rodar_exploratorio.py --charter C5
    python rodar_exploratorio.py --prompt prompt_corrigido.txt   # versão corrigida

Saídas (pasta resultados/):
    resultados_<versao>_<data>.csv  -> abre no Excel; coluna "veredito" para você preencher
    resultados_<versao>_<data>.json -> resposta bruta completa (evidência)

Respeita as regras do desafio: sessão nova por execução, no máximo 4 chamadas em paralelo
(aqui o padrão é 2) e nova tentativa em 429/502.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from casos_exploratorios import CASOS, CHARTERS

URL = os.environ.get("LIA_URL", "https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/")


def ler_env():
    """Lê LIA_API_KEY do .env na raiz do repositório, se existir (o .env está no .gitignore)."""
    for pasta in (os.getcwd(), os.path.dirname(os.path.abspath(__file__)),
                  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
        caminho = os.path.join(pasta, ".env")
        if os.path.exists(caminho):
            for linha in open(caminho, encoding="utf-8-sig"):
                if linha.strip().startswith("LIA_API_KEY="):
                    return linha.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def chamar(chave, mensagem, sessao=None, prompt=None, tentativas=4):
    corpo = {"mensagem": mensagem}
    if sessao:
        corpo["sessao"] = sessao
    if prompt:
        corpo["prompt_sistema"] = prompt
    dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
    for t in range(tentativas):
        req = urllib.request.Request(URL, data=dados, method="POST", headers={
            "Content-Type": "application/json", "x-api-key": chave})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code in (429, 502) and t < tentativas - 1:
                time.sleep(5 * (t + 1))
                continue
            return {"erro": f"HTTP {e.code}: {msg}"}
        except Exception as e:  # rede/timeout
            if t < tentativas - 1:
                time.sleep(5)
                continue
            return {"erro": str(e)}


def executar_caso(chave, caso, execucao, prompt):
    sessao, turnos_log = None, []
    for msg in caso["turnos"]:
        r = chamar(chave, msg, sessao, prompt)
        sessao = r.get("sessao", sessao)
        turnos_log.append({"mensagem": msg, **r})
        if "erro" in r:
            break
    ultimo = turnos_log[-1]
    lat = sum(m.get("metrics", {}).get("latencyMs", 0) for t in turnos_log for m in (t.get("metricas") or []))
    tok = sum(m.get("usage", {}).get("totalTokens", 0) for t in turnos_log for m in (t.get("metricas") or []))
    ferramentas = [f for t in turnos_log for f in (t.get("ferramentas") or [])]
    print(f"  {caso['id']} execução {execucao}: {'ERRO' if 'erro' in ultimo else 'ok'}", flush=True)
    return {
        "id": caso["id"], "charter": caso["charter"], "execucao": execucao,
        "versao": ultimo.get("versao", ""),
        "entrada": " || ".join(caso["turnos"]),
        "resposta_final": ultimo.get("resposta", ultimo.get("erro", "")),
        "todas_respostas": " || ".join(t.get("resposta", t.get("erro", "")) for t in turnos_log),
        "ferramentas": json.dumps(ferramentas, ensure_ascii=False),
        "esperado": caso["esperado"], "referencia": caso["ref"],
        "latencia_ms_total": lat, "tokens_total": tok,
        "veredito": "", "severidade": "", "observacoes": "",
        "_bruto": turnos_log,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--casos", nargs="*", help="IDs específicos, ex.: EXP-01 EXP-16")
    ap.add_argument("--charter", nargs="*", help="Charters, ex.: C3 C5")
    ap.add_argument("--repeticoes", type=int, default=3)
    ap.add_argument("--paralelo", type=int, default=2, help="máximo 4 pelas regras do desafio")
    ap.add_argument("--prompt", help="arquivo .txt com o prompt corrigido (versão corrigida)")
    a = ap.parse_args()

    chave = os.environ.get("LIA_API_KEY") or os.environ.get("LIA_KEY") or ler_env()
    if not chave:
        sys.exit("Defina LIA_API_KEY no .env da raiz do repositório ou como variável de ambiente.")
    paralelo = max(1, min(a.paralelo, 4))
    prompt = open(a.prompt, encoding="utf-8").read() if a.prompt else None

    casos = CASOS
    if a.casos:
        casos = [c for c in casos if c["id"] in a.casos]
    if a.charter:
        casos = [c for c in casos if c["charter"] in a.charter]
    tarefas = [(c, i) for c in casos for i in range(1, a.repeticoes + 1)]
    print(f"{len(casos)} casos x {a.repeticoes} = {len(tarefas)} execuções | paralelo={paralelo} | "
          f"versão={'corrigida' if prompt else 'original'}")

    with ThreadPoolExecutor(max_workers=paralelo) as ex:
        res = list(ex.map(lambda t: executar_caso(chave, t[0], t[1], prompt), tarefas))
    res.sort(key=lambda r: (r["id"], r["execucao"]))

    os.makedirs("resultados", exist_ok=True)
    base = f"resultados/resultados_{'corrigida' if prompt else 'original'}_{datetime.now():%Y%m%d_%H%M}"
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"charters": CHARTERS, "resultados": res}, f, ensure_ascii=False, indent=2)
    campos = [k for k in res[0] if not k.startswith("_")] if res else []
    with open(base + ".csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(res)
    print(f"\nPronto: {base}.csv e {base}.json")


if __name__ == "__main__":
    main()
