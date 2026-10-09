# LeadForge

Sistema web que ajuda freelancers a encontrar clientes. Você diz o que sabe fazer, e o LeadForge procura empresas que provavelmente precisam do seu serviço, mostra as evidências por trás de cada conclusão e ajuda a escrever a primeira mensagem.

> Projeto em fase inicial. Por enquanto estamos na parte de documentação e planejamento, ainda não há código.

## Por que o LeadForge

Quem trabalha por conta própria gasta muito tempo prospectando: procura empresa uma a uma, anota tudo em planilhas soltas, avalia site "no olho" e acaba mandando a mesma mensagem genérica para todo mundo.

As ferramentas de prospecção em geral dizem quem é a empresa e qual o contato. O LeadForge tenta responder o que realmente importa na hora de abordar alguém: **por que essa empresa precisa do meu serviço?**

## Como vai funcionar

```text
Perfil do freelancer + nicho + cidade
        ↓
Descoberta de empresas
        ↓
Evidências públicas (por exemplo, análise do site)
        ↓
Avaliação da oportunidade + nível de certeza
        ↓
Explicação e rascunho de abordagem com IA
        ↓
Acompanhamento e exportação
```

Duas regras guiam o produto:

- **Nada de dado inventado.** Cada conclusão mostra de onde veio e recebe um nível de certeza: `confirmado`, `sinal forte`, `inferência` ou `desconhecido`. Falta de informação não vira afirmação.
- **A IA só trabalha com dados reais.** Ela explica a oportunidade e redige o rascunho da mensagem a partir do que o sistema coletou. Nada é enviado sem o usuário revisar.

## Escopo da primeira versão

Começamos por um módulo só, o de **desenvolvimento web** (sites e landing pages), voltado a negócios locais como clínicas, academias e restaurantes. Ficam de fora, por enquanto, envio automático de mensagens, precificação, geração de propostas e outras áreas de serviço. Os detalhes estão em [`docs/02-tema-e-delimitacao.md`](docs/02-tema-e-delimitacao.md).

## Etapas do projeto

Cada etapa tem uma issue neste repositório, e o que já foi escrito fica na pasta [`docs/`](docs).

| # | Etapa | Entrega |
|---|---|---|
| 1 | Definição do projeto ([doc](docs/01-definicao-do-projeto.md)) | 1 · Documento |
| 2 | Tema e delimitação do projeto de software ([doc](docs/02-tema-e-delimitacao.md)) | 1 · Documento |
| 3 | Requisitos de negócio ([doc](docs/03-requisitos-de-negocio.md)) | 1 · Documento |
| 4 | Requisitos funcionais | 1 · Documento |
| 5 | Requisitos não funcionais | 1 · Documento |
| 6 | Escolha do modelo de software ([doc](docs/Escolha%20do%20modelo%20de%20Software.md)) | 1 · Documento |
| 7 | Planejamento do projeto de software | 1 · Documento |
| 8 | Diagramas de uso | 1 · Documento |
| 9 | Diagramas de classe | 1 · Documento |
| 10 | Protótipos das telas em média fidelidade | 2 · Protótipos |
| 11 | Escolha do modo de testar a prototipação, a partir do contexto de uso | 2 · Protótipos |
| 12 | Desenvolvimento de 30% dos protótipos em sistema | 3 · Sistema |

## Entregas

1. **Documento:** definição, requisitos, modelo de desenvolvimento, planejamento e diagramas (etapas 1 a 9).
2. **Protótipos:** telas em média fidelidade e a forma de testá-las (etapas 10 e 11).
3. **Sistema:** implementação de 30% dos protótipos (etapa 12).

## Como trabalhamos

Usamos Scrum, com ciclos curtos e entregas incrementais. Os motivos da escolha estão em [`docs/Escolha do modelo de Software.md`](docs/Escolha%20do%20modelo%20de%20Software.md). A stack será definida no planejamento (etapa 7).

## Equipe

- Murillo Lourenço
- Allan Batista
- Bruno Rocha

Análise e Desenvolvimento de Sistemas, FATEC Sorocaba.
