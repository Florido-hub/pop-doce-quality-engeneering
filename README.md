# Go/No-Go da assistente Lia (Pop & Doce)

Hackathon de encerramento, squad de Quality Engineering.

A Pop & Doce Pipocaria Gourmet (empresa fictícia) quer colocar no ar a Lia, uma assistente virtual de vendas. A squad atuou como time de qualidade independente para responder três perguntas: quais defeitos e vulnerabilidades a Lia tem, quais correções são necessárias e se ela pode ir para produção.

Recomendação: No-Go. O parecer completo está em [`relatorios/parecer_go_no_go.md`](relatorios/parecer_go_no_go.md), e a comparação entre as versões em [`relatorios/comparacao_original_vs_corrigida.md`](relatorios/comparacao_original_vs_corrigida.md).

## Etapas e responsáveis

| # | Etapa | Responsável | Status |
|---|---|---|---|
| 1 | Testes exploratórios | Andressa | Concluído |
| 2 | Golden dataset (68 casos) | Vitor | Concluído |
| 3 | Automação da suíte (DeepEval e Promptfoo) | Flórido | Concluído |
| 4 | Red teaming (30 tentativas, 6 categorias) | Ananda | Concluído |
| 5 | Teste da versão original | Squad | Concluído |
| 6 | Prompt de sistema corrigido | Squad | Concluído |
| 7 | Teste da versão corrigida | Squad | DeepEval concluído; Promptfoo e red teaming em reexecução |
| 8 | Comparação original x corrigida | Squad | Concluído com os dados válidos; atualizar após a etapa 7 |
| 9 | Parecer Go/No-Go | Squad | Concluído |
| 10 | README e organização | Squad | Concluído |

## Estrutura do repositório

```
base-de-conhecimento-oficial/   Base oficial da Pop & Doce (referência do que é correto)
massa-de-teste.md               Pedidos fictícios usados nos testes
DescritivoDesafio.md            Descrição do desafio

data/
  golden_dataset.json           68 casos com critério esperado, referência, asserções e ferramenta esperada
  golden_dataset.md             Documentação dos casos e dos 6 pares metamórficos
  red_team/resultados/          Red teaming: relatório, JSON/CSV das execuções e análise
  resultados/corrigida/         DeepEval e Promptfoo da versão corrigida

prompts/
  prompt_corrigido.md           Prompt de sistema da versão corrigida

src/
  chatbot.py                    Cliente da API da Lia (lê a chave do .env)
  casos_red_team.py             30 casos de red teaming
  rodar_red_team.py             Executa o red teaming

testes_exploratorios/
  casos_exploratorios.py        60 casos em 8 charters, com o esperado e a referência na base
  rodar_exploratorio.py         Executa os casos e salva as respostas em CSV/JSON
  defeitos_exploratorios.md     Defeitos encontrados, com severidade e evidência
  resultados/                   Execução da versão original (60 casos x 3)

tests/
  deepeval_tests/               Answer Relevancy, Faithfulness e G-Eval sobre o golden dataset
  promptfoo/                    Verificação do campo ferramentas a partir do golden dataset
  utils/                        Juiz do DeepEval, preparação de entradas e escolha da versão
  results/                      Resumos do DeepEval e do Promptfoo da versão original

relatorios/
  comparacao_original_vs_corrigida.md
  parecer_go_no_go.md
```

## Como executar

### 1. Preparar o ambiente

Pré-requisitos: Python 3, Node.js (para o Promptfoo) e Ollama (juiz local do DeepEval).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

Copie o `.env.example` para `.env` e preencha a chave da squad:

```
LIA_API_KEY=sua_chave_aqui
```

O `.env` está no `.gitignore`. A chave nunca deve aparecer em código, logs, resultados ou documentos versionados. Antes de subir resultados, confira com `git grep -n "x-api-key"` que nenhum arquivo traz os cabeçalhos das requisições.

### 2. Escolher a versão da Lia

As suítes usam a variável `VERSAO_LIA`:

| Valor | O que faz |
|---|---|
| `original` (padrão) | Chama a API sem `prompt_sistema` |
| `corrigida` | Envia `prompts/prompt_corrigido.md` no campo `prompt_sistema` |

```bash
# Windows PowerShell
$env:VERSAO_LIA = "corrigida"
# Linux/Mac
export VERSAO_LIA=corrigida
```

Antes de rodar a versão corrigida, confirme que o prompt chega à API. A saída deve ser `corrigida` e o preço R$ 39,90:

```bash
python -c "from src.chatbot import perguntar; from pathlib import Path; r=perguntar('Quanto custa a pipoca Caramelo Clássico grande?', prompt=Path('prompts/prompt_corrigido.md').read_text(encoding='utf-8'), retornar_json=True); print(r.get('versao')); print(r['resposta'])"
```

### 3. DeepEval

O juiz padrão é um modelo local no Ollama (`JUIZ_MODEL`, padrão `gemma3:4b`). Para usar o Gemini, defina `JUIZ_PROVIDER=gemini` e `GEMINI_API_KEY`.

```bash
ollama pull gemma3:4b
cd tests
# Windows PowerShell: $env:PYTHONPATH = ".."    Linux/Mac: export PYTHONPATH=..
python -m pytest deepeval_tests/test_geval.py deepeval_tests/test_answerRelevancy.py deepeval_tests/test_faithfulness.py --junitxml=resultado_deepeval.xml
```

Repita 3 vezes para cada versão.

### 4. Promptfoo

```bash
python tests/promptfoo/gerar_testes.py
cd tests/promptfoo
npx promptfoo@latest eval -c promptfooconfig.yaml --no-cache --max-concurrency 2
npx promptfoo@latest view
```

Repita 3 vezes para cada versão e exporte os resultados em JSON/CSV pela interface do `promptfoo view`. Mais detalhes em [`tests/promptfoo/README.md`](tests/promptfoo/README.md).

### 5. Red teaming

```bash
python src/rodar_red_team.py                                       # versão original, 30 casos x 3
python src/rodar_red_team.py --prompt prompts/prompt_corrigido.md  # versão corrigida
python src/rodar_red_team.py --casos RT-PI-01 RT-CM-03 --repeticoes 1
```

### 6. Testes exploratórios

```bash
python testes_exploratorios/rodar_exploratorio.py                                       # 60 casos x 3, versão original
python testes_exploratorios/rodar_exploratorio.py --prompt prompts/prompt_corrigido.md  # versão corrigida
python testes_exploratorios/rodar_exploratorio.py --charter C2 --repeticoes 1          # só um charter
```

Os resultados vão para `resultados/`, em CSV (abre no Excel) e JSON.

## Regras seguidas

- Testes feitos só contra a Lia, pela API fornecida, sem acesso à conta AWS ou à infraestrutura.
- No máximo 4 chamadas em paralelo (os scripts usam 2). Sem testes de carga ou estresse.
- Apenas a massa de teste e dados inventados. Nenhum dado pessoal real.
- Cada caso executado pelo menos 3 vezes, em sessão nova, nas duas versões.
- Suítes geradas com apoio de IA foram revisadas pela squad.
