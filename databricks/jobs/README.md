# Materialized Tables - Databricks Jobs Setup

Documentação completa para criação e configuração das tabelas materializadas do Dashboard CRM.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquivos SQL](#arquivos-sql)
3. [Setup Inicial - Criação das Tabelas](#setup-inicial---criação-das-tabelas)
4. [Configuração do Databricks Job](#configuração-do-databricks-job)
5. [Monitoramento e Troubleshooting](#monitoramento-e-troubleshooting)
6. [Custos Estimados](#custos-estimados)

---

## Visão Geral

### Objetivo
Reduzir custos de queries no Databricks através de tabelas materializadas que são atualizadas 1x ao dia.

### Benefícios
- **Redução de custo**: ~93% de economia (~$2.800/mês)
- **Performance**: Queries 20-50x mais rápidas
- **Escalabilidade**: Suporta milhares de usuários simultâneos

### Arquitetura
```
┌─────────────────────────────────────────┐
│ Views Originais (leitura 1x/dia)        │
│ - vw_crm_verification                   │
│ - vw_crm_verification_question          │
│ - vw_crm_action                         │
└─────────────────────────────────────────┘
                ↓ (Job diário 6h AM)
┌─────────────────────────────────────────┐
│ Tabelas Materializadas (agregadas)      │
│ - crm_metrics_daily                     │
│ - crm_action_priorities_daily           │
│ - crm_actions_open_snapshot             │
└─────────────────────────────────────────┘
                ↓ (API consulta)
┌─────────────────────────────────────────┐
│ Backend Cache (95%+ hit rate)           │
│ - TTL: 4-6 horas                        │
└─────────────────────────────────────────┘
```

---

## Arquivos SQL

### 1. `01_create_crm_metrics_daily.sql`
**Tabela**: `hs_franquia.gold_connect_bot.crm_metrics_daily`

**Descrição**: Métricas agregadas por dia/organização/localização
- Total de verificações e não-conformes
- Total de controles críticos e não-conformes
- Total de perguntas e não-conformes

**Particionamento**: Por `data_referencia`

**Tamanho estimado**: ~10-50 MB por mês

---

### 2. `02_create_crm_action_priorities_daily.sql`
**Tabela**: `hs_franquia.gold_connect_bot.crm_action_priorities_daily`

**Descrição**: Distribuição de ações abertas por categoria de prioridade
- Vencidas, S=0, S=1, S=2, S=3, S=4, Posterior a S=4

**Particionamento**: Por `data_referencia`

**Tamanho estimado**: ~5-10 MB por mês

---

### 3. `03_create_crm_actions_open_snapshot.sql`
**Tabela**: `hs_franquia.gold_connect_bot.crm_actions_open_snapshot`

**Descrição**: Snapshot diário completo de todas as ações abertas
- ID, responsável, vencimento, status, tipo
- Usado para listagem paginada no dashboard

**Particionamento**: Por `data_snapshot`

**Tamanho estimado**: ~50-100 MB por mês

---

### 4. `04_refresh_daily_materialized_tables.sql`
**Descrição**: Script de refresh diário executado pelo Databricks Job

**Estratégias de refresh**:
1. **crm_metrics_daily**: DELETE + INSERT incremental (últimos 7 dias)
2. **crm_action_priorities_daily**: DELETE + INSERT snapshot diário
3. **crm_actions_open_snapshot**: DELETE + INSERT snapshot diário

**Limpeza automática**: Remove dados > 90 dias

**Tempo estimado**: 5-10 minutos

---

## Setup Inicial - Criação das Tabelas

### Passo 1: Executar Scripts de Criação

Acesse o Databricks SQL Editor e execute os scripts na ordem:

```bash
# 1. Criar tabela de métricas
01_create_crm_metrics_daily.sql

# 2. Criar tabela de prioridades
02_create_crm_action_priorities_daily.sql

# 3. Criar tabela de ações
03_create_crm_actions_open_snapshot.sql
```

### Passo 2: Verificar Criação

Após executar cada script, verificar:

```sql
-- Verificar tabelas criadas
SHOW TABLES IN hs_franquia.gold_connect_bot LIKE 'crm_*';

-- Verificar dados
SELECT COUNT(*) FROM hs_franquia.gold_connect_bot.crm_metrics_daily;
SELECT COUNT(*) FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily;
SELECT COUNT(*) FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot;
```

### Passo 3: Validar Particionamento

```sql
-- Verificar partições
DESCRIBE EXTENDED hs_franquia.gold_connect_bot.crm_metrics_daily;
```

---

## Configuração do Databricks Job

### Opção A: Via Interface Web (Recomendado)

1. **Acessar Databricks Workflows**
   - Ir para: `Workflows` → `Jobs` → `Create Job`

2. **Configurar Job Básico**
   - **Nome**: `CRM Dashboard - Daily Refresh Materialized Tables`
   - **Descrição**: `Atualização diária das tabelas materializadas do dashboard CRM`

3. **Adicionar Task**
   - **Task name**: `refresh_crm_materialized_tables`
   - **Type**: `SQL`
   - **SQL warehouse**: Selecionar warehouse de produção
   - **SQL file**: Copiar conteúdo de `04_refresh_daily_materialized_tables.sql`
   - **Timeout**: `30 minutes`

4. **Configurar Schedule**
   - **Trigger type**: `Scheduled`
   - **Schedule**: `Cron expression`
   - **Cron**: `0 6 * * *` (diário às 6h AM - horário do cluster)
   - **Timezone**: `America/Sao_Paulo` (ou timezone local)
   - **Pause schedule**: Desativado

5. **Configurar Alertas**
   - **Email on failure**: Adicionar e-mails dos responsáveis
   - **Email on success**: Opcional (apenas para primeiras execuções)

6. **Configurar Retry**
   - **Max retries**: `2`
   - **Min retry interval**: `5 minutes`

### Opção B: Via API (Terraform/Programático)

```python
import requests
import json

databricks_token = "YOUR_TOKEN"
databricks_host = "https://your-workspace.databricks.com"

job_config = {
    "name": "CRM Dashboard - Daily Refresh Materialized Tables",
    "tasks": [
        {
            "task_key": "refresh_crm_materialized_tables",
            "sql_task": {
                "warehouse_id": "YOUR_WAREHOUSE_ID",
                "query": {
                    "query_id": "YOUR_QUERY_ID"  # Ou usar "query" com SQL direto
                }
            },
            "timeout_seconds": 1800,
            "max_retries": 2,
            "min_retry_interval_millis": 300000
        }
    ],
    "schedule": {
        "quartz_cron_expression": "0 0 6 * * ?",
        "timezone_id": "America/Sao_Paulo"
    },
    "email_notifications": {
        "on_failure": ["team@company.com"]
    }
}

response = requests.post(
    f"{databricks_host}/api/2.1/jobs/create",
    headers={"Authorization": f"Bearer {databricks_token}"},
    json=job_config
)

print(f"Job created: {response.json()}")
```

### Opção C: Via Databricks CLI

```bash
# Instalar CLI
pip install databricks-cli

# Configurar
databricks configure --token

# Criar job
databricks jobs create --json-file job_config.json
```

---

## Monitoramento e Troubleshooting

### Verificar Execução do Job

```sql
-- Ver última execução
SELECT
  'crm_metrics_daily' as tabela,
  MAX(data_referencia) as ultima_atualizacao,
  COUNT(*) as total_registros
FROM hs_franquia.gold_connect_bot.crm_metrics_daily
GROUP BY tabela

UNION ALL

SELECT
  'crm_action_priorities_daily' as tabela,
  MAX(data_referencia) as ultima_atualizacao,
  COUNT(*) as total_registros
FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily
GROUP BY tabela

UNION ALL

SELECT
  'crm_actions_open_snapshot' as tabela,
  MAX(data_snapshot) as ultima_atualizacao,
  COUNT(*) as total_registros
FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot
GROUP BY tabela;
```

### Alertas Recomendados

1. **Job falhou**: E-mail imediato
2. **Job rodou > 15 minutos**: Investigar performance
3. **Tabela sem atualização há > 2 dias**: Alerta crítico

### Troubleshooting Comum

#### Problema 1: Job falha com timeout
**Solução**: Aumentar timeout ou otimizar queries

```sql
-- Verificar volume de dados processados
SELECT
  DATE(VERIFICATION_DATE) as data,
  COUNT(*) as total_verificacoes
FROM hs_franquia.gold_connect_bot.vw_crm_verification
WHERE VERIFICATION_DATE >= DATE_SUB(CURRENT_DATE(), 7)
GROUP BY DATE(VERIFICATION_DATE)
ORDER BY data DESC;
```

#### Problema 2: Dados desatualizados
**Solução**: Executar refresh manual

```sql
-- Executar manualmente o script:
-- 04_refresh_daily_materialized_tables.sql
```

#### Problema 3: Storage crescendo muito
**Solução**: Ajustar período de retenção

```sql
-- Limpar dados > 30 dias (ao invés de 90)
DELETE FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily
WHERE data_referencia < DATE_SUB(CURRENT_DATE(), 30);

DELETE FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot
WHERE data_snapshot < DATE_SUB(CURRENT_DATE(), 30);

VACUUM hs_franquia.gold_connect_bot.crm_action_priorities_daily RETAIN 0 HOURS;
VACUUM hs_franquia.gold_connect_bot.crm_actions_open_snapshot RETAIN 0 HOURS;
```

---

## Custos Estimados

### Cenário Atual (Sem Materialized Tables)
- **Queries por dia**: 10.000+ (1000 usuários × 10 refreshes)
- **Custo por query**: ~$0.01
- **Custo mensal**: ~$3.000

### Cenário Novo (Com Materialized Tables)
- **Job diário**: 10 min × 30 dias = $50/mês
- **Storage**: ~200 MB/mês = $5/mês
- **Cache misses**: 500 queries/dia = $150/mês
- **TOTAL**: ~$200/mês
- **ECONOMIA**: **93% (~$2.800/mês)**

### Breakdown de Custos por Tabela

| Tabela | Tamanho Mensal | Custo Storage | Custo Compute (Job) | Total |
|--------|---------------|---------------|---------------------|-------|
| crm_metrics_daily | ~30 MB | $1 | $15 | $16 |
| crm_action_priorities_daily | ~5 MB | $0.50 | $10 | $10.50 |
| crm_actions_open_snapshot | ~100 MB | $3 | $25 | $28 |
| **TOTAL** | **~135 MB** | **$4.50** | **$50** | **$54.50** |

*Obs: Valores estimados baseados em pricing médio do Databricks*

---

## Validação Final

Após configurar tudo, validar:

### Checklist de Validação

- [ ] 3 tabelas criadas no catálogo `hs_franquia.gold_connect_bot`
- [ ] Tabelas populadas com dados iniciais
- [ ] Particionamento funcionando corretamente
- [ ] Databricks Job configurado e agendado
- [ ] Primeira execução manual bem-sucedida
- [ ] Alertas de e-mail configurados
- [ ] Queries do backend atualizadas (próximo passo)
- [ ] Cache implementado no backend (próximo passo)

### Query de Validação Completa

```sql
-- Executar e verificar se todos os valores são recentes
SELECT
  'Métricas' as tipo,
  COUNT(*) as registros,
  MAX(data_referencia) as ultima_data,
  DATEDIFF(day, MAX(data_referencia), CURRENT_DATE()) as dias_atraso
FROM hs_franquia.gold_connect_bot.crm_metrics_daily

UNION ALL

SELECT
  'Prioridades' as tipo,
  COUNT(*) as registros,
  MAX(data_referencia) as ultima_data,
  DATEDIFF(day, MAX(data_referencia), CURRENT_DATE()) as dias_atraso
FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily

UNION ALL

SELECT
  'Ações' as tipo,
  COUNT(*) as registros,
  MAX(data_snapshot) as ultima_data,
  DATEDIFF(day, MAX(data_snapshot), CURRENT_DATE()) as dias_atraso
FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot;

-- Resultado esperado: dias_atraso = 0 ou 1 (dependendo do horário)
```

---

## Próximos Passos

Após configurar as materialized tables:

1. ✅ **Implementar cache no backend** ([Fase 2](../../docs/CACHE_IMPLEMENTATION.md))
2. ✅ **Atualizar queries do backend** ([Fase 3](../../docs/BACKEND_QUERIES_UPDATE.md))
3. ✅ **Testes de carga e validação** ([Fase 4](../../docs/TESTING.md))

---

## Suporte

Para dúvidas ou problemas:
1. Verificar logs do Databricks Job
2. Executar queries de troubleshooting acima
3. Contatar time de data engineering

---

**Última atualização**: 2025-12-20
**Versão**: 1.0
