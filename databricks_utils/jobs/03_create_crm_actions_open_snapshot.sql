-- =====================================================================
-- Script: Criação da Tabela Materializada de Ações Abertas (Snapshot)
-- Tabela: hs_franquia.gold_connect_bot.crm_actions_open_snapshot
-- Descrição: Snapshot diário de todas as ações abertas com detalhes
-- Atualização: Diária (via Databricks Job)
-- =====================================================================

-- Drop table if exists (apenas para recriar estrutura)
DROP TABLE IF EXISTS hs_franquia.gold_connect_bot.crm_actions_open_snapshot;

-- Create materialized table
CREATE TABLE hs_franquia.gold_connect_bot.crm_actions_open_snapshot (
  data_snapshot DATE COMMENT 'Data do snapshot',
  id_acao STRING COMMENT 'ID da ação',
  id_verificacao STRING COMMENT 'ID da verificação que originou a ação',
  responsavel STRING COMMENT 'Nome completo do responsável',
  data_vencimento_acao DATE COMMENT 'Data de vencimento da ação',
  status_acao STRING COMMENT 'Atrasado ou Em Andamento',
  tipo STRING COMMENT 'Tipo da ação',
  organizacao STRING COMMENT 'Unidade organizacional (uo_level_03)',
  localizacao STRING COMMENT 'Localização (TEXT_PT)',
  tipo_verificacao STRING COMMENT 'Tipo de verificação'
)
USING DELTA
PARTITIONED BY (data_snapshot)
COMMENT 'Snapshot diário de ações abertas com detalhes completos'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);

-- Insert initial data
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

WHERE a.COMPLETED_DATE IS NULL;  -- Apenas ações abertas

-- Optimize table
OPTIMIZE hs_franquia.gold_connect_bot.crm_actions_open_snapshot;

-- Collect statistics
ANALYZE TABLE hs_franquia.gold_connect_bot.crm_actions_open_snapshot COMPUTE STATISTICS FOR ALL COLUMNS;

-- Show sample data (ações mais atrasadas)
SELECT
  data_snapshot,
  id_acao,
  id_verificacao,
  responsavel,
  data_vencimento_acao,
  status_acao,
  tipo,
  organizacao,
  localizacao
FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot
WHERE data_snapshot = CURRENT_DATE()
ORDER BY
  CASE WHEN status_acao = 'Atrasado' THEN 0 ELSE 1 END,
  data_vencimento_acao ASC
LIMIT 20;

-- Show statistics
SELECT
  data_snapshot,
  status_acao,
  COUNT(*) as total_acoes
FROM hs_franquia.gold_connect_bot.crm_actions_open_snapshot
WHERE data_snapshot = CURRENT_DATE()
GROUP BY data_snapshot, status_acao
ORDER BY status_acao;
