import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def obter_prompt():
    versao = os.getenv("VERSAO_LIA", "original").lower()

    if versao == "original":
        return None

    if versao == "corrigida":
        caminho = ROOT / "prompts" / "prompt_corrigido.md"
        return caminho.read_text(encoding="utf-8")

    raise ValueError(
        f"VERSAO_LIA inválida: {versao}. "
        "Use 'original' ou 'corrigida'."
    )