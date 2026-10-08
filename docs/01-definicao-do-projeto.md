# 1. Definição do Projeto

> Issue #1 — explicação do que é e em que consiste o projeto.

## 1.1 O que é o LeadForge

O **LeadForge** é um **copiloto comercial para freelancers**: um sistema web que ajuda o profissional autônomo a descobrir quem pode precisar do seu serviço, entender *por que* aquela empresa é uma oportunidade e preparar a primeira abordagem comercial.

A ideia central pode ser resumida em uma frase:

> O freelancer informa o que sabe fazer, e o sistema encontra empresas que provavelmente precisam dessa habilidade, mostra as evidências que sustentam essa conclusão e ajuda a escrever a abordagem.

## 1.2 O problema que o projeto resolve

Freelancers gastam grande parte do tempo com uma tarefa que não é o seu ofício: **prospectar clientes**. Na prática, isso costuma acontecer de forma manual e desorganizada:

- pesquisa de empresas em mapas, redes sociais e buscadores, uma a uma;
- análise subjetiva ("acho que esse site está ruim") sem registro de evidências;
- planilhas soltas, sem histórico e sem priorização;
- mensagens genéricas, copiadas para dezenas de empresas, com baixa taxa de resposta.

As ferramentas tradicionais de prospecção respondem apenas a *"quem é a empresa e qual o contato"*. Falta responder a pergunta que realmente converte: ***"por que essa empresa precisa do meu serviço agora?"***.

## 1.3 No que o projeto consiste

O LeadForge organiza a prospecção em um fluxo único, do perfil do freelancer até a mensagem pronta para envio:

```text
Perfil do freelancer (habilidades, serviços, região)
        ↓
Descoberta de empresas por nicho + cidade
        ↓
Coleta de evidências públicas (ex.: análise do site da empresa)
        ↓
Avaliação da oportunidade, com nível de certeza
        ↓
Priorização (ranking) das oportunidades
        ↓
Assistente de IA: justificativa e rascunho de abordagem
        ↓
Exportação / acompanhamento do contato
```

Os principais componentes do sistema são:

| Componente | O que faz |
|---|---|
| **Perfil do freelancer** | Registra habilidades, serviços oferecidos e região de atuação, para evitar recomendações incompatíveis. |
| **Descoberta de empresas** | Busca negócios por nicho e localização em fontes de dados externas e remove duplicatas. |
| **Coleta de evidências** | Analisa informações públicas de cada empresa (por exemplo, se o site tem HTTPS, versão mobile, formulário de contato, botão de WhatsApp) e registra a origem de cada achado. |
| **Avaliação de oportunidade** | Transforma as evidências em uma pontuação e em problemas detectados, sempre indicando o grau de certeza. |
| **Assistente de IA** | Explica a oportunidade em linguagem simples e redige uma proposta de primeira mensagem, usando **somente dados reais já coletados**. |
| **Painel e exportação** | Lista e filtra oportunidades, acompanha o status de cada contato e exporta os dados (CSV/JSON). |

## 1.4 Integração com Inteligência Artificial

Por orientação da professora, o projeto incorpora IA como parte do produto, e não apenas como ferramenta de desenvolvimento. O uso de IA no LeadForge segue uma regra de integridade:

> A IA **organiza e explica** dados reais do sistema; ela **não inventa** empresas, contatos, problemas, preços ou evidências.

Na prática, a IA é usada para:

1. **Explicar a oportunidade** — traduz as evidências técnicas em um texto compreensível ("o site não é adaptado para celular e não tem botão de contato direto");
2. **Sugerir a abordagem** — gera um rascunho de mensagem personalizado, com base no perfil do freelancer e nas evidências da empresa, sempre editável pelo usuário;
3. **Responder perguntas sobre a carteira** (evolução prevista) — por exemplo, "quais empresas de Sorocaba têm maior chance de precisar de um site novo?", consultando os dados persistidos.

Para evitar conclusões falsas, cada achado recebe um nível de certeza:

| Nível | Significado |
|---|---|
| `confirmado` | Há evidência observável que sustenta a conclusão. |
| `sinal forte` | Há indício forte, mas sem confirmação direta. |
| `inferência` | Interpretação plausível a partir das evidências. |
| `desconhecido` | Não há informação suficiente — ausência de evidência não é evidência de ausência. |

## 1.5 Origem e evolução da ideia

O LeadForge nasceu como um projeto pessoal em desenvolvimento no repositório [`murilloalvz/leadforge-ai`](https://github.com/murilloalvz/leadforge-ai), que validou a viabilidade técnica da descoberta de empresas e da análise de sites. Este Trabalho de Conclusão de Curso **reaproveita a ideia de produto**, mas é um **novo projeto**, reconstruído do zero, com:

- processo de engenharia de software formal (levantamento de requisitos, modelagem UML, protótipos e implementação);
- integração com IA como requisito do produto;
- escopo definido e delimitado para o prazo do TCC (ver documento 2).

## 1.6 Objetivos

**Objetivo geral:** desenvolver um sistema web que auxilie freelancers a identificar e priorizar empresas com potencial de contratação, apoiando a abordagem comercial com explicações geradas por IA a partir de evidências públicas.

**Objetivos específicos:**

1. levantar e documentar os requisitos de negócio, funcionais e não funcionais do sistema;
2. modelar o sistema com diagramas de caso de uso e de classe;
3. prototipar as telas principais em média fidelidade e validá-las com usuários;
4. implementar o fluxo central: perfil → descoberta → evidências → avaliação → abordagem;
5. integrar um modelo de linguagem para explicar oportunidades e sugerir abordagens sem fabricar informações;
6. avaliar o sistema com potenciais usuários (freelancers).

## 1.7 Público-alvo

Freelancers e pequenos prestadores de serviço digital, como desenvolvedores web, designers, profissionais de social media, SEO, copywriting, gestão de tráfego e automação, que precisam captar clientes por conta própria.
