# Dashboard CRM - Control Risk Management

Sistema de dashboard para visualização e gestão de dados do processo CRM (Control Risk Management) com chatbot integrado, deployado no Databricks Apps.

## 📁 Estrutura do Projeto

```
dash_crm/
├── docs/                   # Documentação do projeto
│   ├── CLAUDE.md          # Guia para Claude Code
│   ├── PROJECT_OVERVIEW.md # Visão geral e objetivos
│   ├── REFERENCES.md       # Referências e boilerplates
│   ├── DATABASE_SCHEMA.md  # Documentação completa das tabelas CRM
│   ├── NEXT_STEPS.md      # Contexto e próximos passos
│   ├── main.ipynb         # Notebook para consultas Databricks
│   └── crm_table_metadata.csv # Metadados das tabelas
│
├── frontend/               # ✅ Aplicação React (Dashboard)
│   ├── src/               # Código-fonte React + TypeScript
│   ├── public/            # Assets estáticos
│   └── package.json       # Dependências Node.js
│
├── backend/                # ✅ Backend FastAPI + Databricks
│   ├── main.py            # Aplicação FastAPI
│   ├── config.py          # Configurações
│   ├── database.py        # Conexão Databricks SQL
│   ├── models/            # Pydantic models
│   ├── services/          # Lógica de negócio e queries
│   ├── routes/            # Endpoints REST
│   └── requirements.txt   # Dependências Python
│
├── requirements.txt        # Dependências Python (projeto geral)
└── databricks.yml         # Configuração Databricks Apps
```

## 🚀 Tecnologias

- **Frontend**: React (Dashboard customizado + Chatbot widget)
- **Backend**: Python (Databricks)
- **Deployment**: Databricks Apps
- **Database**: Databricks SQL (Catálogo: hs_franquia)

## 📚 Documentação

- **[CLAUDE.md](docs/CLAUDE.md)** - Instruções para Claude Code trabalhar no projeto
- **[PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** - Objetivos e contexto do projeto
- **[REFERENCES.md](docs/REFERENCES.md)** - Links para templates e referências
- **[DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)** - Estrutura completa das tabelas CRM

## 🎯 Funcionalidades

### Dashboard
- Visualização de métricas de verificações, controles e perguntas
- Gráfico de priorização de ações (S=0 a S=4 + Vencidas)
- Tabela de ações em aberto
- Filtros por organização, localização, tipo de verificação e data

### Chatbot
- Widget embedded (canto inferior direito)
- Botão circular flutuante
- Integração com endpoint Databricks
- Conversação sobre dados CRM

## 🔗 Endpoints

**Chatbot**: `https://adb-116288240407984.4.azuredatabricks.net/serving-endpoints/connect_bot_prd/invocations`

## 📊 Tabelas Principais

- `vw_crm_action` - Ações corretivas e preventivas
- `vw_crm_verification` - Verificações de segurança
- `vw_crm_verification_question` - Respostas dos checklists
- `vw_crm_user` - Usuários do sistema
- `vw_crm_location` - Localizações e hierarquia geográfica
- `vw_general_de_para_hier_org_unit` - Hierarquia organizacional

Consulte [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) para detalhes completos.

## 🛠️ Desenvolvimento

### Backend (FastAPI + Databricks)

```bash
cd backend

# Criar ambiente virtual e instalar dependências
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Configurar .env (copiar de .env.example)
cp .env.example .env
# Editar .env com suas credenciais Databricks

# Executar servidor
python main.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Frontend (React + TypeScript)

```bash
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
# Dashboard: http://localhost:5175
```

### Databricks Notebook

```bash
# Executar notebook de exploração
jupyter notebook docs/main.ipynb
```

## 🚀 Quick Start

1. **Backend**: Configure o `.env` e execute `python backend/main.py`
2. **Frontend**: Execute `npm run dev` na pasta `frontend/`
3. Acesse http://localhost:5175 para ver o dashboard

## 📝 Status do Projeto

- [x] Documentação completa das tabelas CRM
- [x] Frontend React com dashboard interativo
- [x] Backend FastAPI com integração Databricks
- [x] Queries SQL otimizadas para todas as visualizações
- [ ] Integração frontend ↔ backend (próximo passo)
- [ ] Widget do chatbot embedded
- [ ] Deploy no Databricks Apps

## 📚 Documentação Detalhada

- **Backend**: [backend/README.md](backend/README.md)
- **Próximos Passos**: [docs/NEXT_STEPS.md](docs/NEXT_STEPS.md)
- **Database Schema**: [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)
