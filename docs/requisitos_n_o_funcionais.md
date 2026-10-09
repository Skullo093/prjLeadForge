## 4.3 Requisitos Não Funcionais (RNF)
Os requisitos não funcionais definem as qualidades sistêmicas, limitações e exigências operacionais que garantem o correto funcionamento do LeadForge:

| Código | Atributo / Categoria | Descrição do Requisito | Restrição Relacionada |
| :--- | :--- | :--- | :--- |
| **RNF-01** | Integridade de Dados (IA) | A IA é restrita ao papel de síntese; ela não deve gerar informações fictícias (alucinações). Todas as frases devem ser rastreáveis. | REG-04, OBJ-04 |
| **RNF-02** | Segurança e Privacidade | O sistema deve isolar as carteiras por usuário e atender às premissas da LGPD, armazenando preferencialmente dados públicos corporativos (PJ). | REG-08, REG-09 |
| **RNF-03** | Acessibilidade e Portabilidade | O software deve ser entregue como uma aplicação web responsiva compatível com os principais navegadores do mercado (Chrome, Edge, Firefox, Safari). | Seção 2.3.1 |
| **RNF-04** | Conectividade e Limites de API | As integrações com serviços externos de busca e LLM devem tratar limites de requisições (rate limit) e falhas de conexão de forma graciosa. | Seção 2.3.3 |
| **RNF-05** | Intervenção Humana Obrigatória | Nenhuma mensagem comercial pode ser transmitida automaticamente sem a expressa revisão e ação manual do usuário. | REG-05, REG-07 |
| **RNF-06** | Extensibilidade Modular | O código deve ser estruturado de forma desacoplada para permitir a adição posterior de novos módulos de serviço sem quebras na arquitetura. | Seção 2.3.1 |