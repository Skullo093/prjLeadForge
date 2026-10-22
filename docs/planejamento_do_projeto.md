# Planejamento do Projeto de Software

Este documento organiza como o LeadForge será construído: o que entra em cada entrega, quem faz o quê, em que ordem, com quais tecnologias e como vamos garantir a qualidade. Ele parte do que já está definido nos documentos anteriores:

- [Definição do projeto](01-definicao-do-projeto.md), [tema e delimitação](02-tema-e-delimitacao.md) e [requisitos de negócio](03-requisitos-de-negocio.md);
- [Requisitos funcionais](requisitos_funcionais.md) e [não funcionais](requisitos_n_o_funcionais.md);
- [Escolha do modelo de software](Escolha%20do%20modelo%20de%20Software.md): Scrum.

## 1. Objetivo e entregas

Entregar o fluxo central do LeadForge (perfil → descoberta → evidências → avaliação → abordagem com IA → exportação) em três artefatos:

| Entrega | Conteúdo | Etapas (issues) |
|---|---|---|
| **1. Documento** | Definição, requisitos, modelo de desenvolvimento, planejamento e diagramas | #1 a #9 |
| **2. Protótipos** | Telas em média fidelidade e a forma de testá-las | #10 e #11 |
| **3. Sistema** | Implementação de 30% dos protótipos | #12 |

Os 30% de protótipos implementados formam o **recorte do sistema** desta etapa do TCC. O produto completo (RF-01 a RF-11) segue como backlog e orienta a ordem de construção.

## 2. Organização da equipe

Seguimos o Scrum, como definido na escolha do modelo de software. Os três integrantes atuam como desenvolvedores; os outros dois papéis são distribuídos conforme a atuação de cada um até aqui. Esta distribuição foi confirmada pela equipe.

| Papel | Responsável | Responsabilidade |
|---|---|---|
| Product Owner | Murillo Lourenço | Mantém o backlog e define prioridades com base nos requisitos de negócio. |
| Scrum Master | Allan Batista | Facilita os eventos, remove impedimentos e cuida do processo. |
| Desenvolvedor | Murillo Lourenço, Allan Batista e Bruno Rocha | Estimam, constroem e testam os itens da sprint. |

### Cadência dos eventos

| Evento | Frequência | Duração |
|---|---|---|
| Sprint | 2 semanas (a Sprint 5 tem 1 semana) | — |
| Sprint Planning | Início da sprint | até 1 h |
| Daily Scrum | Combinada pela equipe (pode ser assíncrona no grupo de mensagens) | até 15 min |
| Sprint Review | Data de fim da sprint (ver seção 4) | até 1 h |
| Retrospectiva | Após a review | até 30 min |

## 3. Backlog do produto

Agrupamos os requisitos em épicos e priorizamos pelo método MoSCoW (**M**ust, **S**hould, **C**ould).

| Épico | Requisitos | Prioridade | Previsto em | Observação |
|---|---|---|---|---|
| E1. Conta e perfil | RF-01, RNF-02 | Must | Sprint 4 | Inclui cadastro e login, necessários para isolar a carteira de cada usuário (REG-09). |
| E2. Descoberta de empresas | RF-02, RF-03, RNF-04 | Must | Sprint 4 | Integração com a API Geoapify, atrás de uma interface substituível. |
| E3. Evidências e avaliação | RF-04, RF-05, RF-06 | Must | Sprint 4 (parcial) | Núcleo do produto: o que é detectado e com qual certeza. Entra o que couber nos 30%. |
| E4. IA aplicada | RF-07, RF-08, RNF-01, RNF-05 | Must | Após os 30%, ou Sprint 5 se houver folga | A IA só sintetiza dados já coletados e nada é enviado sem revisão. |
| E5. Gestão da carteira | RF-10, RF-11 | Should | Após os 30% | Status do contato e exportação CSV/JSON. |
| E6. Assistente de análise | RF-09 | Could | Após os 30% | Consulta em linguagem natural; entra se houver tempo. |
| E7. Transversais | RNF-03, RNF-06 | Must | Todas as sprints | Interface responsiva e código modular. |

A **prioridade** diz o quanto o item importa para o produto; a coluna **Previsto em** diz quando ele entra, considerando que o sistema desta etapa cobre 30% dos protótipos. Quais telas formam esses 30% será definido na Sprint 3, junto com os protótipos (issue #10).

## 4. Plano de sprints

As datas abaixo são o **fim de cada sprint**, quando acontecem a Sprint Review e a Retrospectiva. Os milestones do GitHub (S1 a S5) correspondem às sprints.

| Sprint | Fim | Foco | Issues | Resultado esperado |
|---|---|---|---|---|
| **1** | 09/10 | Definição e requisitos | #1 a #6 | Definição, tema e delimitação, requisitos de negócio, funcionais e não funcionais, e modelo de software. **Concluída.** |
| **2** | 23/10 | Planejamento e modelagem | #7, #8 e #9 | Este planejamento, o diagrama de casos de uso e o diagrama de classes. |
| **3** | 06/11 | Protótipos | #10 e #11 | Telas em média fidelidade, definição dos 30% a implementar e escolha do modo de testar a prototipação. |
| **4** | 20/11 | Sistema | #12 | Implementação de 30% dos protótipos: base do projeto, perfil, descoberta de empresas e o que couber da avaliação de oportunidades. |
| **5** | 27/11 | Entrega final | #13, #14 e #15 | Consolidação e entrega dos três artefatos: Documento, Protótipos e Sistema. Sprint de 1 semana. |

A Sprint 5 é curta e serve para revisar e consolidar, por isso nenhuma funcionalidade nova deve começar nela, a não ser que as anteriores terminem com folga.

### Decisões deixadas para a Sprint 3

O que ainda não precisa ser decidido agora fica para a próxima sprint. Abaixo estão as opções que mais fazem sentido para cada ponto, com uma sugestão. A decisão final é da equipe e, depois de tomada, será registrada neste documento.

**1. Provedor da API de IA** (usado em E4: explicação e rascunho de abordagem)

| Opção | Vantagens | Pontos de atenção |
|---|---|---|
| **OpenAI** (sugerida) | SDK amplo e bem documentado, boa saída estruturada em JSON, já havia chave reservada para esse uso. | Uso pago; é preciso definir um teto de gasto. |
| Anthropic (Claude) | Bom desempenho em português e em seguir instruções restritas, o que ajuda no RNF-01. | Uso pago; menos material de apoio em português. |
| Google (Gemini) | Possui camada gratuita com limites, útil para desenvolver sem custo. | Limites de requisição menores, o que pesa no RNF-04. |

Como a camada de IA fica atrás de uma interface própria (RNF-06), trocar de provedor depois tem custo baixo. A sugestão é começar por um e manter o outro como alternativa.

**2. Quais telas formam os 30% do sistema** (a definição final sai junto com os protótipos, issue #10)

| Opção | Telas | Cobre | Observação |
|---|---|---|---|
| **A. Fluxo mínimo ponta a ponta** (sugerida) | Cadastro/login, perfil, busca de empresas e lista de oportunidades com ranking | RF-01, RF-02, RF-03, RF-06 | Mostra o valor do produto sem depender da IA e é a opção mais segura para o prazo. |
| B. Foco na IA | Busca, detalhe da oportunidade com explicação e rascunho de abordagem | RF-02, RF-07, RF-08 | Destaca a integração pedida pela professora, mas depende de a busca e as evidências funcionarem bem. |
| C. Foco na gestão | Lista de oportunidades, status do contato e exportação | RF-10, RF-11 | Entrega mais fácil, mas com menos peso técnico para o TCC. |

**3. Modo de testar a prototipação** (issue #11)

| Opção | Quem testa | Vantagens | Pontos de atenção |
|---|---|---|---|
| Restrito | Só a equipe de desenvolvimento | Rápido e sem custo de organização. | Visão enviesada, pois quem fez conhece o fluxo. |
| **Total** (sugerida) | Possíveis clientes, ou seja, freelancers | Feedback do público-alvo real. | Exige recrutar poucas pessoas e combinar horário. |
| Geral | Qualquer pessoa | Fácil de conseguir participantes. | O retorno pode não refletir a necessidade de um freelancer. |

A sugestão é começar com o teste restrito para corrigir erros óbvios e fazer o teste total com 3 a 5 freelancers antes da entrega.

## 5. Tecnologias

| Camada | Escolha | Motivo |
|---|---|---|
| Backend | Python 3.12 + FastAPI | API REST simples de construir, documentação automática e bom ecossistema para IA e análise de HTML. |
| Banco de dados | SQLite no desenvolvimento, com migrações (Alembic) e SQLAlchemy | Zero configuração para a equipe; permite migrar para PostgreSQL sem reescrever. |
| Frontend | React + Vite | Atende à aplicação web responsiva (RNF-03) e é amplamente documentado. |
| IA | API de um modelo de linguagem, acessada por uma camada própria | Isola o provedor para trocar sem afetar o sistema (RNF-04 e RNF-06). O provedor será escolhido na Sprint 3. |
| Busca de empresas | **Geoapify** (Places, Geocoding e Place Details), acessada por uma camada própria | Permite guardar os resultados na carteira do usuário, o que não é possível com a API de lugares do Google por restrição de armazenamento. Os dados vêm do OpenStreetMap, com a atribuição exigida. |
| Fonte alternativa | OpenStreetMap (Overpass) | Plano B quando não houver chave do Geoapify. É menos estável, então não é o caminho principal. |
| Testes e qualidade | Pytest, Ruff e GitHub Actions | Testes automáticos e verificação de estilo a cada pull request. |
| Gestão | GitHub (issues, milestones e pull requests) | Já é usado pela equipe. |

> A stack foi aprovada pela equipe. Qualquer mudança futura deve ser registrada neste documento.

### Visão geral da arquitetura

```text
Navegador (React)
      ↓  HTTP/JSON
API FastAPI
  ├── Perfil e autenticação
  ├── Descoberta de empresas ──→ Geoapify
  ├── Análise de evidências ───→ sites públicos
  ├── Avaliação e ranking
  ├── Camada de IA ────────────→ provedor de LLM
  └── Carteira e exportação
      ↓
Banco de dados
```

Cada integração externa fica atrás de uma interface própria, o que sustenta o RNF-06 (extensibilidade) e facilita testar sem chamar serviços reais.

## 6. Gestão de configuração

- **Branches:** `main` é sempre estável; cada trabalho nasce em uma branch curta (`docs/...`, `feature/...`, `fix/...`).
- **Pull requests:** toda mudança entra por PR, com descrição objetiva e referência à issue (`Closes #n`). Outro integrante revisa antes do merge.
- **Commits:** mensagens curtas e no imperativo ou com prefixo (`docs:`, `feat:`, `fix:`, `test:`).
- **Issues e labels:** cada tarefa é uma issue com label de tamanho estimado (P, M ou G) e milestone da sprint.
- **Segredos:** chaves de API ficam em variáveis de ambiente e nunca no repositório.

## 7. Qualidade e testes

**Definição de pronto (DoD)** para um item do backlog:

1. atende aos critérios de aceite da issue;
2. tem testes automáticos quando envolve regra de negócio;
3. passa na verificação de estilo (lint) e nos testes no CI;
4. foi revisado por outro integrante via pull request;
5. a documentação afetada foi atualizada.

**Estratégia de testes:**

| Tipo | O que cobre |
|---|---|
| Unitários | Pontuação, níveis de certeza, deduplicação e montagem dos textos de IA. |
| Integração | Rotas da API com banco de teste e provedores simulados (mocks). |
| Integridade da IA | Verificação por amostra de que os textos gerados só usam dados coletados (RNF-01). |
| Usabilidade | Teste dos protótipos conforme definido na etapa 11. |

## 8. Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Limite de requisições ou indisponibilidade das APIs externas (RNF-04) | Alto | Interface substituível, cache dos resultados e provedor simulado para desenvolver e testar. |
| IA gerar informação que não existe nos dados (RNF-01) | Alto | Prompt restrito aos dados coletados, exibição da origem de cada afirmação e revisão por amostra. |
| Custo de uso das APIs | Médio | Limitar o número de resultados por busca e usar chaves de teste com teto de gasto. |
| Prazo curto para 30% do sistema | Alto | Priorização MoSCoW e construção do fluxo ponta a ponta antes dos itens `Should` e `Could`. |
| Falsos positivos na análise de sites | Médio | Usar os níveis de certeza e tratar ausência de evidência como `desconhecido` (REG-03). |
| Disponibilidade da equipe | Médio | Tarefas pequenas, revisão cruzada e comunicação semanal. |
| Questões de privacidade (LGPD) | Médio | Armazenar apenas dados públicos de empresas e isolar a carteira por usuário (RNF-02). |

## 9. Comunicação

- **Acompanhamento:** issues e milestones do GitHub.
- **Dia a dia:** grupo de mensagens da equipe, com a Daily Scrum feita ali quando não houver reunião.
- **Decisões:** registradas nas issues ou neste documento, para não se perderem.

## 10. Critérios de conclusão desta etapa

A etapa 7 está concluída quando este planejamento estiver revisado e aprovado pelos três integrantes e mesclado na `main`. Ajustes posteriores em prazos e tecnologias são feitos por pull request e registrados na retrospectiva da sprint.
