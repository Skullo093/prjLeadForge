# 2. Requisitos de Software
**Issue #4 e #5** — detalhamento dos requisitos funcionais e não funcionais do sistema.

## 4.1 Visão Geral dos Requisitos
Os requisitos apresentados a seguir traduzem as necessidades do negócio (Issue #3) em especificações técnicas e comportamentais do software final, sob a ótica da Engenharia de Software. Eles foram divididos entre o comportamento direto do sistema (Requisitos Funcionais) e os seus critérios de qualidade e restrições operacionais (Requisitos Não Funcionais).

## 4.2 Requisitos Funcionais (RF)
Os requisitos funcionais descrevem todas as ações, fluxos de dados e comportamentos das funcionalidades que o LeadForge deve executar:

| Código | Nome do Requisito | Descrição | Origem (Regra / Objetivo) |
| :--- | :--- | :--- | :--- |
| **RF-01** | Manutenção do Perfil do Freelancer | Permitir que o usuário cadastre e edite suas habilidades, serviços (módulo web), localização e estilo de tom de comunicação. | RN-04, OBJ-02 |
| **RF-02** | Busca Externa de Negócios | Realizar pesquisas de empresas informando nicho de mercado, cidade e UF por meio de integração com API de lugares/mapas. | RN-01, OBJ-01 |
| **RF-03** | Deduplicação de Oportunidades | Identificar e mesclar/remover entradas duplicadas de uma mesma empresa na carteira do usuário. | REG-06, OBJ-01 |
| **RF-04** | Varredura de Evidências do Site | Coletar indicadores técnicos no site do cliente (existência de HTTPS, responsividade mobile, botão de WhatsApp, formulário e chamada para ação). | RN-02, REG-01 |
| **RF-05** | Classificação por Nível de Certeza | Atribuir um nível explícito (confirmado, sinal forte, inferência, desconhecido) a cada problema detectado no site. | REG-02, REG-03 |
| **RF-06** | Pontuação e Ranqueamento | Calcular a pontuação da oportunidade com base nas evidências coletadas e classificar a carteira da maior para a menor relevância. | RN-03, OBJ-02 |
| **RF-07** | Explicação de Oportunidades por IA | Gerar uma explicação sucinta e em linguagem acessível sobre a oportunidade usando exclusivamente os dados coletados. | RN-05, REG-04 |
| **RF-08** | Geração de Abordagem Comercial por IA | Criar um rascunho de mensagem de primeiro contato totalmente editável com base no perfil do usuário e nos dados da empresa. | RN-06, REG-05, REG-07 |
| **RF-09** | Assistente de Análise da Carteira | Permitir que o usuário consulte sua carteira de empresas por meio de perguntas em linguagem natural processadas pelo assistente de IA. | RN-05, OBJ-05 |
| **RF-10** | Gestão de Status do Contato | Oferecer interface para alteração do ciclo de vida do contato (novo, contatado, respondeu, descartado). | RN-07, OBJ-05 |
| **RF-11** | Exportação de Dados | Disponibilizar a exportação das oportunidades e evidências nos formatos de arquivo CSV e JSON. | RN-08, OBJ-05 |