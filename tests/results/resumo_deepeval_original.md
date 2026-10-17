# Resumo — DeepEval — Lia Original (Baseline)

Este documento consolida os resultados de **três rodadas de avaliação da versão original da Lia**, realizadas **antes de qualquer melhoria no prompt**, utilizando o DeepEval.

Em cada rodada, foram executados os **68 casos do Golden Dataset** nas métricas **Answer Relevancy**, **Faithfulness** e **G-Eval (Conformidade de Claims)**, totalizando **204 testes por rodada** e **612 execuções** no conjunto das três rodadas.

**Critério de contabilização:** todo teste que não terminou em `PASS` foi registrado como `FAIL`, incluindo reprovações por score e erros de execução. As taxas representam **aprovações sobre os 68 testes de cada métrica**. Os erros técnicos não são detalhados nos quadros de resultados; sua inclusão em `FAIL` não significa necessariamente que a resposta da Lia tenha sido incorreta.

**Thresholds:** Answer Relevancy ≥ 0,70; Faithfulness ≥ 0,80; G-Eval ≥ 0,80.

---

## Rodada 1

### Resultado geral da execução

A primeira rodada executou **204 testes**, correspondentes aos 68 casos do Golden Dataset avaliados nas três métricas.

| Métrica | PASS | FAIL | Total | Taxa de aprovação |
|---|---:|---:|---:|---:|
| Answer Relevancy | 30 | 38 | 68 | 44,1% |
| Faithfulness | 17 | 51 | 68 | 25,0% |
| G-Eval | 4 | 64 | 68 | 5,9% |
| **Total** | **51** | **153** | **204** | **25,0%** |

### Falhas observadas

O **Answer Relevancy** apresentou respostas pouco diretas, informações adicionais irrelevantes e excesso de conteúdo em perguntas objetivas.

O **Faithfulness** apresentou reprovações relacionadas à fidelidade ao contexto. Algumas justificativas do modelo juiz local, porém, foram internamente contraditórias, atribuindo scores baixos mesmo quando declaravam não identificar contradições. Essas ocorrências exigem revisão manual.

O **G-Eval** identificou divergências em preços e tamanhos, disponibilidade de sabores sazonais, restrições de embalagens e composição de kits.

### Falhas dos testes G-Eval

Os casos `TC-MLT-01` a `TC-MLT-06` falharam com **`KeyError: 'criterio_esperado'`**, devido à diferença na estrutura dos critérios dos casos multitur­no. Essas seis ocorrências estão incluídas na coluna **FAIL** do G-Eval, conforme o critério adotado neste relatório. Trata-se de falha da implementação do teste, e não de uma reprovação comprovada do agente.

---

## Rodada 2

A segunda rodada repetiu a avaliação da **mesma versão original da Lia**, sem alterações no prompt, totalizando **204 testes**.

| Métrica | PASS | FAIL | Total | Taxa de aprovação |
|---|---:|---:|---:|---:|
| Answer Relevancy | 29 | 39 | 68 | 42,6% |
| Faithfulness | 13 | 55 | 68 | 19,1% |
| G-Eval | 4 | 64 | 68 | 5,9% |
| **Total** | **46** | **158** | **204** | **22,5%** |

### Falhas observadas

O **Answer Relevancy** manteve problemas de prolixidade e respostas pouco alinhadas à solicitação, inclusive em cenários fora do escopo, adversariais e metamórficos.

O **Faithfulness** continuou apresentando baixa aprovação. Algumas justificativas do modelo juiz foram questionáveis, incluindo avaliações de disponibilidade sazonal e atribuição de scores baixos sem contradições explicitamente identificadas.

O **G-Eval** persistiu com reprovações associadas a preços, restrições de produtos e disponibilidade de sabores.

### Falhas dos testes G-Eval

Os seis casos `TC-MLT-01` a `TC-MLT-06` voltaram a apresentar **`KeyError: 'criterio_esperado'`**. As seis ocorrências estão contabilizadas como **FAIL**, sem serem atribuídas a um comportamento incorreto comprovado da Lia.

---

## Rodada 3

A terceira rodada manteve os mesmos critérios, thresholds e a **versão original do prompt**, com **204 testes** executados.

| Métrica | PASS | FAIL | Total | Taxa de aprovação |
|---|---:|---:|---:|---:|
| Answer Relevancy | 33 | 35 | 68 | 48,5% |
| Faithfulness | 22 | 46 | 68 | 32,4% |
| G-Eval | 6 | 62 | 68 | 8,8% |
| **Total** | **61** | **143** | **204** | **29,9%** |

### Falhas observadas

O **Answer Relevancy** registrou 33 aprovações, superando as duas rodadas anteriores em número absoluto, embora ainda tenha apresentado respostas com conteúdo pouco pertinente.

O **Faithfulness** registrou 22 aprovações. Persistiram possíveis conflitos com regras comerciais, incluindo restrições da lata presente, e justificativas inconsistentes do modelo juiz.

O **G-Eval** obteve seis aprovações. Permaneceram divergências de preços, tamanhos e disponibilidade sazonal. Como o prompt não foi modificado, o resultado não caracteriza melhoria implementada no agente.

### Falhas dos testes G-Eval

Os casos `TC-MLT-01` a `TC-MLT-06` permaneceram com **`KeyError: 'criterio_esperado'`**, totalizando mais seis ocorrências registradas como **FAIL**.

---

## Comparação das três rodadas

### Resultados por métrica

| Métrica | Rodada 1 | Rodada 2 | Rodada 3 | Aprovação geral |
|---|---:|---:|---:|---:|
| Answer Relevancy | 44,1% | 42,6% | 48,5% | **45,1%** |
| Faithfulness | 25,0% | 19,1% | 32,4% | **25,5%** |
| G-Eval | 5,9% | 5,9% | 8,8% | **6,9%** |
| **Resultado geral** | **25,0%** | **22,5%** | **29,9%** | **25,8%** |

### Análise comparativa

**Answer Relevancy — melhor desempenho relativo.** A aprovação variou entre **42,6% e 48,5%**, indicando que a relevância das respostas foi a dimensão com mais testes aprovados. Permaneceram falhas relacionadas à objetividade e à aderência à pergunta.

**Faithfulness — desempenho intermediário, com limitações do juiz.** A aprovação variou entre **19,1% e 32,4%**. Os resultados apontam riscos de afirmações sem sustentação no contexto, mas justificativas contraditórias do modelo juiz exigem inspeção manual antes de classificar todas as reprovações como alucinações reais.

**G-Eval — principal ponto crítico.** A aprovação ficou entre **5,9% e 8,8%**, com numerosas reprovações em critérios de catálogo, preços, disponibilidade e restrições comerciais. Os seis erros dos testes multitur­no se repetiram nas três rodadas.

**Variação entre rodadas.** As diferenças de aprovação não demonstram evolução do agente: **nenhuma melhoria foi aplicada ao prompt** entre as execuções. A natureza não determinística das respostas e do juiz, somada à contabilização de erros de execução como `FAIL`, limita a interpretação dos percentuais como medida isolada da qualidade do agente.

---

## Relatório geral — Baseline da Lia Original

### Síntese quantitativa

| Indicador | Resultado |
|---|---:|
| Versão avaliada | **Lia original, sem melhorias no prompt** |
| Casos no Golden Dataset | 68 |
| Métricas avaliadas | 3 |
| Rodadas por métrica | 3 |
| **Total de testes executados** | **612** |
| **PASS** | **158** |
| **FAIL** | **454** |
| **Taxa geral de aprovação** | **25,8%** |
| Falhas de implementação do G-Eval (`KeyError`), incluídas em FAIL | **18** |

### Diagnóstico de qualidade

A versão original da Lia obteve mais aprovações em **Answer Relevancy** do que em **Faithfulness** e **G-Eval**. Isso mostra que uma resposta pode ser pertinente à pergunta, mas ainda apresentar **preços incorretos, regras comerciais violadas ou afirmações sem respaldo na fonte de referência**.

Os principais problemas identificados foram:

1. **Precisão do catálogo:** divergências em preços, tamanhos e características de produtos.
2. **Cumprimento de regras comerciais:** inconsistências sobre sabores sazonais, embalagens, kits e combinações permitidas.
3. **Fidelidade factual:** respostas potencialmente incompatíveis com o contexto e avaliações do juiz que precisam de revisão.
4. **Confiabilidade da suíte:** falhas recorrentes na implementação da avaliação dos seis casos multitur­no do G-Eval.

### Limitações da avaliação

Os percentuais representam **taxas brutas de aprovação dos testes executados**, e não médias dos scores numéricos do DeepEval. Como todo resultado diferente de `PASS` foi classificado como `FAIL`, **a quantidade de falhas não equivale à quantidade de respostas incorretas da Lia**. Isso inclui falhas de implementação dos testes e outras execuções sem aprovação.

O modelo juiz local apresentou justificativas inconsistentes em alguns casos de Faithfulness. Por isso, a análise qualitativa das reprovações deve considerar as respostas, os contextos de referência e os critérios esperados.

### Conclusão

As três rodadas estabelecem a **baseline da versão original da Lia**, anterior às melhorias de prompt. Foram registrados **158 testes aprovados e 454 testes com falha**, resultando em **25,8% de aprovação geral**.

O melhor desempenho ocorreu em **Answer Relevancy (45,1%)**, seguido de **Faithfulness (25,5%)** e **G-Eval (6,9%)**. Os resultados indicam prioridades de melhoria na **aderência ao catálogo, aplicação de regras comerciais, fundamentação factual e objetividade das respostas**.

Essa baseline poderá ser comparada posteriormente com a **Lia corrigida**, mantendo o mesmo Golden Dataset, os mesmos thresholds e critérios de avaliação. A decisão final de **Go/No-Go** deve considerar também Promptfoo, Red Teaming, testes determinísticos e revisão dos casos críticos, pois os percentuais brutos, isoladamente, não permitem atribuir todas as falhas ao agente.
