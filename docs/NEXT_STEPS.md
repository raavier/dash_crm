# Dashboard CRM - Próximos Passos e Contexto

## 📌 Status Atual do Projeto

### ✅ Completado
1. **Frontend React** - 100% implementado e funcionando
   - Localização: `frontend/`
   - Rodando em: `http://localhost:5175`
   - Tecnologias: React 18 + TypeScript + Vite + Chakra UI v2 + Recharts
   - Estado: Context API
   - Dados: Usando mocks temporários

2. **Documentação Completa**
   - [CLAUDE.md](CLAUDE.md) - Guia para Claude Code
   - [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Schema completo das tabelas CRM
   - [REFERENCES.md](REFERENCES.md) - Links e referências
   - [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Visão geral do projeto

### 🎯 Próximo Passo: Backend Python + Integração Databricks

## 📋 Contexto para Nova Sessão

### Informações do Databricks
- **Workspace**: `https://adb-116288240407984.4.azuredatabricks.net`
- **Cluster ID**: `0103-144058-4tvp4kpg`
- **Profile**: `ravi-local`
- **Catálogo**: `hs_franquia`
- **Schema**: `gold_connect_bot` (views), `silver_crm` (base)

### Tabelas Principais
1. `vw_crm_action` - Ações corretivas/preventivas
2. `vw_crm_verification` - Verificações de segurança
3. `vw_crm_verification_question` - Respostas dos checklists
4. `vw_crm_user` - Usuários (⚠️ usar `USER_ID` para JOINs, não `ID`)
5. `vw_crm_location` - Localizações hierárquicas
6. `vw_general_de_para_hier_org_unit` - Hierarquia organizacional

### Queries SQL Necessárias
Todas as queries estão documentadas em [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) seção "Queries para o Dashboard":

1. **Métricas principais** (verificações, controles, perguntas + % não conformes)
2. **Priorização de ações** (gráfico de barras: Vencidas, S=0 a S=4, Posterior)
3. **Lista de ações em aberto** (tabela com paginação)
4. **Opções de filtros** (organizações, localizações, tipos)

### Endpoints que o Backend Deve Expor

```python
# FastAPI ou Flask

POST /api/metrics
# Input: DashboardFilters (organization, location, verificationType, dateRange)
# Output: MetricsData { verifications, controls, questions }

POST /api/action-priorities
# Input: DashboardFilters
# Output: ActionPriority[] (category, count, color)

POST /api/actions
# Input: DashboardFilters + page number
# Output: PaginatedActions { data[], total, page, pageSize }

GET /api/filter-options
# Output: FilterOptions { organizations[], locations[], verificationTypes[] }
```

### Estrutura dos Dados (TypeScript Types)

Veja tipos completos em `frontend/src/types/dashboard.types.ts`

**Exemplo de MetricsData**:
```typescript
{
  verifications: { total: 316414, nonCompliant: 63705, percentage: 20.13 },
  controls: { total: 772899, nonCompliant: 70015, percentage: 9.06 },
  questions: { total: 3627949, nonCompliant: 89363, percentage: 2.46 }
}
```

**Exemplo de ActionPriority**:
```typescript
[
  { category: 'Vencidas', count: 133, color: '#BB133E' },
  { category: 'S=0', count: 97, color: '#E37222' },
  ...
]
```

## 🔧 Tarefas para o Backend

### 1. Setup do Projeto
```bash
cd backend/
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install fastapi uvicorn databricks-sql-connector python-dotenv pydantic
```

### 2. Estrutura Sugerida
```
backend/
├── main.py                 # FastAPI app
├── config.py              # Configurações Databricks
├── database.py            # Conexão Databricks SQL
├── models/
│   └── dashboard.py       # Pydantic models
├── services/
│   └── dashboard_service.py  # Lógica de queries
├── routes/
│   └── dashboard.py       # Endpoints REST
├── requirements.txt
└── .env                   # Credenciais (não commitar!)
```

### 3. Configuração Databricks

**arquivo `.env`**:
```env
DATABRICKS_HOST=https://adb-116288240407984.4.azuredatabricks.net
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/YOUR_WAREHOUSE_ID
DATABRICKS_TOKEN=YOUR_TOKEN_HERE
```

**Conexão com databricks-sql-connector**:
```python
from databricks import sql

connection = sql.connect(
    server_hostname=os.getenv("DATABRICKS_HOST").replace("https://", ""),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_TOKEN")
)
```

### 4. Exemplo de Query

Query para métricas (do DATABASE_SCHEMA.md):
```python
def get_metrics(filters):
    query = """
    SELECT
      COUNT(DISTINCT v.ID) as total_verificacoes,
      COUNT(DISTINCT CASE WHEN q.CRITICAL_CONTROL_NON_COMPLIANCE = 1 THEN v.ID END) as verificacoes_nao_conformes,
      ROUND(
        COUNT(DISTINCT CASE WHEN q.CRITICAL_CONTROL_NON_COMPLIANCE = 1 THEN v.ID END) * 100.0 /
        NULLIF(COUNT(DISTINCT v.ID), 0),
        2
      ) as percentual_nao_conforme
    FROM hs_franquia.gold_connect_bot.vw_crm_verification v
    LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_verification_question q
      ON v.ID = q.VERIFICATION_ID
    WHERE v.VERIFICATION_DATE BETWEEN :start_date AND :end_date
    """
    # Executar query...
```

### 5. CORS para Desenvolvimento

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔄 Integração Frontend → Backend

### Atualizar dashboardService.ts

Substituir mocks por chamadas reais:

```typescript
// frontend/src/services/dashboardService.ts
import api from './api';

export const dashboardService = {
  async getMetrics(filters: DashboardFilters): Promise<MetricsData> {
    const response = await api.post('/api/metrics', filters);
    return response.data;
  },
  // ... outros métodos
};
```

### Criar .env no Frontend

```env
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

## 📝 Arquivos Importantes para Consultar

1. **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Todas as queries SQL prontas
2. **[frontend/src/types/dashboard.types.ts](../frontend/src/types/dashboard.types.ts)** - Estrutura dos dados
3. **[frontend/src/services/dashboardService.ts](../frontend/src/services/dashboardService.ts)** - Ver dados mock atuais
4. **[docs/main.ipynb](main.ipynb)** - Notebook com conexão Databricks já configurada

## 🎯 Prompt Sugerido para Nova Sessão

```
Olá! Estou continuando o desenvolvimento do Dashboard CRM.

STATUS ATUAL:
- Frontend React completo e funcionando (localhost:5175)
- Usando dados mock temporários
- Toda documentação pronta em docs/

PRÓXIMO PASSO:
Criar o backend Python com FastAPI que:
1. Conecta ao Databricks SQL
2. Executa as queries documentadas em docs/DATABASE_SCHEMA.md
3. Expõe endpoints REST para o frontend consumir

CONTEXTO COMPLETO:
Veja docs/NEXT_STEPS.md para todos os detalhes.

Por favor, comece criando a estrutura do backend em backend/ com FastAPI + databricks-sql-connector.
```

## ⚠️ Notas Importantes

1. **USER_ID vs ID**: Sempre usar `USER_ID` (int) para JOINs em `vw_crm_user`, NUNCA `ID` (UUID)
2. **Filtros de Data**: Frontend envia dateRange como objetos Date ISO
3. **Paginação**: Frontend espera { data[], total, page, pageSize }
4. **Cores**: Backend deve retornar cores hex (#BB133E) no ActionPriority
5. **CORS**: Necessário para dev local frontend↔backend
6. **Autenticação**: Por enquanto, sem auth. Databricks token no backend .env

## 🚀 Ordem de Implementação Sugerida

1. ✅ Setup FastAPI + estrutura de pastas
2. ✅ Configurar conexão Databricks SQL
3. ✅ Implementar endpoint `/api/metrics`
4. ✅ Testar integração com frontend
5. ✅ Implementar `/api/action-priorities`
6. ✅ Implementar `/api/actions` (com paginação)
7. ✅ Implementar `/api/filter-options`
8. ✅ Tratamento de erros e logging
9. ✅ Deploy local e testes completos

## 📞 Chatbot (Fase Futura)

**Endpoint do chatbot Databricks**:
```
POST https://adb-116288240407984.4.azuredatabricks.net/serving-endpoints/connect_bot_prd/invocations

Headers:
  Authorization: Bearer {databricks_token}
  Content-Type: application/json

Body:
{
  "messages": [
    {"role": "user", "content": "Sua pergunta aqui"}
  ]
}
```

O chatbot será implementado como um widget embedded após o backend estar funcionando.

---

**Última atualização**: Dashboard frontend completo, pronto para integração backend.
**Próximo desenvolvedor**: Comece em `backend/` criando API REST com FastAPI.
