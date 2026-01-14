-- =====================================================================
-- Script: Criação da Tabela Materializada de Prioridades de Ações
-- Tabela: hs_franquia.gold_connect_bot.crm_action_priorities_daily
-- Descrição: Distribuição de ações abertas por categoria de prioridade
-- Atualização: Diária (via Databricks Job)
-- =====================================================================

-- Drop table if exists (apenas para recriar estrutura)
DROP TABLE IF EXISTS hs_franquia.gold_connect_bot.crm_action_priorities_daily;

-- Create materialized table
CREATE TABLE hs_franquia.gold_connect_bot.crm_action_priorities_daily (
  data_referencia DATE COMMENT 'Data de referência do snapshot',
  organizacao STRING COMMENT 'Unidade organizacional (uo_level_03)',
  localizacao STRING COMMENT 'Localização (TEXT_PT)',
  tipo_verificacao STRING COMMENT 'Tipo de verificação',
  categoria_prioridade STRING COMMENT 'Categoria: Vencidas, S=0 a S=4, Posterior a S=4',
  total_acoes BIGINT COMMENT 'Total de ações na categoria'
)
USING DELTA
PARTITIONED BY (data_referencia)
COMMENT 'Distribuição de ações abertas por prioridade'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);

-- Insert initial data
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

WHERE a.COMPLETED_DATE IS NULL  -- Apenas ações abertas

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

-- Optimize table
OPTIMIZE hs_franquia.gold_connect_bot.crm_action_priorities_daily;

-- Collect statistics
ANALYZE TABLE hs_franquia.gold_connect_bot.crm_action_priorities_daily COMPUTE STATISTICS FOR ALL COLUMNS;

-- Show sample data (agrupado por categoria)
SELECT
  data_referencia,
  categoria_prioridade,
  SUM(total_acoes) as total_geral
FROM hs_franquia.gold_connect_bot.crm_action_priorities_daily
GROUP BY data_referencia, categoria_prioridade
ORDER BY
  CASE categoria_prioridade
    WHEN 'Vencidas' THEN 0
    WHEN 'S=0' THEN 1
    WHEN 'S=1' THEN 2
    WHEN 'S=2' THEN 3
    WHEN 'S=3' THEN 4
    WHEN 'S=4' THEN 5
    WHEN 'Posterior a S=4' THEN 6
    ELSE 7
  END;
