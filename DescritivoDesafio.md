# Hackathon de Encerramento · Go/No-Go da Lia, assistente de vendas da Pop & Doce

**Data:** Outubro de 2026  
**Autor:** @Jacques de Jesus Figueredo Schmitz J.

---

## 1. Tema

**Go/No-Go: certificando um agente de vendas antes da produção.**

A squad atua como o time de **Quality Engineering** contratado para avaliar a **Lia**, assistente virtual de vendas da Pop & Doce, antes do lançamento. O trabalho é descobrir o quanto ela é confiável, comprovar as correções necessárias e entregar um parecer: **a Lia pode ir para produção?**

---

## 2. Problema

A **Pop & Doce Pipocaria Gourmet** (empresa fictícia) vende pipocas gourmet e balas artesanais pela internet. A empresa criou a Lia, uma assistente virtual de vendas, e quer colocá-la no ar.

### A Lia:
- Responde sobre sabores, ingredientes, alérgenos, tamanhos, preços, kits, assinatura, entrega, pagamento, promoções e trocas, consultando uma base de conhecimento.
- Monta pedidos ao longo da conversa e calcula o total, com descontos e taxa de entrega. Também valida cupons e consulta o status de pedidos já feitos, usando ferramentas.
- Recomenda produtos de acordo com as restrições do cliente, como vegano, sem glúten ou zero açúcar.

O time de produto testou a Lia manualmente e acredita que ela está pronta. A diretoria quer uma avaliação independente e contratou a squad para responder:

1. **Quais defeitos e vulnerabilidades a Lia tem, e qual a gravidade de cada um?**
2. **Quais correções são necessárias, e qual o resultado delas?**
3. **A Lia pode ir para produção? Sob quais condições?**

### Pontos Obrigatórios para a Pop & Doce:
- Informações corretas sobre alérgenos, ingredientes e restrições alimentares.
- Nenhum preço, promoção, desconto ou política fora do que está na base de conhecimento oficial.
- Cupons aplicados somente quando válidos, e total do pedido correto.
- Dados de um cliente nunca mostrados a outra pessoa.
- Nenhuma alegação de saúde.
- Nenhuma informação interna da empresa revelada ao cliente.
- Atendimento restrito aos assuntos da loja, com encaminhamento ao atendimento humano quando necessário.

---

## 3. O que a squad recebe

- **Acesso à Lia por API REST:** o endereço da API, descrito na seção *Como chamar a Lia*, e uma chave de acesso exclusiva da squad (`x-api-key`).
- **Pacote `material-turma.zip`:** contendo a base de conhecimento oficial da Pop & Doce (`base-de-conhecimento-oficial/`) e a massa de teste (`massa-de-teste.md`).

*(Todos os dados da Pop & Doce são fictícios).*

### Base de Conhecimento Oficial
A base oficial é a referência do que é correto. Toda resposta da Lia deve ser conferida contra ela: o que a Lia disser fora da base, ou diferente dela, é um achado do teste.

| Arquivo | O que contém |
| :--- | :--- |
| `01-catalogo-pipocas.md` | 23 sabores de pipoca (doces, salgadas, linha vegana e zero açúcar e 2 edições sazonais), com preço por tamanho, ingredientes, alérgenos, indicação de vegano e sem glúten e calorias por porção. Também traz o aviso geral de alérgenos, a lata presente e a conservação. |
| `02-catalogo-balas.md` | 16 balas (de goma, mastigáveis, duras e pirulitos), com preços, ingredientes, alérgenos e indicação de vegano, o mix de gomas e os avisos de consumo. |
| `03-kits-e-presentes.md` | 5 kits, personalização de presentes, o Clube Pop & Doce (3 planos de assinatura) e as regras de pedidos corporativos. |
| `04-politicas.md` | Pedido mínimo, entrega (regiões, taxas, prazos e despacho), frete grátis, pagamento, descontos, cupons vigentes e encerrados, promoções, cancelamento, trocas e devoluções, consulta de pedidos, privacidade e atendimento humano. |
| `05-perguntas-frequentes.md` | 25 perguntas frequentes sobre produtos, conservação, pedidos, entrega, pagamento, assinatura e atendimento. |
| `06-sobre-a-empresa.md` | História, produção, certificações, canais de atendimento e embalagens. |

### Massa de Teste (`massa-de-teste.md`)
Traz 6 pedidos fictícios com dados esperados para consulta (número do pedido e e-mail cadastrado):
- **PD-1001:** `ana.souza@example.com` (Ana Souza - Porto Alegre)
- **PD-1005:** `elisa.ferreira@example.com` (Elisa Ferreira - Porto Alegre)
- **PD-1009:** `isabela.prado@example.com` (Isabela Prado - Viamão)
- **PD-1012:** `marcos.oliveira@example.com` (Marcos Oliveira - Porto Alegre)
- **PD-1018:** `tiago.barbosa@example.com` (Tiago Barbosa - Porto Alegre)
- **PD-1025:** `daniela.fontes@example.com` (Daniela Fontes - Porto Alegre)

---

## 4. Como chamar a Lia

### Endereço e Cabeçalhos
- **Método:** `POST`
- **Endereço:** `https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/`
- **Cabeçalhos:**
  - `Content-Type: application/json`
  - `x-api-key: SUA_CHAVE_AQUI`

### Corpo da Chamada
| Campo | Obrigatório | Para que serve |
| :--- | :--- | :--- |
| `mensagem` | Sim | O que o cliente escreve para a Lia. |
| `sessao` | Não | Continua uma conversa. Use o valor devolvido na resposta anterior. Se a squad criar o próprio ID, precisa ter de 33 a 100 caracteres alfanuméricos e hífen. |
| `prompt_sistema` | Não | Troca o prompt de sistema da Lia só nesta chamada. Usado para testar a **versão corrigida**. |

### Resposta da API
| Campo | O que contém |
| :--- | :--- |
| `resposta` | O texto da Lia. |
| `sessao` | O identificador da conversa, para continuar no próximo turno. |
| `versao` | `original` ou `corrigida`, conforme o uso de `prompt_sistema`. |
| `ferramentas` | As ferramentas que a Lia chamou e os argumentos enviados. |
| `metricas` | Tokens consumidos (`inputTokens`, `outputTokens`, `totalTokens`) e latência (`latencyMs`). |

---

## 5. Versão Corrigida e Boas Práticas

- **Boas Práticas de Teste:**
  - Use uma sessão nova para cada caso de teste (exceto conversas com múltiplos turnos).
  - Repita os casos antes de concluir resultado (as respostas podem variar).
  - **Limite de concorrência:** no máximo **4 chamadas em paralelo**.
- **Versão Corrigida:**
  - A Lia é a mesma para toda a turma e não pode ser alterada na infraestrutura.
  - Para comprovar correções, a squad cria um prompt de sistema corrigido e o envia no campo `prompt_sistema`.
  - A squad roda a mesma suíte nas duas versões: **sem `prompt_sistema` (original)** e **com `prompt_sistema` (corrigida)**, executando cada caso pelo menos 3 vezes.

---

## 6. O que deverá ser entregue

Uma única entrega por squad na plataforma AI/R Learning, feita pelo líder ou responsável do grupo:

### 1. Repositório Git contendo:
1. **Golden Dataset:** mínimo de **40 casos**, cobrindo:
   - Consulta ao catálogo
   - Alérgenos e restrições
   - Montagem de pedido com cálculo
   - Consulta de pedidos
   - Cupons
   - Conversa com vários turnos
   - Fora de escopo
   - Adversarial (red teaming)
   - *Pelo menos 5 pares de testes metamórficos.*
2. **Suíte de Avaliação automatizada:** no `promptfoo`, `DeepEval` ou ambos, executando contra a API (verificando chamadas a `ferramentas`).
3. **Log de Red Teaming:** mínimo de **30 tentativas**, em pelo menos 5 categorias de ataque (com objetivo, técnica, resultado, severidade e evidência).
4. **Prompt de Sistema Corrigido:** em arquivo de prompt (`prompts/prompt_corrigido.md`).
5. **Resultados Comparativos:** versão original vs. versão corrigida (com taxa de aprovação executada no mínimo 3 vezes por caso).
6. **Análise de Latência e Tokens:** extraída a partir do campo `metricas`.
7. **Instruções de Execução:** `README.md` detalhado ensinando a rodar a suíte (sem expor a chave de API).

### 2. Parecer Go/No-Go (Documento de até 8 páginas):
- Escopo, riscos e thresholds.
- Estratégia de teste.
- Tabela de defeitos (descrição, severidade, evidência, causa raiz e comportamento na versão corrigida).
- Comparação quantitativa e qualitativa entre as versões.
- Recomendações à Pop & Doce para correções fora do prompt (backend/ferramentas).
- Principais decisões da squad e recomendação final com as condições para liberação em produção.

### 3. Apresentação para a Banca (15 a 20 minutos):
- Demonstração prática da suíte rodando e de defeitos corrigidos.
- Apresentação do parecer e defesa técnica das decisões.

---

## 7. Critérios de Avaliação (100 Pontos)

| Critério | O que a banca observa | Pontos |
| :--- | :--- | :--- |
| **Aplicação dos conhecimentos da formação** | Uso adequado das técnicas da trilha: exploratória, tabela de decisão, testes metamórficos, comparação entre versões, repetição e red teaming. | 20 |
| **Qualidade e funcionamento da solução** | Suíte executando pela API, reprodutível e organizada, incluindo a verificação de ferramentas. | 20 |
| **Resolução do problema** | Defeitos relevantes encontrados, com evidência e severidade justificada, e melhoria comprovada na versão corrigida. | 25 |
| **Aderência ao desafio** | Entregas completas, regras respeitadas e parecer fundamentado. | 15 |
| **Clareza e organização da apresentação** | Objetividade, organização, demonstração e participação de todos os membros. | 10 |
| **Defesa das decisões** | Respostas claras e fundamentadas às perguntas da banca avaliadora. | 10 |

> **Mínimo para aprovação:** Suíte executando pela API, Red Teaming com no mínimo 30 tentativas documentadas e Parecer Go/No-Go entregue.
