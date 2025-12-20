# Dashboard CRM - Project Overview

## Objetivo

Criar um dashboard interativo para visualização e gestão de dados do processo CRM (Control Risk Management) - um sistema de segurança ocupacional - com chatbot integrado.

## Contexto

Sistema de gestão de segurança ocupacional que permite:
- Visualização de métricas e KPIs de segurança
- Análise de riscos e incidentes
- Interação via chatbot para consultas e insights
- Gestão de processos de controle de risco

## Stack Tecnológico

### Frontend
- **Framework**: React
- **Deployment**: Databricks Apps
- **Funcionalidades**:
  - Dashboard com visualizações de dados CRM
  - Interface de chatbot integrada
  - Comunicação com backend via REST APIs

### Backend
- **Linguagem**: Python
- **Ambiente**: Databricks (100% do backend roda no Databricks)
- **Funcionalidades**:
  - Processamento de dados das tabelas CRM
  - Endpoint do chatbot
  - Queries no Databricks SQL
  - APIs REST para o frontend

## Estrutura Inicial Planejada

### Frontend (a receber)
- Boilerplate React inicial
- Componentes de dashboard
- Interface do chatbot

### Backend (a receber)
- Estrutura das tabelas CRM
- Endpoint do chatbot
- Configuração Databricks Apps

## Próximos Passos

1. Receber e integrar boilerplate do frontend React
2. Receber estrutura das tabelas CRM
3. Implementar endpoint do chatbot
4. Configurar deployment no Databricks Apps
5. Integrar frontend com backend
6. Testes e ajustes finais

## Deployment

Todo o sistema será deployado como um Databricks App, utilizando a infraestrutura e recursos do Databricks para:
- Hospedagem da aplicação
- Processamento de dados
- Queries SQL
- Autenticação e autorização
- Recursos de AI/ML para o chatbot

## Considerações Importantes

- Backend deve ser 100% compatível com ambiente Databricks
- Utilizar Databricks SDK para Python nas integrações
- Aproveitar recursos nativos do Databricks (SQL, ML, etc.)
- Seguir best practices de segurança ocupacional na apresentação dos dados
