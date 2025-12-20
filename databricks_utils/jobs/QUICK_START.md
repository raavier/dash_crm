# Quick Start - Materialized Tables Setup

Guia rápido para configurar as tabelas materializadas em **15 minutos**.

## 🚀 Passos Rápidos

### 1. Criar as Tabelas (5 min)

Acesse **Databricks SQL Editor** e execute na ordem:

```bash
# Executar cada arquivo:
01_create_crm_metrics_daily.sql          # ~2 min
02_create_crm_action_priorities_daily.sql # ~1 min
03_create_crm_actions_open_snapshot.sql   # ~2 min
```

**Validar:**
```sql
SHOW TABLES IN hs_franquia.gold_connect_bot LIKE 'crm_*';
-- Deve retornar 3 tabelas
```

---

### 2. Configurar o Job Diário (5 min)

**Databricks Workflows → Jobs → Create Job**

| Campo | Valor |
|-------|-------|
| **Nome** | `CRM Dashboard - Daily Refresh` |
| **Type** | SQL |
| **SQL file** | Colar conteúdo de `04_refresh_daily_materialized_tables.sql` |
| **Warehouse** | Selecionar warehouse de produção |
| **Schedule** | `0 6 * * *` (6h AM diário) |
| **Timezone** | `America/Sao_Paulo` |
| **Email on failure** | Seu e-mail |
| **Max retries** | 2 |

**Testar:** Clicar em "Run now" e aguardar ~5-10 min

---

### 3. Validar Tudo Funcionou (5 min)

```sql
-- Query de validação completa
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
```

**Resultado esperado:**
- `dias_atraso` = 0 ou 1 (dependendo do horário)
- Todos com `registros` > 0

---

## ✅ Checklist

- [ ] 3 tabelas criadas
- [ ] Tabelas com dados
- [ ] Job configurado
- [ ] Job executado 1x com sucesso
- [ ] Validação passou

---

## 🆘 Troubleshooting Rápido

**Problema**: Job falhou
**Solução**: Ver logs do job e verificar permissões nas views originais

**Problema**: Tabelas vazias
**Solução**: Verificar se as views originais existem:
```sql
SHOW TABLES IN hs_franquia.gold_connect_bot LIKE 'vw_crm_%';
```

**Problema**: Query lenta
**Solução**: Adicionar mais DBUs ao warehouse ou executar fora de horário de pico

---

## 📊 Resultado Esperado

Após setup completo:
- **Custo**: Redução de ~$3.000 → ~$200/mês (93% economia)
- **Performance**: Queries 20-50x mais rápidas
- **Manutenção**: Job roda automaticamente 1x/dia

---

## 🔜 Próximos Passos

1. Implementar cache no backend (Fase 2)
2. Atualizar queries do backend para usar as tabelas materializadas (Fase 3)
3. Testes e deploy (Fase 4)

Ver [README.md](README.md) para detalhes completos.
