# Resumo — DeepEval — Lia Corrigida

Este documento consolida os resultados das três rodadas de avaliação da versão corrigida da Lia utilizando o DeepEval.

Em cada rodada foram avaliados os 68 casos do Golden Dataset nas métricas Answer Relevancy, Faithfulness e G-Eval, totalizando 204 avaliações por rodada.

---

## Rodada 1

### Resultado geral da execução

A primeira rodada executou 204 avaliações, correspondentes aos 68 casos do Golden Dataset avaliados pelas três métricas do DeepEval.

| Métrica | PASS | FAIL | Total | Taxa de aprovação |
|---|---:|---:|---:|---:|
| Answer Relevancy | 48 | 20 | 68 | 70,6% |
| Faithfulness | 13 | 55 | 68 | 19,1% |
| G-Eval | 29 | 39 | 68 | 42,6%* |
| **Total bruto** | **90** | **114** | **204** | **44,1%** |

\* O resultado bruto do G-Eval contém 6 casos multi-turno que falharam por erro técnico (`KeyError: 'criterio_esperado'`) e, portanto, não representam falhas da Lia.

### Correção dos casos multi-turno

Foi identificado que os casos `TC-MLT-01` a `TC-MLT-06` armazenam os critérios dos turnos em uma estrutura diferente dos casos de turno único e possuem `llm_rubric` no nível principal.

O teste G-Eval foi ajustado para utilizar:

- `criterio_esperado` nos casos que possuem esse campo;
- `llm_rubric` como alternativa para os casos multi-turno.

Após a correção, os 6 casos foram reexecutados sem ocorrência de `KeyError`.

### Reexecução registrada

| Caso | Resultado |
|---|---|
| TC-MLT-01 | FAIL |
| TC-MLT-02 | FAIL |
| TC-MLT-03 | FAIL |
| TC-MLT-04 | FAIL |
| TC-MLT-05 | PASS |
| TC-MLT-06 | PASS |

Resultado da reexecução: **2 PASS e 4 FAIL**.

> A reexecução dos casos multi-turno é registrada separadamente da execução original, pois as respostas da Lia e a avaliação por LLM possuem comportamento não determinístico. Os resultados não foram utilizados para sobrescrever retroativamente as respostas obtidas na execução inicial.

### Evidências da Rodada 1

- `deepeval_rodada_1.log`
- `deepeval_rodada_1.xml`
- `deepeval_rodada_1_correcao_mlt.log`
- `deepeval_rodada_1_correcao_mlt.xml`

---

## Rodada 2

A segunda rodada foi executada após a correção do tratamento dos casos multi-turno. Foram realizadas novamente 204 avaliações.

| Métrica | PASS | FAIL | Total | Taxa de aprovação |
|---|---:|---:|---:|---:|
| Answer Relevancy | 47 | 21 | 68 | 69,1% |
| Faithfulness | 12 | 56 | 68 | 17,6% |
| G-Eval | 28 | 40 | 68 | 41,2% |
| **Total** | **87** | **117** | **204** | **42,6%** |

A execução foi concluída em aproximadamente **2h11min25s**.

Não foram identificados erros de infraestrutura nos casos multi-turno nesta rodada. Os casos que não atingiram os thresholds definidos foram registrados normalmente como falhas das métricas.

### Evidências da Rodada 2

- `deepeval_rodada_2.log`
- `deepeval_rodada_2.xml`

---

## Rodada 3

A terceira rodada repetiu a mesma configuração utilizada na Rodada 2, com 204 avaliações.

| Métrica | PASS | FAIL | Total | Taxa de aprovação |
|---|---:|---:|---:|---:|
| Answer Relevancy | 48 | 20 | 68 | 70,6% |
| Faithfulness | 10 | 58 | 68 | 14,7% |
| G-Eval | 28 | 40 | 68 | 41,2% |
| **Total** | **86** | **118** | **204** | **42,2%** |

A execução foi concluída em aproximadamente **2h03min15s**.

Não foram identificados erros de infraestrutura equivalentes ao `KeyError` encontrado na primeira rodada. Os casos multi-turno foram avaliados normalmente pelo G-Eval.

### Evidências da Rodada 3

- `deepeval_rodada_3.log`
- `deepeval_rodada_3.xml`

---

## Comparação das três rodadas

### Resultados por métrica

| Métrica | Rodada 1 | Rodada 2 | Rodada 3 |
|---|---:|---:|---:|
| Answer Relevancy | 70,6% | 69,1% | 70,6% |
| Faithfulness | 19,1% | 17,6% | 14,7% |
| G-Eval | 42,6%* | 41,2% | 41,2% |
| **Resultado geral bruto** | **44,1%*** | **42,6%** | **42,2%** |

\* A Rodada 1 deve ser interpretada com cautela devido ao erro técnico encontrado nos 6 casos multi-turno do G-Eval. A reexecução desses casos foi registrada separadamente e não substituiu retroativamente os resultados da execução original.

### Análise

Os resultados demonstraram comportamento relativamente estável entre as três execuções.

Answer Relevancy apresentou o melhor desempenho, permanecendo próximo de 70% de aprovação nas três rodadas. Faithfulness apresentou o menor desempenho e uma redução progressiva, passando de 19,1% na primeira rodada para 17,6% na segunda e 14,7% na terceira.

O G-Eval apresentou 41,2% de aprovação tanto na segunda quanto na terceira rodada. A primeira rodada apresentou resultado bruto de 42,6%, porém foi afetada pelo erro técnico nos seis casos multi-turno.

Considerando os resultados gerais brutos, foram obtidas taxas de aprovação de 44,1%, 42,6% e 42,2%. A pequena variação entre as execuções é compatível com o comportamento não determinístico da Lia e da avaliação realizada por LLM.

Os thresholds e critérios das métricas não foram alterados entre as execuções. Dessa forma, os resultados foram preservados mesmo quando as justificativas produzidas pelo modelo juiz apresentaram avaliações mais restritivas.

---

## Conclusão

As três rodadas da versão corrigida demonstram que a Lia ainda apresenta quantidade significativa de falhas nas métricas automatizadas avaliadas pelo DeepEval.

Answer Relevancy apresentou o resultado mais consistente e elevado, enquanto Faithfulness concentrou a maior quantidade de falhas. O G-Eval permaneceu próximo de 41% de aprovação nas duas rodadas executadas integralmente após a correção dos casos multi-turno.

Os resultados das três rodadas devem ser utilizados em conjunto com as demais evidências do projeto, incluindo Promptfoo, Red Teaming e a comparação com a versão original, para fundamentar a decisão final de Go/No-Go.