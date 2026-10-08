# 2. Tema e Delimitação do Projeto de Software

> Issue #2 — breve descrição do que se trata a aplicação.

## 2.1 Tema

**Prospecção comercial assistida por inteligência artificial para freelancers.**

## 2.2 Descrição breve da aplicação

O **LeadForge** é uma aplicação web que ajuda freelancers a encontrar clientes. A partir das habilidades do profissional e de um nicho de mercado em uma cidade, o sistema descobre empresas, analisa informações públicas (como o site da empresa), identifica oportunidades de serviço com um nível de certeza explícito e usa IA para explicar cada oportunidade e sugerir uma mensagem de abordagem.

## 2.3 Delimitação do projeto

Como o produto completo é amplo, o TCC adota um **recorte** realista para o prazo disponível. A regra adotada é: *a visão pode ser grande, mas cada entrega precisa ser pequena, funcional e testável*.

### 2.3.1 O que está dentro do escopo

| Item | Delimitação |
|---|---|
| **Área de serviço** | Um módulo inicial: **desenvolvimento web** (sites e landing pages). A arquitetura deve permitir novos módulos no futuro, mas eles não serão implementados. |
| **Mercado-alvo** | Negócios locais (ex.: clínicas, academias, restaurantes, escritórios), em cidades brasileiras. |
| **Descoberta** | Busca de empresas por nicho + cidade + UF, com remoção de duplicatas, usando uma fonte de dados externa (API de mapas/lugares). |
| **Evidências** | Análise de sinais públicos e objetivos do site: HTTPS, adaptação a celular, formulário, WhatsApp/telefone, chamada para ação, informações de serviços e localização. |
| **Avaliação** | Pontuação da oportunidade, lista de problemas detectados e nível de certeza (`confirmado`, `sinal forte`, `inferência`, `desconhecido`). |
| **IA** | Explicação em linguagem natural da oportunidade e rascunho de mensagem de abordagem, baseados apenas nos dados coletados. |
| **Perfil do freelancer** | Cadastro simples de habilidades, serviços, região e tom de comunicação. |
| **Gestão básica** | Lista de oportunidades com filtros, status de contato (novo, contatado, respondeu, descartado) e exportação em CSV/JSON. |
| **Plataforma** | Aplicação web responsiva, acessada por navegador. |

### 2.3.2 O que está fora do escopo

- envio automático de mensagens (e-mail, WhatsApp ou redes sociais) — o sistema apenas **gera o rascunho**; o envio é sempre feito pelo usuário;
- precificação automática de projetos;
- geração de propostas comerciais completas e de demonstrações (demos) para o cliente;
- módulos para outras áreas além de desenvolvimento web (design, SEO, social media etc.);
- análise de redes sociais, avaliações de clientes ou dados não públicos;
- coleta de dados pessoais de pessoas físicas — o foco é em **informações públicas de empresas**;
- aplicativo móvel nativo;
- integração com CRMs externos;
- cobrança, planos pagos e múltiplos usuários com permissões complexas.

### 2.3.3 Restrições e premissas

- O sistema usa apenas **informações publicamente acessíveis**, respeitando os termos de uso das fontes de dados e as boas práticas de acesso (ex.: `robots.txt`, limites de requisição).
- A IA **não pode inventar** empresas, contatos, problemas ou evidências; todo texto gerado deve ser rastreável a dados do sistema.
- O usuário permanece no controle: nenhuma mensagem é enviada sem revisão humana.
- O projeto deve respeitar a **LGPD**: priorizar dados de pessoas jurídicas e evitar o armazenamento desnecessário de dados pessoais.
- O desenvolvimento é limitado ao calendário acadêmico do TCC, o que justifica o recorte em um único módulo de serviço.
- Dependência de serviços externos (API de lugares e API do modelo de linguagem), cujas chaves são configuradas por variáveis de ambiente.

## 2.4 Justificativa

A captação de clientes é uma das maiores dificuldades de quem trabalha por conta própria, e o tempo gasto nela é tempo não faturável. Automatizar a parte repetitiva da pesquisa e apoiar a redação da abordagem com IA — mantendo a transparência sobre as evidências — pode reduzir esse esforço e aumentar a qualidade do contato inicial com o cliente. O tema também reúne, em um único produto, conteúdos centrais do curso de Análise e Desenvolvimento de Sistemas: levantamento de requisitos, modelagem, banco de dados, desenvolvimento web, integração com APIs e aplicação prática de inteligência artificial.

## 2.5 Resultado esperado

Ao final do TCC, espera-se entregar:

1. **Documento** com a especificação do projeto (definição, requisitos, modelagem e planejamento);
2. **Protótipos** das telas principais em média fidelidade;
3. **Sistema** funcional cobrindo o fluxo: perfil → descoberta → evidências → avaliação → abordagem com IA → exportação.
