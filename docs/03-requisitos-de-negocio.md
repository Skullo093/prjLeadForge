# 3. Requisitos de Negócio

> Issue #3 — o que deve ser entregue para oferecer valor (o que vai ser o software final).

Requisitos de negócio descrevem **por que** o sistema existe e **qual valor** ele precisa entregar à organização/usuário. Os requisitos funcionais (issue #4) e não funcionais (issue #5) detalham *como* esse valor será entregue.

## 3.1 Contexto de negócio

O freelancer é, ao mesmo tempo, quem executa o serviço e quem vende. O gargalo do negócio dele é a **captação de clientes**: encontrar empresas certas, justificar a abordagem e fazer o primeiro contato consome tempo e costuma ter baixo retorno quando é feito de forma genérica.

## 3.2 Oportunidade e objetivos de negócio

| Código | Objetivo de negócio | Como o software gera valor |
|---|---|---|
| **OBJ-01** | Reduzir o tempo gasto com pesquisa de potenciais clientes. | Descoberta automática de empresas por nicho e cidade. |
| **OBJ-02** | Aumentar a qualidade das oportunidades abordadas. | Avaliação baseada em evidências reais, com nível de certeza e ranking. |
| **OBJ-03** | Aumentar a chance de resposta no primeiro contato. | Mensagem personalizada com o problema real detectado, gerada com apoio de IA. |
| **OBJ-04** | Dar confiança ao usuário nas conclusões do sistema. | Toda conclusão mostra a evidência de origem e o grau de certeza; a IA não inventa dados. |
| **OBJ-05** | Organizar a prospecção em um só lugar. | Lista de oportunidades com status de contato e exportação dos dados. |

## 3.3 Partes interessadas (stakeholders)

| Parte interessada | Interesse |
|---|---|
| **Freelancer (usuário principal)** | Encontrar clientes de forma rápida, organizada e com argumentos concretos. |
| **Empresa prospectada (impactado indireto)** | Receber contatos relevantes e honestos, baseados em informações públicas. |
| **Equipe de desenvolvimento do TCC** | Entregar um sistema funcional, documentado e dentro do prazo. |
| **Professores / banca avaliadora** | Verificar aplicação dos conceitos do curso, incluindo a integração com IA. |

## 3.4 O que o software final deve entregar (proposta de valor)

Para que o produto ofereça valor ao freelancer, o software final **deve entregar**:

| Código | Entrega de valor | Objetivo relacionado |
|---|---|---|
| **RN-01** | **Descoberta de empresas** por nicho e localização, sem resultados duplicados. | OBJ-01 |
| **RN-02** | **Análise de evidências públicas** das empresas (no escopo inicial, o site), registrando a origem de cada informação. | OBJ-02, OBJ-04 |
| **RN-03** | **Avaliação e ranking de oportunidades**, com pontuação e problemas detectados, indicando o nível de certeza de cada conclusão. | OBJ-02, OBJ-04 |
| **RN-04** | **Perfil do freelancer**, usado para que as oportunidades sejam compatíveis com o que ele oferece. | OBJ-02 |
| **RN-05** | **Explicação por IA** de cada oportunidade em linguagem simples, baseada apenas em dados do sistema. | OBJ-03, OBJ-04 |
| **RN-06** | **Rascunho de abordagem por IA**, personalizado e editável, para o freelancer enviar por conta própria. | OBJ-03 |
| **RN-07** | **Acompanhamento do contato**, com status por oportunidade (novo, contatado, respondeu, descartado). | OBJ-05 |
| **RN-08** | **Exportação dos dados** (CSV/JSON) para uso fora do sistema. | OBJ-05 |

## 3.5 Regras de negócio

| Código | Regra |
|---|---|
| **REG-01** | O sistema só pode utilizar informações **públicas** de empresas. |
| **REG-02** | Toda conclusão sobre uma empresa deve ter um nível de certeza: `confirmado`, `sinal forte`, `inferência` ou `desconhecido`. |
| **REG-03** | A **ausência de evidência não pode ser tratada como evidência de ausência**; nesse caso o resultado é `desconhecido`. |
| **REG-04** | A IA **não pode inventar** empresas, contatos, problemas, preços ou evidências; só pode redigir a partir de dados coletados. |
| **REG-05** | O sistema **não envia mensagens automaticamente**; a abordagem é sempre revisada e enviada pelo usuário. |
| **REG-06** | Uma mesma empresa não deve aparecer duplicada na carteira do usuário. |
| **REG-07** | Mensagens e conteúdos gerados por IA devem ser identificados como **sugestões** e permanecer editáveis. |
| **REG-08** | O tratamento de dados deve respeitar a LGPD, priorizando dados de pessoas jurídicas. |
| **REG-09** | Cada usuário acessa apenas a sua própria carteira de oportunidades. |

## 3.6 Indicadores de sucesso

| Indicador | Meta para o TCC |
|---|---|
| Tempo para obter uma lista priorizada de empresas para um nicho/cidade | Poucos minutos, contra horas na pesquisa manual. |
| Oportunidades com evidência registrada e nível de certeza | 100% das oportunidades exibidas. |
| Mensagens de IA sem informação fabricada, em revisão amostral | 100% das amostras revisadas. |
| Satisfação de freelancers que testarem o protótipo/sistema | Avaliação positiva (ex.: nota média ≥ 4 em 5) em questionário. |
| Fluxo completo (perfil → descoberta → avaliação → abordagem → exportação) funcionando | Concluído de ponta a ponta na demonstração final. |

## 3.7 Restrições e premissas de negócio

- O projeto é acadêmico, com prazo e equipe limitados, e por isso entrega um **único módulo de serviço (desenvolvimento web)**.
- Dependência de serviços externos (fonte de dados de empresas e modelo de linguagem), com custos e limites de uso que devem ser controlados.
- Premissa: freelancers desejam abordar clientes com base em evidências, e não por envio em massa.
- Fora do escopo de negócio: precificação, propostas, demos, envio automático e outras áreas de serviço (ver documento 2).

## 3.8 Visão do software final

> Um sistema web em que o freelancer cadastra o que sabe fazer, escolhe um nicho e uma cidade e recebe uma **lista priorizada de empresas** que provavelmente precisam do seu serviço — cada uma com **evidências, nível de certeza, explicação em linguagem simples e um rascunho de mensagem** gerado por IA, pronto para ser revisado e enviado por ele.
