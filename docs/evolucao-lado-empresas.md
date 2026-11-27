# Evolução: o lado das empresas

> **Status:** proposta de evolução, ainda não implementada. Este documento registra a ideia, os requisitos, as telas e o plano para ela ser construída aos poucos.

## 1. A ideia

Hoje o LeadForge funciona em um só sentido: o **freelancer** procura **empresas** que provavelmente precisam do seu serviço. A evolução proposta é o sentido contrário:

> A **empresa** informa o próprio site, descobre o que precisa melhorar e recebe uma **vitrine de freelancers** que podem resolver cada ponto, com habilidades, serviços, trabalhos já feitos e localização. Ela escolhe com quem entrar em contato.

A ideia nasceu de uma sugestão feita na apresentação do sistema (30%): além do diferencial de achar empresas que não sabem que precisam do serviço, a plataforma poderia ser usada **também pelas empresas** para encontrar freelancers.

O mesmo motor de análise e o mesmo princípio sustentam os dois lados: **mostrar o que se sabe e o nível de certeza de cada achado**.

## 2. Os dois lados do produto

| | Lado do freelancer (já existe) | Lado da empresa (proposto) |
|---|---|---|
| Quem começa | O freelancer | A empresa |
| Ponto de partida | Nicho e cidade | O site da própria empresa |
| O sistema entrega | Ranking de empresas com brechas | Diagnóstico e vitrine de freelancers |
| Quem escolhe | O freelancer escolhe quem abordar | A empresa escolhe quem contatar |

## 3. Fluxo da empresa

```text
Empresa informa o site e a cidade
        ↓
Diagnóstico: o que o site tem de problema, com nível de certeza
        ↓
Cada problema vira uma necessidade (um serviço)
        ↓
Vitrine de freelancers que oferecem esses serviços
        ↓
A empresa compara os perfis e demonstra interesse
        ↓
O freelancer recebe o interesse e responde
```

## 4. O que já existe e será reaproveitado

| Peça atual | Uso no lado da empresa |
|---|---|
| Análise do site (5 evidências) | O diagnóstico do site da própria empresa |
| Níveis de certeza | A empresa também vê o que é confirmado e o que é só um sinal |
| Pontuação | Vira uma nota de saúde digital do site |
| Perfil do freelancer (habilidades, serviços, cidade) | A base da vitrine |
| Contas com dados isolados por usuário | A base das contas de empresa |

## 5. Do problema ao serviço

A recomendação de freelancers parte de uma tabela simples, que liga cada problema encontrado ao serviço que o resolve:

| Problema encontrado | Necessidade da empresa | Serviço do freelancer |
|---|---|---|
| Sem site encontrado | Ter um site | Criação de site |
| Sem versão para celular | Site que funcione no celular | Redesign de site |
| Sem HTTPS | Site seguro | Redesign de site |
| Sem botão de WhatsApp | Contato direto com clientes | Landing page |
| Sem formulário de contato | Receber pedidos de orçamento | Landing page |
| Sem chamada para ação clara | Converter visitantes em clientes | Landing page |
| Site inacessível | Recuperar o site | Redesign de site |

Os serviços acompanham os do perfil atual (Criação de site, Landing page, Redesign de site e Loja virtual). Quando surgirem novas análises (seção 11), a tabela ganha novas linhas.

## 6. A vitrine de freelancers

Para cada freelancer recomendado, a vitrine mostra:

| Informação | Origem |
|---|---|
| Nome e apresentação | Perfil público (novo) |
| Habilidades | Já existe no perfil |
| Serviços que presta | Já existe no perfil |
| Localização | Já existe no perfil |
| Trabalhos já feitos (portfólio) | **Novo**: projetos com título, descrição e link |
| Disponibilidade | **Novo** |

**Ordem de recomendação:** primeiro quem oferece os serviços de que a empresa precisa; depois a proximidade (mesma cidade ou região), as habilidades e o portfólio verificado.

### Selos de transparência
A vitrine segue a mesma filosofia do produto, de dizer o que se sabe:

| Selo | Significa |
|---|---|
| **Informado** | O freelancer disse que fez o projeto, e o sistema não verificou |
| **Verificado** | O sistema abriu o link do projeto e confirmou que o site está no ar (por exemplo, com HTTPS e versão para celular) |

## 7. Requisitos propostos

A numeração continua a dos [requisitos funcionais](requisitos_funcionais.md) e [não funcionais](requisitos_n_o_funcionais.md) existentes.

### Funcionais

| Código | Requisito | Prioridade |
|---|---|---|
| RF-12 | Cadastro e login de empresa | Must |
| RF-13 | A empresa solicitar o diagnóstico do próprio site | Must |
| RF-14 | Traduzir os problemas encontrados em necessidades (serviços) | Must |
| RF-15 | Vitrine de freelancers recomendados por necessidade e localização | Must |
| RF-16 | Portfólio do freelancer (projetos realizados, com link) | Should |
| RF-17 | Perfil público do freelancer, opcional e com consentimento | Must |
| RF-18 | A empresa demonstrar interesse em um freelancer | Should |
| RF-19 | Verificação automática dos projetos do portfólio | Could |

### Não funcionais

| Código | Requisito | Prioridade |
|---|---|---|
| RNF-07 | Privacidade e consentimento: só aparece na vitrine quem escolheu aparecer, e só com os dados necessários (LGPD) | Must |
| RNF-08 | Transparência da verificação: sempre indicar se uma informação foi informada ou verificada | Should |
| RNF-09 | Prevenção de abuso: limite de pedidos de contato e canal de denúncia | Could |

### Regras de negócio

| Código | Regra |
|---|---|
| REG-10 | Um freelancer só aparece na vitrine se tiver ativado o perfil público. |
| REG-11 | O contato entre empresa e freelancer é mediado pela plataforma, sem expor e-mail ou telefone antes do aceite. |
| REG-12 | A plataforma mostra informações e verificações, mas não garante a qualidade do serviço. |
| REG-13 | O diagnóstico usa apenas informações públicas do site informado. |
| REG-14 | Uma empresa que pede diagnóstico só passa a ser oportunidade para freelancers se aceitar isso explicitamente. |
| REG-15 | Itens do portfólio sempre aparecem com o selo Informado ou Verificado. |

## 8. Telas propostas

**Lado da empresa**

| Tela | O que faz |
|---|---|
| Cadastro e entrada da empresa | Conta com nome, e-mail, cidade e site |
| Diagnóstico do meu site | Campo para a URL e botão de analisar, com andamento |
| Resultado do diagnóstico | Nota de saúde digital, problemas com nível de certeza e as necessidades |
| Vitrine de freelancers | Cartões com habilidades, serviços, cidade e selos, com filtros |
| Perfil do freelancer (visão da empresa) | Apresentação, portfólio com selos e botão de interesse |
| Pedido de contato | Mensagem curta, enviada pela plataforma |

**Lado do freelancer (novas)**

| Tela | O que faz |
|---|---|
| Portfólio | Cadastro e edição de projetos, com link |
| Perfil público | Ativar ou desativar a aparição na vitrine e ver como fica |
| Interesses recebidos | Lista de empresas interessadas, com opção de responder ou recusar |

## 9. Modelo de dados proposto

| Entidade | Situação | Campos principais |
|---|---|---|
| `Usuario` | Alterar | Novo campo `tipo` (freelancer ou empresa) |
| `PerfilFreelancer` | Alterar | Novos: `visivel` (perfil público), `apresentacao`, `disponibilidade` |
| `PerfilEmpresa` | Nova | nome, cidade, estado, `url_site` e segmento |
| `Diagnostico` | Nova | empresa, URL analisada, pontuação e data |
| `Evidencia` | Generalizar | Hoje liga-se à empresa prospectada; passa a poder ligar-se a um diagnóstico |
| `Necessidade` | Nova | diagnóstico, serviço, problema de origem e prioridade |
| `Projeto` | Nova | freelancer, título, descrição, link, serviços e `verificacao` (informado ou verificado) |
| `Interesse` | Nova | diagnóstico, freelancer, mensagem e status (enviado, visto, respondido ou recusado) |

**Decisão de projeto:** a análise do site é a mesma nos dois lados. O ideal é manter um só motor (`analisar_site`) e generalizar de quem são as evidências, em vez de duplicar o código.

## 10. Análises possíveis do site da empresa

| Análise | Situação | Observação |
|---|---|---|
| HTTPS, celular, WhatsApp, formulário e chamada para ação | Já existe | |
| Título e descrição da página, título principal (H1) e texto alternativo das imagens | Fácil de acrescentar | Ajudam no Google; abre um novo serviço, o de SEO |
| Telefone e endereço visíveis e coerentes com o cadastro do mapa | Médio | |
| Tempo de carregamento | Mais trabalhoso | Exige um navegador automatizado |
| Análise do JavaScript (página renderizada) | Mais trabalhoso | Reduz falsos alarmes em sites feitos com JavaScript |

## 11. Riscos e cuidados

| Tema | Cuidado |
|---|---|
| LGPD | Mostrar perfis é tratar dados pessoais: consentimento, só o necessário e possibilidade de sair a qualquer momento. |
| Spam e golpes | Contato mediado, limite de pedidos e canal de denúncia. |
| Qualidade do portfólio | Selos Informado e Verificado, e nenhuma promessa de qualidade. |
| Conflito entre os lados | Empresa que pede diagnóstico só vira oportunidade se aceitar (REG-14). |
| Escala | Se houver muitos usuários, a busca e a análise passam a precisar de fila de tarefas e de PostgreSQL. |
| Escopo | Trata-se, na prática, de um segundo produto. Convém entregar por marcos pequenos. |

## 12. Marcos sugeridos (sem datas)

| Marco | Conteúdo | Depende de |
|---|---|---|
| M1 | Portfólio e perfil público do freelancer (RF-16 e RF-17) | — |
| M2 | Conta de empresa e diagnóstico do próprio site (RF-12 e RF-13) | — |
| M3 | Necessidades e vitrine recomendada (RF-14 e RF-15) | M1 e M2 |
| M4 | Interesse e contato mediado (RF-18) | M3 |
| M5 | Verificação do portfólio (RF-19) | M1 |
| Em paralelo | Protótipos das telas da empresa e teste com empresas reais | — |

O M1 e o M2 são independentes e podem andar ao mesmo tempo.

## 13. Perguntas em aberto

1. O contato será uma mensagem dentro da plataforma ou a empresa recebe o contato do freelancer após o aceite?
2. Haverá avaliações de empresas sobre freelancers?
3. Como confirmar que quem pede o diagnóstico é de fato a empresa dona do site?
4. A plataforma terá algum modelo de receita (por exemplo, destaque na vitrine) ou continuará gratuita?
5. A vitrine será restrita à região da empresa ou aberta a freelancers remotos?
6. Empresas sem site também poderão pedir diagnóstico (por exemplo, só informando o nome e a cidade)?

## 14. Como contar a ideia

> "O LeadForge passa a ter dois lados. O freelancer encontra empresas que precisam do seu serviço, e a empresa descobre o que precisa melhorar e recebe uma vitrine de freelancers para resolver. O mesmo motor de análise sustenta os dois lados, e o mesmo princípio vale para ambos: mostrar o que se sabe e o nível de certeza."
