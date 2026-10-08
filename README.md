# LeadForge

**Copiloto comercial para freelancers** que transforma habilidades em oportunidades prospectadas e explicáveis.

O freelancer informa o que sabe fazer; o LeadForge descobre empresas que podem precisar desse serviço, coleta evidências públicas, avalia a oportunidade e usa IA para explicar o porquê e preparar a abordagem.

Projeto de Trabalho de Conclusão de Curso (TCC) de Análise e Desenvolvimento de Sistemas — FATEC Sorocaba. É uma nova implementação da ideia iniciada em [`leadforge-ai`](https://github.com/murilloalvz/leadforge-ai), agora com processo formal de engenharia de software e IA como parte do produto.

## O problema

Prospectar clientes é a parte mais cara do trabalho de quem é autônomo: pesquisa manual de empresas, análises sem registro, planilhas soltas e mensagens genéricas com pouca resposta.

As ferramentas de prospecção respondem *quem é a empresa e qual o contato*. O LeadForge tenta responder a pergunta que realmente importa: **por que essa empresa precisa do meu serviço?**

## Como funciona

```text
Perfil do freelancer + nicho + cidade
        ↓
Descoberta de empresas
        ↓
Evidências públicas (ex.: análise do site)
        ↓
Avaliação da oportunidade + nível de certeza
        ↓
Explicação e rascunho de abordagem com IA
        ↓
Acompanhamento e exportação
```

Cada conclusão do sistema recebe um nível de certeza, para não transformar falta de dado em afirmação falsa:

| Nível | Significado |
|---|---|
| `confirmado` | Há evidência observável |
| `sinal forte` | Indício forte, sem confirmação direta |
| `inferência` | Interpretação plausível das evidências |
| `desconhecido` | Informação insuficiente |

## Uso de IA no produto

A IA explica oportunidades e redige o rascunho da primeira mensagem. Ela trabalha só com dados reais do sistema: não inventa empresas, contatos, problemas ou evidências, e nenhuma mensagem é enviada sem revisão do usuário.

## Escopo

Dentro do escopo do TCC:

- módulo inicial de **desenvolvimento web**, para negócios locais;
- descoberta de empresas por nicho, cidade e UF;
- análise de sinais públicos do site;
- avaliação com nível de certeza e ranking;
- explicação e rascunho de abordagem por IA;
- status de contato e exportação em CSV/JSON.

Fora do escopo: envio automático de mensagens, precificação, propostas e demos, outras áreas de serviço e aplicativo móvel.

## Documentação

| Documento | Conteúdo |
|---|---|
| [Definição do Projeto](docs/01-definicao-do-projeto.md) | O que é e em que consiste o projeto |
| [Tema e Delimitação](docs/02-tema-e-delimitacao.md) | Descrição da aplicação, escopo e restrições |
| [Requisitos de Negócio](docs/03-requisitos-de-negocio.md) | Objetivos, entregas de valor e regras de negócio |

As próximas etapas (requisitos funcionais e não funcionais, diagramas, protótipos e implementação) são acompanhadas nas [issues](../../issues) do repositório.

## Estado atual

Fase de especificação. Ainda não há código; a stack será definida junto com o planejamento do projeto de software.

## Equipe

**Murillo Lourenço** ([@Skullo093](https://github.com/Skullo093)) e [@brunorw09](https://github.com/brunorw09)  
ADS — FATEC Sorocaba
