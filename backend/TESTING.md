# Guia Rápido de Testes

## 🎯 Teste Principal: Total de Verificações 2025

O teste mais importante valida que o total de verificações em 2025 é **316414**.

### Executar o Teste

```bash
# Windows
run_tests.bat verifications

# Linux/Mac
./run_tests.sh verifications

# Ou diretamente
pytest tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025 -v -s
```

### Saída Esperada

```
tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025 PASSED
✓ Total verifications in 2025: 316414
```

### Se o Teste Falhar

```
AssertionError: Expected 316414 verifications in 2025, but got XXXXX
```

**Possíveis causas:**

1. **Dados atualizados**: O número mudou porque novos dados foram inseridos ou removidos
   - **Solução**: Atualize o valor esperado em `tests/conftest.py`:
     ```python
     @pytest.fixture
     def expected_verifications_2025():
         return XXXXX  # Novo valor obtido
     ```

2. **Query incorreta**: A query não está filtrando corretamente
   - Verifique o intervalo de datas: `2025-01-01` a `2025-12-31`
   - Verifique se está usando `COUNT(DISTINCT v.ID)`

3. **Conexão com Databricks**: Problemas de conectividade
   - Verifique arquivo `.env`
   - Teste conexão usando `docs/main.ipynb`

## 📊 Outros Testes Importantes

### Testar Todos os Endpoints da API

```bash
run_tests.bat api
```

Valida:
- POST /api/metrics
- POST /api/action-priorities
- POST /api/actions
- GET /api/filter-options
- GET /api/health

### Testar Cálculos de Percentual

```bash
pytest tests/test_service.py::TestMetricsService::test_get_metrics_percentages_calculation -v
```

Valida que: `percentage = round((nonCompliant / total) * 100, 2)`

### Testar Paginação

```bash
pytest tests/test_service.py::TestActionsService -v
```

Valida:
- Página 1 com 10 itens
- Página 2 com 10 itens
- Page size customizado

## 🚀 Quick Start

1. **Configure o ambiente**:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edite .env com suas credenciais
   ```

2. **Execute o teste principal**:
   ```bash
   run_tests.bat verifications
   ```

3. **Se passou**: ✅ Queries estão corretas!

4. **Se falhou**: Veja seção "Se o Teste Falhar" acima

## 📝 Estrutura dos Testes

```
tests/
├── conftest.py              # Valor esperado: 316414
├── test_queries.py          # Query SQL direta
├── test_service.py          # Serviço (get_metrics)
└── test_api.py              # Endpoint (POST /api/metrics)
```

Cada nível testa uma camada diferente:
- **Queries**: SQL direto no Databricks
- **Service**: Lógica de transformação
- **API**: Endpoint REST completo

## 🔍 Debug

### Ver Output Detalhado

```bash
pytest tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025 -v -s
```

Flag `-s` mostra os prints do teste.

### Ver Query Executada

Adicione logging em `database.py`:
```python
logger.info(f"Query: {query}")
logger.info(f"Parameters: {parameters}")
```

### Testar Query Manualmente

Copie a query de `test_queries.py` e execute no notebook `docs/main.ipynb`.

## 📚 Mais Informações

- **Documentação completa**: [tests/README.md](tests/README.md)
- **Queries SQL**: [docs/DATABASE_SCHEMA.md](../docs/DATABASE_SCHEMA.md)
- **Service layer**: [services/dashboard_service.py](services/dashboard_service.py)
