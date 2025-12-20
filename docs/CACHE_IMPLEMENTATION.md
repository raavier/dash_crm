# Backend Cache Implementation

Implementação completa de cache in-memory para o Dashboard CRM API.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Como Funciona](#como-funciona)
4. [Endpoints de Cache](#endpoints-de-cache)
5. [Configuração](#configuração)
6. [Monitoramento](#monitoramento)
7. [Troubleshooting](#troubleshooting)

---

## Visão Geral

### Objetivo
Reduzir queries ao Databricks através de cache in-memory com TTL automático.

### Benefícios
- **Redução de custo**: 80-90% menos queries ao Databricks
- **Performance**: Response time <100ms (vs 2-5s sem cache)
- **Escalabilidade**: Suporta milhares de requests simultâneos
- **Simplicidade**: Zero dependências externas (não precisa de Redis)

### Tecnologia
- **Biblioteca**: `cachetools` (Python)
- **Estratégia**: TTLCache (time-to-live)
- **TTL padrão**: 4 horas
- **Maxsize**: 1000 itens

---

## Arquitetura

### Fluxo de Request

```
┌─────────────────────────────────────────┐
│ Frontend (React)                         │
│ - Envia request para /api/metrics       │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│ FastAPI Route (/api/metrics)            │
│ - Recebe filtros do usuário             │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│ Dashboard Service (@cached)             │
│ - Verifica se resultado está em cache   │
└─────────────────────────────────────────┘
         ↓                         ↓
    CACHE HIT                  CACHE MISS
         ↓                         ↓
┌──────────────────┐    ┌──────────────────┐
│ Return cached    │    │ Query Databricks │
│ result (~10ms)   │    │ (~2-5 segundos)  │
└──────────────────┘    └──────────────────┘
                                ↓
                    ┌──────────────────────┐
                    │ Store result in cache│
                    │ (TTL = 4 hours)      │
                    └──────────────────────┘
```

### Cache Hit Rate Esperado
- **Primeiro request**: MISS (executa query)
- **Requests subsequentes (< 4h)**: HIT (retorna do cache)
- **Taxa esperada**: 95%+ de cache hits

---

## Como Funciona

### 1. Decorador @cached

Todas as funções principais do `dashboard_service.py` usam o decorador `@cached`:

```python
@cached
def get_metrics(self, filters: DashboardFilters) -> MetricsData:
    # Query ao Databricks
    result = db.execute_query(query, params)
    return result
```

### 2. Geração de Cache Key

O cache gera uma chave única baseada em:
- Nome da função
- Argumentos (filtros, paginação, etc.)

Exemplo de chave:
```
md5("get_metrics|org=Vale|location=Sao Paulo|startDate=2025-01-01...")
→ "a3f2b8c1d4e5f6g7h8i9j0k1l2m3n4o5"
```

### 3. TTL Automático

Após 4 horas, o item expira automaticamente e é removido do cache.

### 4. Cache LRU

Se o cache atingir 1000 itens (maxsize), os itens mais antigos são removidos automaticamente.

---

## Endpoints de Cache

### GET /api/cache/stats

Retorna estatísticas do cache.

**Response:**
```json
{
  "status": "ok",
  "cache": {
    "size": 45,
    "maxsize": 1000,
    "ttl": 14400,
    "ttl_hours": 4.0
  }
}
```

### POST /api/cache/clear

Limpa todo o cache.

⚠️ **ATENÇÃO**: Próximas requests vão bater no Databricks!

**Response:**
```json
{
  "status": "success",
  "message": "Cache cleared successfully",
  "warning": "Next requests will hit the database"
}
```

**Quando usar:**
- Após refresh do Databricks Job (6h AM)
- Quando detectar dados desatualizados
- Para testes

### POST /api/cache/invalidate?pattern=get_metrics

Invalida apenas chaves que contêm o pattern.

**Query params:**
- `pattern` (required): String para buscar nas chaves

**Exemplos:**
```bash
# Invalidar apenas cache de métricas
POST /api/cache/invalidate?pattern=get_metrics

# Invalidar apenas cache de ações
POST /api/cache/invalidate?pattern=get_actions

# Invalidar cache de filtros
POST /api/cache/invalidate?pattern=get_filter_options
```

**Response:**
```json
{
  "status": "success",
  "pattern": "get_metrics",
  "keys_deleted": 12,
  "message": "Invalidated 12 cache keys matching pattern 'get_metrics'"
}
```

---

## Configuração

### Variáveis de Ambiente (.env)

```bash
# Cache settings (opcional - tem defaults)
CACHE_ENABLED=true
CACHE_TTL=14400     # 4 horas em segundos
CACHE_MAXSIZE=1000  # Máximo de itens no cache
```

### Backend (config.py)

```python
class Settings(BaseSettings):
    cache_enabled: bool = True
    cache_ttl: int = 14400  # 4 hours
    cache_maxsize: int = 1000
```

### Ajustar TTL

Para ajustar o TTL sem reiniciar servidor:

```python
# backend/cache.py (linha 133)
cache = DashboardCache(maxsize=1000, ttl=7200)  # 2 horas
```

Recomendações de TTL:
- **Dados estáveis**: 6-8 horas
- **Dados atualizados 1x/dia**: 4 horas (padrão)
- **Dados frequentes**: 1-2 horas
- **Dados em tempo real**: Não usar cache (ou 5-10 minutos)

---

## Monitoramento

### Logs

O cache emite logs para cada operação:

```
INFO: Cache HIT for get_metrics
INFO: Cache MISS for get_metrics - executing query
INFO: Cache SET: a3f2b8c1d4e5f6g7...
INFO: Cache CLEARED
```

### Métricas Recomendadas

Adicionar ao monitoramento:

1. **Cache hit rate**: % de requests que usaram cache
2. **Cache size**: Número de itens no cache
3. **Average response time**: Latência média das APIs
4. **Databricks query count**: Quantidade de queries executadas

### Query de Validação

```python
# Testar cache funcionando
import requests

# Primeiro request (CACHE MISS)
start = time.time()
r1 = requests.post('http://localhost:8000/api/metrics', json={...})
time1 = time.time() - start
print(f"Request 1 (MISS): {time1:.2f}s")  # ~2-5s

# Segundo request (CACHE HIT)
start = time.time()
r2 = requests.post('http://localhost:8000/api/metrics', json={...})
time2 = time.time() - start
print(f"Request 2 (HIT): {time2:.3f}s")   # ~0.010-0.050s

# Verificar que resultados são iguais
assert r1.json() == r2.json()
print("✓ Cache funcionando!")
```

---

## Troubleshooting

### Problema 1: Cache não está funcionando

**Sintomas**: Todos requests batem no Databricks (logs mostram sempre MISS)

**Possíveis causas:**
1. `cache_enabled=False` no config
2. Filtros mudando a cada request (gerando chaves diferentes)
3. Cache foi limpo recentemente

**Solução:**
```bash
# Verificar stats
curl http://localhost:8000/api/cache/stats

# Verificar logs
# Deve aparecer "Cache HIT" após primeiro request
```

### Problema 2: Dados desatualizados no cache

**Sintomas**: Dashboard mostra dados antigos após refresh do Databricks Job

**Solução:**
```bash
# Opção 1: Limpar todo cache
curl -X POST http://localhost:8000/api/cache/clear

# Opção 2: Invalidar apenas métricas
curl -X POST "http://localhost:8000/api/cache/invalidate?pattern=get_metrics"
```

**Automação recomendada:**
Adicionar step no Databricks Job que chama `/api/cache/clear` após refresh:

```python
# No final do script de refresh (04_refresh_daily_materialized_tables.sql)
# Adicionar notificação via webhook para limpar cache
```

### Problema 3: Cache crescendo muito (memory leak)

**Sintomas**: Uso de memória do servidor crescendo constantemente

**Causa**: Maxsize muito alto ou TTL muito longo

**Solução:**
```python
# Reduzir maxsize
cache = DashboardCache(maxsize=500, ttl=7200)  # 500 itens, 2h TTL

# Ou reiniciar servidor periodicamente (ex: 1x/dia)
```

### Problema 4: Performance não melhorou

**Sintomas**: Response time ainda alto mesmo com cache

**Diagnóstico:**
```bash
# Verificar hit rate
curl http://localhost:8000/api/cache/stats

# Se size=0 ou size muito baixo → cache não está sendo usado
# Se size alto mas requests lentos → problema não é cache
```

**Possíveis causas:**
- Filtros muito variados (cada combinação = chave diferente)
- TTL muito curto (cache expirando rápido)
- Queries do Databricks ainda lentas (verificar materialized tables)

---

## Migração para Redis (Futuro)

Se precisar de cache compartilhado entre múltiplos servidores:

1. **Instalar Redis**:
```bash
pip install redis
```

2. **Criar RedisCache** (similar a DashboardCache):
```python
import redis

class RedisCache:
    def __init__(self, host='localhost', port=6379, ttl=14400):
        self.client = redis.Redis(host=host, port=port)
        self.ttl = ttl
```

3. **Substituir cache global**:
```python
# backend/cache.py
cache = RedisCache(host='redis-server', ttl=14400)
```

**Quando migrar para Redis:**
- Deploy com múltiplos servidores (horizontal scaling)
- Precisa de cache persistente (sobrevive a restarts)
- Precisa de features avançadas (pub/sub, cache invalidation distribuído)

---

## Resumo de Benefícios

### Antes (Sem Cache)
- **Queries por dia**: 10.000+ (1000 usuários × 10 refreshes)
- **Response time**: 2-5 segundos
- **Custo**: ~$3.000/mês

### Depois (Com Cache)
- **Cache hit rate**: 95%+
- **Queries por dia**: ~500 (apenas cache misses)
- **Response time**: <100ms (cache hit)
- **Custo**: ~$200/mês + cache
- **ECONOMIA**: ~93% (~$2.800/mês)

### Performance Esperada

| Métrica | Sem Cache | Com Cache | Melhoria |
|---------|-----------|-----------|----------|
| Response time | 2-5s | <100ms | **20-50x** |
| Queries/dia | 10.000 | ~500 | **95% redução** |
| Custo/mês | $3.000 | $200 | **93% economia** |
| Concurrent users | ~100 | 1000+ | **10x escalabilidade** |

---

## Checklist de Validação

Após implementar cache:

- [ ] `cachetools` instalado no requirements.txt
- [ ] `cache.py` criado com `DashboardCache` e `@cached`
- [ ] Todas as 4 funções principais têm `@cached`
- [ ] Endpoints `/api/cache/*` funcionando
- [ ] Logs mostram "Cache HIT" após primeiro request
- [ ] `/api/cache/stats` retorna `size > 0`
- [ ] Performance melhorou (requests <100ms)
- [ ] Cache expira após 4 horas (TTL funcionando)

---

**Última atualização**: 2025-12-20
**Versão**: 1.0
