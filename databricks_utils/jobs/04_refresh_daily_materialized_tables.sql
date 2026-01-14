-- =====================================================================
-- Script: Refresh Diário das Tabelas Materializadas do CRM
-- Execução: Databricks Job Scheduled (diário às 6h da manhã)
-- Descrição: Atualiza as 3 tabelas materializadas com dados do dia anterior
-- =====================================================================

-- =====================================================================
-- 1. REFRESH: crm_metrics_daily
-- Estratégia: DELETE + INSERT incremental (últimos 7 dias para correções)
-- =====================================================================

-- Delete dados dos últimos 7 dias (para recálculo)
DELETE FROM hs_franquia.gold_connect_bot.crm_metrics_daily
WHERE data_referencia >= DATE_SUB(CURRENT_DATE(), 7);

-- Insert dados atualizados dos últimos 7 dias
INSERT INTO hs_franquia.gold_connect_bot.crm_metrics_daily
SELECT
  DATE(v.VERIFICATION_DATE) as data_referencia,
  org.uo_level_03 as organizacao,
  loc.H_01 as localizacao,
  v.TYPE as tipo_verificacao,

  -- Verificações
  COUNT(DISTINCT v.ID) as total_verificacoes,
  COUNT(DISTINCT CASE WHEN q.NOT = 1 THEN v.ID END) as verificacoes_nao_conformes,

  -- Controles Críticos
  COUNT(DISTINCT CASE WHEN COALESCE(q.ND, 0) != 1 THEN q.CRITICAL_CONTROL END) as total_controles,
  COUNT(DISTINCT CASE WHEN q.NOT = 1 THEN q.CRITICAL_CONTROL END) as controles_nao_conformes,

  -- Perguntas
  COUNT(CASE WHEN COALESCE(q.ND, 0) != 1 THEN 1 END) as total_perguntas,
  SUM(CASE WHEN q.NOT = 1 THEN 1 ELSE 0 END) as perguntas_nao_conformes

FROM hs_franquia.gold_connect_bot.vw_crm_verification v
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_verification_question q
  ON v.ID = q.VERIFICATION_ID
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_location loc
  ON v.SITE_ID = loc.ID_SITE
LEFT JOIN hs_franquia.gold_connect_bot.vw_general_de_para_hier_org_unit org
  ON v.ID_UO = org.id_uo

WHERE v.VERIFICATION_DATE >= DATE_SUB(CURRENT_DATE(), 7)

GROUP BY
  DATE(v.VERIFICATION_DATE),
  org.uo_level_03,
  loc.H_01,
  v.TYPE;

-- Optimize
OPTIMIZE hs_franquia.gold_connect_bot.crm_metrics_daily;

SELECT 'crm_metrics_daily atualizada com sucesso' as status;

-- =====================================================================
-- 2. REFRESH: crm_action_priorities_daily
-- Estratégia: DELETE + INSERT completo (snapshot diário)
-- =====================================================================

-- Delete snapshot do dia atual (se existir)
DELETE FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily
WHERE data_referencia = CURRENT_DATE();

-- Insert novo snapshot
INSERT INTO hs_franquia.gold_connect_bot.crm_action_priorities_daily
SELECT
  CURRENT_DATE() as data_referencia,
  org.uo_level_03 as organizacao,
  loc.H_01 as localizacao,
  v.TYPE as tipo_verificacao,

  CASE
    WHEN a.END_DATE < CURRENT_DATE() AND a.COMPLETED_DATE IS NULL THEN 'Vencidas'
    WHEN a.PRIORITY = 0 THEN 'S=0'
    WHEN a.PRIORITY = 1 THEN 'S=1'
    WHEN a.PRIORITY = 2 THEN 'S=2'
    WHEN a.PRIORITY = 3 THEN 'S=3'
    WHEN a.PRIORITY = 4 THEN 'S=4'
    WHEN a.PRIORITY > 4 THEN 'Posterior a S=4'
    ELSE 'Outros'
  END as categoria_prioridade,

  COUNT(*) as total_acoes

FROM hs_franquia.gold_connect_bot.vw_crm_action a
JOIN hs_franquia.gold_connect_bot.vw_crm_verification v
  ON a.VERIFICATION_ID = v.ID
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_location loc
  ON v.SITE_ID = loc.ID_SITE
LEFT JOIN hs_franquia.gold_connect_bot.vw_general_de_para_hier_org_unit org
  ON v.ID_UO = org.id_uo

WHERE a.COMPLETED_DATE IS NULL

GROUP BY
  org.uo_level_03,
  loc.H_01,
  v.TYPE,
  CASE
    WHEN a.END_DATE < CURRENT_DATE() AND a.COMPLETED_DATE IS NULL THEN 'Vencidas'
    WHEN a.PRIORITY = 0 THEN 'S=0'
    WHEN a.PRIORITY = 1 THEN 'S=1'
    WHEN a.PRIORITY = 2 THEN 'S=2'
    WHEN a.PRIORITY = 3 THEN 'S=3'
    WHEN a.PRIORITY = 4 THEN 'S=4'
    WHEN a.PRIORITY > 4 THEN 'Posterior a S=4'
    ELSE 'Outros'
  END;

-- Optimize
OPTIMIZE hs_franquia.gold_connect_bot.crm_action_priorities_daily;

SELECT 'crm_action_priorities_daily atualizada com sucesso' as status;

-- =====================================================================
-- 3. REFRESH: crm_actions_open_snapshot
-- Estratégia: DELETE + INSERT completo (snapshot diário)
-- =====================================================================

-- Delete snapshot do dia atual (se existir)
DELETE FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot
WHERE data_snapshot = CURRENT_DATE();

-- Insert novo snapshot
INSERT INTO hs_franquia.gold_connect_bot.crm_actions_open_snapshot
SELECT
  CURRENT_DATE() as data_snapshot,
  a.ID as id_acao,
  a.VERIFICATION_ID as id_verificacao,
  u.FULL_NAME as responsavel,
  a.END_DATE as data_vencimento_acao,
  CASE
    WHEN a.END_DATE < CURRENT_DATE() THEN 'Atrasado'
    ELSE 'Em Andamento'
  END as status_acao,
  COALESCE(a.TYPE, 'N/A') as tipo,
  org.uo_level_03 as organizacao,
  loc.H_01 as localizacao,
  v.TYPE as tipo_verificacao

FROM hs_franquia.gold_connect_bot.vw_crm_action a
JOIN hs_franquia.gold_connect_bot.vw_crm_verification v
  ON a.VERIFICATION_ID = v.ID
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_user u
  ON a.RESPONSIBLE_PERSON_ID = u.USER_ID
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_location loc
  ON v.SITE_ID = loc.ID_SITE
LEFT JOIN hs_franquia.gold_connect_bot.vw_general_de_para_hier_org_unit org
  ON v.ID_UO = org.id_uo

WHERE a.COMPLETED_DATE IS NULL;

-- Optimize
OPTIMIZE hs_franquia.gold_connect_bot.crm_actions_open_snapshot;

SELECT 'crm_actions_open_snapshot atualizada com sucesso' as status;

-- =====================================================================
-- 4. LIMPEZA: Remover dados antigos (> 90 dias) para economizar storage
-- =====================================================================

-- Limpar snapshots antigos de action_priorities
DELETE FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily
WHERE data_referencia < DATE_SUB(CURRENT_DATE(), 90);

-- Limpar snapshots antigos de actions
DELETE FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot
WHERE data_snapshot < DATE_SUB(CURRENT_DATE(), 90);

SELECT 'Limpeza de dados antigos concluída' as status;

-- =====================================================================
-- 5. ANÁLISE E ESTATÍSTICAS FINAIS
-- =====================================================================

ANALYZE TABLE hs_franquia.gold_connect_bot.crm_metrics_daily COMPUTE STATISTICS FOR ALL COLUMNS;
ANALYZE TABLE hs_franquia.gold_connect_bot.crm_action_priorities_daily COMPUTE STATISTICS FOR ALL COLUMNS;
ANALYZE TABLE hs_franquia.gold_connect_bot.crm_actions_open_snapshot COMPUTE STATISTICS FOR ALL COLUMNS;

SELECT 'Refresh completo concluído com sucesso!' as status;

-- =====================================================================
-- 6. RESUMO DO REFRESH (para logs)
-- =====================================================================

SELECT
  'crm_metrics_daily' as tabela,
  COUNT(*) as total_registros,
  MIN(data_referencia) as data_inicio,
  MAX(data_referencia) as data_fim
FROM hs_franquia.gold_connect_bot.crm_metrics_daily

UNION ALL

SELECT
  'crm_action_priorities_daily' as tabela,
  COUNT(*) as total_registros,
  MIN(data_referencia) as data_inicio,
  MAX(data_referencia) as data_fim
FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily

UNION ALL

SELECT
  'crm_actions_open_snapshot' as tabela,
  COUNT(*) as total_registros,
  MIN(data_snapshot) as data_inicio,
  MAX(data_snapshot) as data_fim
FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot

ORDER BY tabela;
