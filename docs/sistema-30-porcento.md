# Sistema: 30% dos protótipos implementados

Documento da etapa 12. Descreve o que foi implementado, como executar, como cada requisito foi atendido e o que ainda não faz parte desta entrega.

## 1. Escopo implementado

O planejamento ([`planejamento_do_projeto.md`](planejamento_do_projeto.md)) definiu o **fluxo mínimo ponta a ponta** como recorte dos 30%: cadastro e login, perfil, busca de empresas e lista de oportunidades com ranking. Esse fluxo cobre 5 das 8 telas distintas do protótipo, ou seja, mais que o mínimo de 30%, porque as telas de busca e de lista só fazem sentido juntas.

| Tela do protótipo | Rota | Situação |
|---|---|---|
| Entrar | `/entrar` | Implementada |
| Criar conta | `/criar-conta` | Implementada |
| Perfil | `/perfil` | Implementada |
| Nova busca (formulário, buscando, resultado e erro) | `/nova-busca` | Implementada, com os 4 estados |
| Oportunidades (lista com ranking e filtros) | `/oportunidades` | Implementada, com detalhe das evidências |
| Carteira (quadro por status) | — | Próxima etapa (RF-10) |
| Assistente | — | Próxima etapa (RF-09) |
| Exportar dados | — | Próxima etapa (RF-11); o botão aparece desabilitado |

O detalhe da oportunidade (janela com as evidências e o nível de certeza) não estava na lista de telas da especificação, mas foi incluído porque é por ele que o usuário confere **por que** uma empresa é uma oportunidade.

## 2. Requisitos atendidos

| Requisito | Situação | Como foi atendido |
|---|---|---|
| RF-01 Perfil do freelancer | Atendido | Cadastro e login, e edição de nome, e-mail, habilidades, serviços, localização e tom de comunicação. |
| RF-02 Busca externa de negócios | Atendido | Busca por nicho, cidade e UF pela API Geoapify, atrás da interface `PlacesProvider`. |
| RF-03 Deduplicação | Atendido | Por identificador da fonte e por nome e endereço, dentro do lote e contra a carteira do usuário. |
| RF-04 Varredura de evidências | Parcial | HTTPS, versão para celular, WhatsApp, formulário de contato e chamada para ação. |
| RF-05 Nível de certeza | Atendido | `confirmado`, `sinal forte`, `inferência` e `desconhecido` em cada evidência. |
| RF-06 Pontuação e ranking | Atendido | Pontuação de 0 a 100 e lista ordenada da maior para a menor. |
| RNF-02 Segurança e privacidade | Atendido | Cada usuário só acessa os próprios dados; senhas com scrypt; aceite de LGPD no cadastro; só dados públicos de empresas. |
| RNF-03 Aplicação web responsiva | Atendido | Layout adaptado para celular, com navegação inferior. |
| RNF-04 Limites e falhas das APIs | Atendido | Repetição automática em falhas temporárias, tratamento de limite de requisições e de chave inválida, e tela de erro com código. |
| RNF-06 Extensibilidade modular | Atendido | Fonte de empresas e buscador de sites ficam atrás de interfaces e podem ser trocados. |
| RF-07 a RF-11, RNF-01 e RNF-05 | Fora desta entrega | Dependem da IA, da carteira e da exportação, previstos para depois dos 30%. Nenhuma mensagem é gerada nem enviada. |

## 3. Como executar

Pré-requisitos: Python 3.11 ou superior e Node.js 20 ou superior.

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # no Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env               # opcional; ajuste a chave secreta
alembic upgrade head               # cria o banco SQLite
uvicorn app.main:app --reload      # http://localhost:8000 (documentação em /docs)
```

**Frontend**

```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

O frontend encaminha `/api` para o backend. Se o backend estiver em outro endereço, use `VITE_BACKEND_URL`.

**Modos de operação** (`LEADFORGE_MODE`)

| Modo | O que faz | Quando usar |
|---|---|---|
| `demo` | Empresas e sites simulados, sem chaves nem internet. A cidade "Erro" simula uma falha da fonte de dados. | Demonstração e desenvolvimento. |
| `live` | Busca no Geoapify e análise real do HTML dos sites. Exige `LEADFORGE_GEOAPIFY_API_KEY`. | Uso real. |
| `auto` (padrão) | `live` se houver chave do Geoapify, senão `demo`. | — |

A chave do Geoapify fica apenas em variável de ambiente e nunca vai para o repositório.

## 4. Arquitetura

```text
frontend/ (React + Vite + TypeScript)
  src/pages/        telas: Entrar, CriarConta, Perfil, NovaBusca, Oportunidades
  src/components/   layout, selos de certeza, detalhe da oportunidade
  src/api.ts        cliente da API
backend/ (FastAPI + SQLAlchemy + Alembic)
  app/routers/      rotas: auth, perfil, buscas, oportunidades
  app/services/
    discovery/      fonte de empresas (Geoapify e demo) atrás de PlacesProvider
    site_analysis/  buscador HTTP seguro, análise do HTML e fonte demo
    scoring.py      pontuação e ranking
    busca_runner.py processamento da busca em segundo plano
  alembic/          migrações do banco
```

**Fluxo de uma busca:** o usuário envia nicho, cidade e UF; a API cria a busca e responde na hora; o processamento roda em segundo plano nas etapas **buscando empresas → removendo duplicatas → analisando sites**; a tela consulta o andamento a cada segundo até o resultado ou o erro. A busca pode ser cancelada.

### API

| Método e rota | Função |
|---|---|
| `POST /auth/cadastro` · `POST /auth/login` · `GET /auth/eu` | Conta e sessão |
| `GET /perfil` · `PUT /perfil` | Perfil do freelancer |
| `POST /buscas` · `GET /buscas/{id}` · `POST /buscas/{id}/cancelar` | Busca de empresas e andamento |
| `GET /oportunidades` | Lista ordenada, com filtros `q`, `status_contato` e `nivel_certeza` |
| `GET /oportunidades/{id}` | Detalhe com as evidências |

## 5. Regras da análise

**Níveis de certeza.** Ausência de informação nunca vira afirmação:

| Situação | Nível |
|---|---|
| A URL do site é `http` (sem HTTPS) | Confirmado |
| Algo está presente no HTML (viewport, link de WhatsApp, formulário) | Confirmado |
| Algo está ausente no HTML estático (pode ser carregado por JavaScript) | Sinal forte |
| Chamada para ação (identificada por palavras-chave) | Inferência |
| Empresa sem site, ou site que não pôde ser acessado | Desconhecido |

**Pontuação.** Soma do peso de cada problema, reduzido pelo nível de certeza, limitada a 100:

| Problema | Peso |
|---|---|
| Sem site encontrado | 80 |
| Sem versão para celular | 35 |
| Sem HTTPS | 25 |
| Sem botão de WhatsApp | 20 |
| Sem formulário de contato | 15 |
| Sem chamada para ação | 10 |
| Site inacessível | 40 |

Multiplicadores: confirmado 1,0; sinal forte 0,85; inferência 0,6; desconhecido 0,8.

**Acesso aos sites.** O buscador só aceita `http` e `https`, bloqueia endereços que não sejam públicos (proteção contra SSRF, inclusive em redirecionamentos), respeita o `robots.txt`, limita tempo, tamanho e número de redirecionamentos e se identifica com um User-Agent próprio.

## 6. Modelo de dados

O banco segue o [diagrama de classes](Diagrams/class-diagram.plant) (`PerfilFreelancer`, `Empresa`, `Evidencia`, `Oportunidade`), com estes acréscimos necessários à implementação:

| Acréscimo | Motivo |
|---|---|
| `Usuario` | Login e isolamento dos dados por usuário (RNF-02). |
| `Busca` | Guardar o andamento e o resultado do processamento em segundo plano. |
| `Evidencia.indica_problema` | Separar o que é problema do que é só observação. |
| `TipoEvidencia.DISPONIBILIDADE_SITE` | Registrar "site não encontrado" ou "inacessível" como `desconhecido`. |

`SugestaoAbordagem`, `AssistenteIA` e `ServicoExportacao` ficam para a etapa seguinte.

## 7. Testes e verificação

| Verificação | Resultado |
|---|---|
| Testes do backend (`pytest`) | 79 testes: autenticação, perfil, busca completa, deduplicação, isolamento entre usuários, análise de HTML, pontuação, proteção SSRF, `robots.txt`, Geoapify com respostas simuladas |
| Testes do frontend (`npm test`) | 21 testes: login, cadastro, lista e filtros, detalhe, os 4 estados da busca, perfil |
| Lint e tipos | `ruff` no backend e `tsc` no frontend, sem erros |
| Migração | `alembic upgrade head` e `downgrade base` executam em banco novo |
| Fluxo ponta a ponta no navegador | Percorrido em modo `demo`: cadastro, perfil, busca (com repetição para testar duplicadas e com falha simulada), ranking, filtros, detalhe, sessão após recarregar e layout no celular |

O CI do repositório (`.github/workflows/ci.yml`) executa essas verificações a cada pull request.

## 8. Limitações conhecidas

- A integração com o Geoapify e a análise de sites reais (modo `live`) foram testadas com respostas simuladas. Ainda falta validá-las com uma chave real e com sites públicos.
- Na verificação de endereços, o nome do site é resolvido uma vez para a checagem e outra pela conexão. Para um uso em produção, convém fixar o IP resolvido.
- O token de acesso fica no navegador (`localStorage` ou `sessionStorage`) e não há limite de tentativas de login.
- O acompanhamento da busca é feito por consultas periódicas, e o processamento roda no próprio servidor da API. Para volumes maiores, seria preciso uma fila de tarefas.
- O SQLite atende ao desenvolvimento e à demonstração; para vários usuários simultâneos, a troca para PostgreSQL é indicada (já prevista no planejamento).

## 9. Próximos passos

Os itens abaixo ficam para depois dos 30%, na ordem de prioridade do planejamento: gestão de status do contato e exportação (RF-10 e RF-11), explicação e rascunho de abordagem por IA (RF-07, RF-08, RNF-01 e RNF-05) e assistente de análise da carteira (RF-09).
