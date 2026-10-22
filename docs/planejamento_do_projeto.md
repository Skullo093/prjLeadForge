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

Seguimos o Scrum, como definido na escolha do modelo de software. Os três integrantes atuam como desenvolvedores; os outros dois papéis são distribuídos conforme a atuação de cada um até aqui.

| Papel | Responsável | Responsabilidade |
|---|---|---|
| Product Owner | Murillo Lourenço | Mantém o backlog e define prioridades com base nos requisitos de negócio. |
| Scrum Master | Allan Batista | Facilita os eventos, remove impedimentos e cuida do processo. |
| Desenvolvedor | Murillo Lourenço, Allan Batista e Bruno Rocha | Estimam, constroem e testam os itens da sprint. |

### Cadência dos eventos

| Evento | Frequência | Duração |
|---|---|---|
| Sprint | 2 semanas | — |
| Sprint Planning | Início da sprint | até 1 h |
| Daily Scrum | Combinada pela equipe (pode ser assíncrona no grupo de mensagens) | até 15 min |
| Sprint Review | Fim da sprint | até 1 h |
| Retrospectiva | Após a review | até 30 min |

## 3. Backlog do produto

Agrupamos os requisitos em épicos e priorizamos pelo método MoSCoW (**M**ust, **S**hould, **C**ould).

| Épico | Requisitos | Prioridade | Observação |
|---|---|---|---|
| E1. Conta e perfil | RF-01, RNF-02 | Must | Inclui cadastro e login, necessários para isolar a carteira de cada usuário (REG-09). |
| E2. Descoberta de empresas | RF-02, RF-03, RNF-04 | Must | Integração com API de lugares, atrás de uma interface substituível. |
| E3. Evidências e avaliação | RF-04, RF-05, RF-06 | Must | Núcleo do produto: o que é detectado e com qual certeza. |
| E4. IA aplicada | RF-07, RF-08, RNF-01, RNF-05 | Must | A IA só sintetiza dados já coletados e nada é enviado sem revisão. |
| E5. Gestão da carteira | RF-10, RF-11 | Should | Status do contato e exportação CSV/JSON. |
| E6. Assistente de análise | RF-09 | Could | Consulta em linguagem natural; entra se houver tempo. |
| E7. Transversais | RNF-03, RNF-06 | Must | Interface responsiva e código modular, aplicados em todas as sprints. |

## 4. Plano de sprints

As datas serão fixadas na primeira Sprint Planning, a partir do prazo oficial de cada entrega. A ordem abaixo é a sequência prevista.

| Sprint | Foco | Resultado esperado |
|---|---|---|
| **1** | Fechar o **Documento** (etapas 7, 8 e 9) | Planejamento, diagrama de casos de uso e diagrama de classes aprovados. Fecha a Entrega 1. |
| **2** | **Protótipos** (etapas 10 e 11) | Telas em média fidelidade das jornadas principais e plano de teste dos protótipos. Fecha a Entrega 2. |
| **3** | **Sistema, base** (etapa 12) | Repositório estruturado, banco de dados, autenticação, perfil do freelancer (E1) e integração com a API de lugares (E2). |
| **4** | **Sistema, evidências** (etapa 12) | Varredura de sites, níveis de certeza, pontuação e ranking (E3). |
| **5** | **Sistema, IA** (etapa 12) | Explicação e rascunho de abordagem (E4), com as regras de integridade validadas. Fecha a Entrega 3. |
| **Extra** | Gestão da carteira e assistente | E5 e, se houver tempo, E6, além de ajustes finais. |

A sequência prioriza primeiro o que gera risco (integrações externas e IA) e deixa os itens `Should` e `Could` para o fim.

## 5. Tecnologias propostas

| Camada | Escolha | Motivo |
|---|---|---|
| Backend | Python 3.12 + FastAPI | API REST simples de construir, documentação automática e bom ecossistema para IA e análise de HTML. |
| Banco de dados | SQLite no desenvolvimento, com migrações (Alembic) e SQLAlchemy | Zero configuração para a equipe; permite migrar para PostgreSQL sem reescrever. |
| Frontend | React + Vite | Atende à aplicação web responsiva (RNF-03) e é amplamente documentado. |
| IA | API de um modelo de linguagem, acessada por uma camada própria | Isola o provedor para trocar sem afetar o sistema (RNF-04 e RNF-06). |
| Busca de empresas | API de lugares/mapas, acessada por uma camada própria | Mesmo motivo; permite substituir a fonte de dados. |
| Testes e qualidade | Pytest, Ruff e GitHub Actions | Testes automáticos e verificação de estilo a cada pull request. |
| Gestão | GitHub (issues, milestones e pull requests) | Já é usado pela equipe. |

> A stack é uma proposta e pode ser ajustada na primeira Sprint Planning, desde que a decisão seja registrada neste documento.

### Visão geral da arquitetura

```text
Navegador (React)
      ↓  HTTP/JSON
API FastAPI
  ├── Perfil e autenticação
  ├── Descoberta de empresas ──→ provedor de lugares
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
