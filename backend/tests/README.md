# Dashboard CRM API - Tests

Suite de testes automatizados para validar queries SQL, lógica de negócio e endpoints REST.

## 🧪 Estrutura dos Testes

```
tests/
├── conftest.py           # Fixtures compartilhadas (filtros 2025, etc.)
├── test_queries.py       # Testes de queries SQL diretas
├── test_service.py       # Testes da camada de serviço
├── test_api.py           # Testes dos endpoints REST
└── README.md            # Esta documentação
```

## 🎯 Tipos de Testes

### 1. Testes de Queries (test_queries.py)

Testa queries SQL diretamente no Databricks para validar:
- ✅ Total de verificações em 2025 = **316414**
- ✅ Contagem de controles não conformes
- ✅ Distribuição de prioridades de ações
- ✅ JOINs com usuários e localizações

**Exemplo:**
```python
def test_total_verifications_2025(self, filters_2025, expected_verifications_2025):
    """Valida que o total de verificações em 2025 = 316414"""
```

### 2. Testes de Serviço (test_service.py)

Testa a camada de negócio (services/dashboard_service.py):
- ✅ Cálculo correto de percentuais
- ✅ Transformação de dados (DB → Pydantic models)
- ✅ Paginação
- ✅ Aplicação de filtros

**Exemplo:**
```python
def test_get_metrics_2025(self, filters_2025, expected_verifications_2025):
    """Valida que get_metrics retorna estrutura correta com total = 316414"""
```

### 3. Testes de API (test_api.py)

Testa os endpoints REST usando FastAPI TestClient:
- ✅ Status codes corretos (200, 422, etc.)
- ✅ Estrutura de resposta JSON
- ✅ Validação de parâmetros
- ✅ CORS e headers

**Exemplo:**
```python
def test_metrics_endpoint_2025(self, client, expected_verifications_2025):
    """Valida POST /api/metrics retorna 200 e dados corretos"""
```

## 🚀 Executando os Testes

### Pré-requisitos

1. **Ambiente virtual ativado**:
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. **Dependências instaladas**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Arquivo .env configurado** com credenciais Databricks:
   ```env
   DATABRICKS_HOST=adb-116288240407984.4.azuredatabricks.net
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/YOUR_WAREHOUSE_ID
   DATABRICKS_TOKEN=YOUR_TOKEN_HERE
   ```

### Executar Todos os Testes

```bash
pytest
```

### Executar Testes Específicos

```bash
# Apenas testes de queries
pytest tests/test_queries.py

# Apenas testes de serviço
pytest tests/test_service.py

# Apenas testes de API
pytest tests/test_api.py

# Teste específico (total de verificações 2025)
pytest tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025

# Testes com output detalhado
pytest -v -s
```

### Executar com Marcadores

```bash
# Apenas testes rápidos (sem testes marcados como 'slow')
pytest -m "not slow"

# Apenas testes de integração
pytest -m integration

# Apenas testes unitários
pytest -m unit
```

## 📊 Exemplo de Saída

```
============================= test session starts ==============================
collected 15 items

tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025 PASSED
✓ Total verifications in 2025: 316414

tests/test_service.py::TestMetricsService::test_get_metrics_2025 PASSED
✓ Metrics for 2025:
  Verifications: 316414 total, 63705 non-compliant (20.13%)
  Controls: 772899 total, 70015 non-compliant (9.06%)

tests/test_api.py::TestMetricsEndpoint::test_metrics_endpoint_2025 PASSED
✓ POST /api/metrics (2025):
  Verifications: 316414 total, 20.13% non-compliant

============================== 15 passed in 12.34s ==============================
```

## ✅ Validações Principais

### Total de Verificações 2025

O teste mais importante valida que:
```python
assert result.verifications.total == 316414
```

Isso garante que:
- A query está corretamente filtrando por data
- O JOIN com outras tabelas não duplica registros
- A contagem DISTINCT está funcionando

### Percentuais de Não Conformidade

Valida que os cálculos estão corretos:
```python
percentage = round((nonCompliant * 100.0) / total, 2)
assert result.percentage == percentage
```

### Estrutura de Dados

Valida que os modelos Pydantic correspondem aos dados:
```python
assert isinstance(result, MetricsData)
assert result.verifications.total > 0
assert 0 <= result.verifications.percentage <= 100
```

## 🐛 Troubleshooting

### Erro de Conexão com Databricks

```
Error connecting to Databricks: ...
```

**Solução:**
- Verifique se o arquivo `.env` está configurado corretamente
- Teste a conexão usando `docs/main.ipynb`
- Verifique se o token não expirou

### Teste Falhou: Total Diferente de 316414

```
AssertionError: Expected 316414 verifications in 2025, but got XXXXX
```

**Possíveis causas:**
1. **Dados foram atualizados**: O valor 316414 era válido em uma data específica. Se os dados mudaram, atualize o valor esperado em `conftest.py`:
   ```python
   @pytest.fixture
   def expected_verifications_2025():
       return 316414  # Atualizar para novo valor
   ```

2. **Filtros incorretos**: Verifique se a query está usando o intervalo de datas correto (2025-01-01 a 2025-12-31)

3. **JOINs duplicando registros**: Verifique se está usando `COUNT(DISTINCT v.ID)`

### Testes Lentos

Se os testes estiverem demorando muito:

```bash
# Executar apenas testes rápidos
pytest -m "not slow"

# Limitar número de testes
pytest tests/test_api.py -k "health"
```

## 📝 Adicionando Novos Testes

### Padrão para Novos Testes

```python
def test_my_new_feature(self, filters_2025):
    """
    Descrição clara do que o teste valida.

    Validates:
    - Item 1
    - Item 2
    """
    # Arrange
    expected_value = 123

    # Act
    result = dashboard_service.get_something(filters_2025)

    # Assert
    assert result == expected_value, f"Expected {expected_value}, got {result}"

    # Print (opcional, para debug)
    print(f"✓ Test passed: {result}")
```

### Boas Práticas

1. **Nome descritivo**: `test_what_it_validates_when_condition`
2. **Docstring clara**: Explique o que está sendo validado
3. **Assertions específicas**: Use mensagens de erro descritivas
4. **Fixtures reutilizáveis**: Use fixtures do `conftest.py`
5. **Prints informativos**: Ajudam no debug e documentação visual

## 🔗 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [DATABASE_SCHEMA.md](../../docs/DATABASE_SCHEMA.md) - Queries SQL
- [dashboard_service.py](../services/dashboard_service.py) - Implementação

## 📞 Suporte

Se algum teste falhar inesperadamente:
1. Verifique se o backend está rodando: `python main.py`
2. Teste manualmente no Swagger: http://localhost:8000/docs
3. Verifique os logs do backend para mais detalhes
4. Compare com queries no notebook: `docs/main.ipynb`
