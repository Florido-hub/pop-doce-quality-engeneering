## Executando os testes com Promptfoo

### 1. Executar os testes

Primeiro, acesse o diretório do Promptfoo:

```powershell
cd .\tests\promptfoo
```

Depois, execute:

```powershell
npx promptfoo@latest eval -c .\promptfooconfig.yaml --no-cache --max-concurrency 2
```

**Parâmetros:**

- `-c`: especifica o arquivo de configuração.
- `--no-cache`: força novas chamadas à API, sem reutilizar respostas anteriores.
- `--max-concurrency 2`: limita a execução a duas requisições simultâneas.

### 2. Gerar os casos de teste

Sempre que houver alterações no `gerar_testes.py` ou no `data/golden_dataset.json`, é necessário regenerar o arquivo `tool_usage.yaml`.

Execute o comando na **raiz do projeto**:

```powershell
python .\tests\promptfoo\gerar_testes.py
```

Esse comando atualiza os casos de teste utilizados pelo Promptfoo.

### 3. Visualizar os resultados

Após a execução, utilize:

```powershell
npx promptfoo@latest view
```

O Promptfoo abrirá uma interface no navegador para visualizar os casos aprovados (`PASS`), reprovados (`FAIL`) e com erros de execução (`ERROR`).

### 4. Fluxo de execução após modificações

Sempre que modificar o gerador ou o Golden Dataset, siga esta sequência:

```powershell
# Na raiz do projeto: regenerar os testes
python .\tests\promptfoo\gerar_testes.py

# Acessar o diretório do Promptfoo
cd .\tests\promptfoo

# Executar os testes
npx promptfoo@latest eval -c .\promptfooconfig.yaml --no-cache --max-concurrency 2

# Visualizar os resultados
npx promptfoo@latest view
```

**Observação:** se nenhuma alteração foi realizada no gerador ou no Golden Dataset, não é necessário regenerar os testes. Basta executar o Promptfoo diretamente.