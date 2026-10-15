
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

DATASET = ROOT / "data" / "golden_dataset.json"
SAIDA = Path(__file__).parent / "tests_promptfoo" / "tool_usage.yaml"


def gerar_testes():
    with DATASET.open("r", encoding="utf-8") as arquivo:
        dataset = json.load(arquivo)

    testes = []

    for caso in dataset:
        # Por enquanto, processamos casos de turno único.
        if "turnos" in caso:
            continue

        teste = {
            "description": f"{caso['id']} - {caso['titulo']}",
            "vars": {
                "mensagem": caso["entrada"],
                "espera_ferramenta": caso.get("espera_ferramenta", False),
                "ferramenta_esperada": caso.get(
                    "ferramenta_esperada", []
                ),
            },
            "assert": [],
        }

        # # Verificações determinísticas da resposta
        # for termo in caso.get("assert_contains", []):
        #     teste["assert"].append({
        #         "type": "contains",
        #         "value": termo,
        #     })
        #
        # for termo in caso.get("assert_not_contains", []):
        #     teste["assert"].append({
        #         "type": "not-contains",
        #         "value": termo,
        #     })

        # Verificação das ferramentas executadas
        teste["assert"].append({
            "type": "javascript",
            "value": """



const ferramentas =
  context.providerResponse?.metadata?.ferramentas;

const esperadoOriginal = context.vars.ferramenta_esperada;
const deveUsar = context.vars.espera_ferramenta === true ||
                 context.vars.espera_ferramenta === "true";

const esperadas = Array.isArray(esperadoOriginal)
  ? esperadoOriginal
  : esperadoOriginal
    ? [esperadoOriginal]
    : [];

if (!Array.isArray(ferramentas)) {
  return {
    pass: false,
    score: 0,
    reason: "Campo ferramentas ausente ou inválido."
  };
}

const executadas = ferramentas.map(f => f.ferramenta);

const passou = deveUsar
  ? esperadas.length > 0 &&
    esperadas.every(nome => executadas.includes(nome))
  : executadas.length === 0;

return {
  pass: passou,
  score: passou ? 1 : 0,
  reason: JSON.stringify({
    deveUsar,
    ferramentasEsperadas: esperadas,
    ferramentasExecutadas: executadas,
    resultado: passou ? "PASS" : "FAIL"
  })
};



""".strip(),
        })

        testes.append(teste)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)

    with SAIDA.open("w", encoding="utf-8") as arquivo:
        yaml.safe_dump(
            testes,
            arquivo,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )

    print(f"{len(testes)} testes gerados em: {SAIDA}")


if __name__ == "__main__":
    gerar_testes()
