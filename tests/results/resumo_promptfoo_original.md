# Resumo — Promptfoo | Lia Original (Baseline)

**Objetivo:** avaliar o uso correto das ferramentas pela Lia, utilizando 62 casos de teste por rodada, sem cache e com concorrência de 2 execuções. A execução antiga foi descartada.

## Resultados por rodada

| Rodada | Total | PASS | FAIL* | Aprovação | Tempo de execução |
|---|---:|---:|---:|---:|---:|
| 1 | 62 | 11 | 51 | 17,74% | 2min30s |
| 2 | 62 | 13 | 49 | 20,97% | 1min44s |
| 3 | 62 | 13 | 49 | 20,97% | 1min15s |

\* Erros técnicos foram contabilizados como FAIL.

## Média e consolidado

| Indicador | Resultado |
|---|---:|
| Média de PASS por rodada | 12,33 |
| Média de FAIL por rodada | 49,67 |
| **Taxa média de aprovação** | **19,89%** |
| Total de avaliações (3 rodadas) | 186 |
| Total de PASS | 37 |
| Total de FAIL | 149 |
| Tempo total de execução | 5min29s |
| Tempo médio por rodada | 1min50s (aprox.) |

## Conclusão

A Lia Original apresentou **baixa taxa de aprovação** nos testes de uso de ferramentas, com resultados próximos nas três rodadas (17,74% a 20,97%). O desempenho indica a necessidade de melhorar a seleção e o acionamento das ferramentas. Esta avaliação constitui a **baseline** para futura comparação com a versão corrigida.
