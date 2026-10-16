# Resumo — Promptfoo — Lia Corrigida

## Contexto

A versão corrigida da Lia foi avaliada com o Promptfoo utilizando os casos automatizados derivados do Golden Dataset. Foram realizadas três rodadas independentes, sem uso de cache e com concorrência máxima de 2 requisições.

Cada rodada executou 62 casos de teste, totalizando 186 execuções.

## Resultados

| Rodada | PASS | FAIL | Erros | Taxa de sucesso | Duração |
|---|---:|---:|---:|---:|---:|
| 1 | 13 | 49 | 0 | 20,97% | 2m43s |
| 2 | 13 | 49 | 0 | 20,97% | 2m29s |
| 3 | 13 | 49 | 0 | 20,97% | 4m11s |
| **Total** | **39** | **147** | **0** | **20,97%** | — |

## Análise

Os resultados foram consistentes nas três rodadas: 13 dos 62 casos foram aprovados em cada execução, resultando em uma taxa de sucesso de 20,97%.

A avaliação do Promptfoo utilizada neste projeto verifica principalmente se a Lia acionou a ferramenta esperada para cada caso. Portanto, um resultado FAIL não significa necessariamente que todo o conteúdo textual da resposta esteja incorreto. Em diversos casos, a falha ocorreu porque a resposta foi fornecida diretamente sem o acionamento da ferramenta exigida pelo teste.

Entretanto, durante as execuções também foram observadas respostas com informações incompatíveis com a base oficial, demonstrando que parte das falhas não se limita ao uso de ferramentas.

## Evidências

Foram exportados os resultados completos de cada rodada nos formatos JSON e CSV:

- Rodada 1: `eval-Qyf-2026-10-16T12_32_34`
- Rodada 2: `eval-vvf-2026-10-16T12_38_29`
- Rodada 3: `eval-7tx-2026-10-16T12_44_13`

## Conclusão

A versão corrigida apresentou comportamento estável nas três execuções do Promptfoo, porém manteve uma taxa de aprovação baixa, de 20,97%. Os resultados indicam problemas persistentes no acionamento das ferramentas esperadas e, em alguns casos, na conformidade das respostas com a base oficial.

Esses resultados devem ser analisados em conjunto com as métricas do DeepEval e com os testes de Red Teaming para a decisão final de Go/No-Go.
