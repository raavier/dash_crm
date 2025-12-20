# Dashboard CRM - Backend API

Backend FastAPI que conecta ao Databricks SQL e fornece endpoints REST para o frontend React.

## 🚀 Setup Rápido

### 1. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
DATABRICKS_HOST=adb-116288240407984.4.azuredatabricks.net
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/YOUR_WAREHOUSE_ID
DATABRICKS_TOKEN=YOUR_TOKEN_HERE

API_HOST=0.0.0.0
API_PORT=8000

FRONTEND_URL=http://localhost:5175
```

**Como obter as credenciais:**

1. **DATABRICKS_HTTP_PATH**: No Databricks, vá em SQL Warehouses → Seu Warehouse → Connection Details → HTTP Path
2. **DATABRICKS_TOKEN**: Settings → Developer → Access Tokens → Generate New Token

### 4. Executar o Servidor

```bash
# Modo desenvolvimento (com reload automático)
python main.py

# Ou usando uvicorn diretamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Documentação Interativa**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Estrutura do Projeto

```
backend/
├── main.py                   # FastAPI app principal
├── config.py                # Configurações e variáveis de ambiente
├── database.py              # Conexão Databricks SQL
├── requirements.txt         # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
├── models/
│   └── dashboard.py        # Pydantic models (request/response)
├── services/
│   └── dashboard_service.py  # Lógica de negócio e queries SQL
└── routes/
    └── dashboard.py        # Endpoints REST
```

## 🔌 Endpoints da API

### POST /api/metrics
Retorna as métricas principais (verificações, controles, perguntas).

**Request:**
```json
{
  "organization": "Nome da UO",
  "location": "Nome do Local",
  "verificationType": "Manager Verification",
  "dateRange": {
    "start": "2025-01-01",
    "end": "2025-12-31"
  }
}
```

**Response:**
```json
{
  "verifications": { "total": 316414, "nonCompliant": 63705, "percentage": 20.13 },
  "controls": { "total": 772899, "nonCompliant": 70015, "percentage": 9.06 },
  "questions": { "total": 3627949, "nonCompliant": 89363, "percentage": 2.46 }
}
```

### POST /api/action-priorities
Retorna a distribuição de prioridades das ações.

**Response:**
```json
[
  { "category": "Vencidas", "count": 133, "color": "#BB133E" },
  { "category": "S=0", "count": 97, "color": "#E37222" },
  { "category": "S=1", "count": 245, "color": "#F4A100" }
]
```

### POST /api/actions?page=1&page_size=10
Retorna lista paginada de ações em aberto.

**Response:**
```json
{
  "data": [
    {
      "id": "uuid-da-acao",
      "verificationId": "uuid-da-verificacao",
      "responsible": "Nome do Responsável",
      "dueDate": "2025-12-31",
      "status": "Atrasado",
      "type": "System or Process"
    }
  ],
  "total": 1543,
  "page": 1,
  "pageSize": 10
}
```

### GET /api/filter-options
Retorna opções disponíveis para os filtros.

**Response:**
```json
{
  "organizations": [
    { "value": "UO Nome", "label": "UO Nome" }
  ],
  "locations": [
    { "value": "Local Nome", "label": "Local Nome" }
  ],
  "verificationTypes": [
    { "value": "Manager Verification", "label": "Manager Verification" }
  ]
}
```

### GET /api/health
Health check do serviço.

## 🧪 Testes Automatizados

### Executar Todos os Testes

```bash
# Usando o script
run_tests.bat  # Windows
# ./run_tests.sh  # Linux/Mac

# Ou diretamente com pytest
pytest -v
```

### Executar Testes Específicos

```bash
# Teste de total de verificações 2025 = 316414
run_tests.bat verifications

# Apenas testes de queries SQL
run_tests.bat queries

# Apenas testes de serviço
run_tests.bat service

# Apenas testes de API
run_tests.bat api

# Teste específico
pytest tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025 -v -s
```

### O que é Testado

1. **Queries SQL diretas** (test_queries.py)
   - ✅ Total de verificações 2025 = **316414**
   - ✅ Contagem de controles não conformes
   - ✅ Distribuição de prioridades de ações
   - ✅ JOINs com usuários

2. **Camada de serviço** (test_service.py)
   - ✅ Cálculo de percentuais
   - ✅ Transformação de dados
   - ✅ Paginação
   - ✅ Filtros

3. **Endpoints REST** (test_api.py)
   - ✅ Status codes
   - ✅ Estrutura de resposta JSON
   - ✅ Validação de parâmetros

Veja documentação completa em [tests/README.md](tests/README.md)

## 🧪 Testando a API Manualmente

### Usando a Documentação Interativa

Acesse http://localhost:8000/docs para testar todos os endpoints diretamente no navegador.

### Usando cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Obter métricas
curl -X POST http://localhost:8000/api/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "dateRange": {
      "start": "2025-01-01",
      "end": "2025-12-31"
    }
  }'

# Obter opções de filtros
curl http://localhost:8000/api/filter-options
```

## 🔧 Desenvolvimento

### Logs

Os logs aparecem no console com informações detalhadas sobre:
- Conexões com Databricks
- Queries SQL executadas
- Tempo de resposta
- Erros e exceções

### Estrutura de Dados

Os modelos Pydantic em `models/dashboard.py` correspondem aos tipos TypeScript do frontend em `frontend/src/types/dashboard.types.ts`.

### Queries SQL

Todas as queries estão implementadas em `services/dashboard_service.py` e seguem as especificações de `docs/DATABASE_SCHEMA.md`.

## 📊 Dados do Databricks

**Catálogo**: `hs_franquia`
**Schema**: `gold_connect_bot`

**Tabelas principais:**
- `vw_crm_verification` - Verificações de segurança
- `vw_crm_verification_question` - Respostas dos checklists
- `vw_crm_action` - Ações corretivas/preventivas
- `vw_crm_user` - Usuários
- `vw_crm_location` - Localizações
- `vw_general_de_para_hier_org_unit` - Hierarquia organizacional

## ⚠️ Notas Importantes

1. **USER_ID**: Sempre usar `USER_ID` (int) para JOINs em `vw_crm_user`, NUNCA `ID` (UUID)
2. **Filtros Opcionais**: Todos os filtros são opcionais exceto `dateRange`
3. **CORS**: Configurado para aceitar requisições do frontend em localhost:5175
4. **Paginação**: Default é 10 itens por página, máximo 100

## 🐛 Troubleshooting

### Erro de Conexão com Databricks

```
Error connecting to Databricks: ...
```

**Solução:**
1. Verifique se o `DATABRICKS_TOKEN` está correto
2. Verifique se o `DATABRICKS_HTTP_PATH` está correto (inclui o warehouse ID)
3. Teste a conexão usando o notebook `docs/main.ipynb`

### Erro de Permissão

```
Permission denied on table/view ...
```

**Solução:**
Verifique se seu usuário tem permissão de leitura nas views do schema `gold_connect_bot`.

### CORS Error no Frontend

```
Access to fetch at ... has been blocked by CORS policy
```

**Solução:**
Verifique se a URL do frontend em `.env` está correta (`FRONTEND_URL=http://localhost:5175`).

## 📚 Documentação Adicional

- [DATABASE_SCHEMA.md](../docs/DATABASE_SCHEMA.md) - Schema completo das tabelas
- [NEXT_STEPS.md](../docs/NEXT_STEPS.md) - Contexto e próximos passos
- [CLAUDE.md](../docs/CLAUDE.md) - Guia para Claude Code
