-- =====================================================================
-- Script: Criação da Tabela Materializada de Métricas Diárias
-- Tabela: hs_franquia.gold_connect_bot.crm_metrics_daily
-- Descrição: Agregações diárias de verificações, controles e perguntas
-- Atualização: Diária (via Databricks Job)
-- =====================================================================

-- Drop table if exists (apenas para recriar estrutura)
DROP TABLE IF EXISTS hs_franquia.gold_connect_bot.crm_metrics_daily;

-- Create materialized table
CREATE TABLE hs_franquia.gold_connect_bot.crm_metrics_daily (
  data_referencia DATE COMMENT 'Data da verificação',
  organizacao STRING COMMENT 'Unidade organizacional (uo_level_03)',
  localizacao STRING COMMENT 'Localização (TEXT_PT)',
  tipo_verificacao STRING COMMENT 'Tipo de verificação',

  total_verificacoes BIGINT COMMENT 'Total de verificações',
  verificacoes_nao_conformes BIGINT COMMENT 'Verificações não conformes',

  total_controles BIGINT COMMENT 'Total de controles críticos únicos',
  controles_nao_conformes BIGINT COMMENT 'Controles não conformes',

  total_perguntas BIGINT COMMENT 'Total de perguntas (exclui ND=1)',
  perguntas_nao_conformes BIGINT COMMENT 'Perguntas não conformes'
)
USING DELTA
PARTITIONED BY (data_referencia)
COMMENT 'Métricas agregadas diárias do CRM - Verificações, Controles e Perguntas'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);

-- Insert initial data (usar YES/NOT/ND corretos)
INSERT INTO hs_franquia.gold_connect_bot.crm_metrics_daily
SELECT
  DATE(v.VERIFICATION_DATE) as data_referencia,
  org.uo_level_03 as organizacao,
  loc.TEXT_PT as localizacao,
  v.TYPE as tipo_verificacao,

  -- Verificações (USA NOT=1 ao invés de campo legado)
  COUNT(DISTINCT v.ID) as total_verificacoes,
  COUNT(DISTINCT CASE WHEN q.NOT = 1 THEN v.ID END) as verificacoes_nao_conformes,

  -- Controles Críticos (USA CRITICAL_CONTROL, exclui ND=1)
  COUNT(DISTINCT CASE WHEN COALESCE(q.ND, 0) != 1 THEN q.CRITICAL_CONTROL END) as total_controles,
  COUNT(DISTINCT CASE WHEN q.NOT = 1 THEN q.CRITICAL_CONTROL END) as controles_nao_conformes,

  -- Perguntas (exclui ND=1)
  COUNT(CASE WHEN COALESCE(q.ND, 0) != 1 THEN 1 END) as total_perguntas,
  SUM(CASE WHEN q.NOT = 1 THEN 1 ELSE 0 END) as perguntas_nao_conformes

FROM hs_franquia.gold_connect_bot.vw_crm_verification v
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_verification_question q
  ON v.ID = q.VERIFICATION_ID
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_location loc
  ON v.SITE_ID = loc.ID_SITE
LEFT JOIN hs_franquia.gold_connect_bot.vw_general_de_para_hier_org_unit org
  ON v.ID_UO = org.id_uo

WHERE v.VERIFICATION_DATE >= DATE_SUB(CURRENT_DATE(), 365)  -- Último ano

GROUP BY
  DATE(v.VERIFICATION_DATE),
  org.uo_level_03,
  loc.TEXT_PT,
  v.TYPE;

-- Optimize table
OPTIMIZE hs_franquia.gold_connect_bot.crm_metrics_daily;

-- Collect statistics
ANALYZE TABLE hs_franquia.gold_connect_bot.crm_metrics_daily COMPUTE STATISTICS FOR ALL COLUMNS;

-- Show sample data
SELECT
  data_referencia,
  organizacao,
  localizacao,
  tipo_verificacao,
  total_verificacoes,
  verificacoes_nao_conformes,
  total_controles,
  controles_nao_conformes,
  total_perguntas,
  perguntas_nao_conformes
FROM hs_franquia.gold_connect_bot.crm_metrics_daily
ORDER BY data_referencia DESC
LIMIT 10;
