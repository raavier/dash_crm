# Estrutura do Banco de Dados CRM

Documentação completa das tabelas do sistema de Gerenciamento de Riscos Críticos (Control Risk Management).

**Catálogo**: `hs_franquia`
**Schema Gold (Views)**: `gold_connect_bot`
**Schema Silver (Base)**: `silver_crm`, `silver_general`

---

## 📋 Índice

1. [Tabelas Principais](#tabelas-principais)
2. [Relacionamentos](#relacionamentos-entre-tabelas)
3. [Queries para Dashboard](#queries-para-o-dashboard)
4. [Notas Importantes](#notas-importantes)

---

## Tabelas Principais

### 1. vw_crm_action - Ações Corretivas e Preventivas

**Nome Completo**: `hs_franquia.gold_connect_bot.vw_crm_action`

#### Descrição
Registro de planos de ação corretivos e preventivos derivados de verificações de segurança, inspeções e auditorias.

#### Contexto de Negócio
Gestão do ciclo de vida de ações de segurança e manutenção, desde identificação até fechamento. Permite rastreamento de conformidade, priorização por criticidade e acompanhamento de responsabilidades.

#### Colunas

| Coluna | Tipo | Descrição | PK | FK | Relacionamento |
|--------|------|-----------|----|----|----------------|
| ID | string | Identificador único da ação | ✓ | | |
| VERIFICATION_ID | string | ID da verificação que originou a ação | | ✓ | verification.ID |
| ID_UO | int | Identificador da unidade organizacional | | ✓ | vw_general_de_para_hier_org_unit.id_uo |
| TEXT | string | Descrição detalhada da ação | | | |
| QUESTION_ID | string | ID da pergunta do checklist relacionada | | | |
| CONTROL_ID | int | ID do controle crítico associado | | | |
| COMMENTS | string | Comentários adicionais | | | |
| TYPE | string | Tipo: System or Process / Plant or Equipment / Behavioural | | | |
| FIXED_IN_FIELD | int | Corrigido em campo (0=não, 1=sim) | | | |
| DATE_RAISED | date | Data em que a ação foi registrada | | | |
| PRIORITY | int | Prioridade (1=crítico, 4=baixo) | | | |
| END_DATE | date | Data limite/prazo | | | |
| RESPONSIBLE_PERSON_ID | int | ID do usuário responsável | | ✓ | vw_crm_user.USER_ID |
| COMPLETED_DATE | date | Data de conclusão (NULL = em aberto) | | | |
| CHANGED | timestamp | Última modificação | | | |

**Valores de Exemplo**:
- **PRIORITY**: 1 (crítico) → 4 (baixo)
- **TYPE**: "System or Process", "Plant or Equipment", "Behavioural"
- **FIXED_IN_FIELD**: 0 (não), 1 (sim - "Ver e Agir")

---

### 2. vw_crm_verification - Verificações de Segurança

**Nome Completo**: `hs_franquia.gold_connect_bot.vw_crm_verification`

#### Descrição
Registro de verificações de segurança realizadas em campo. Captura informações sobre localização, verificador, riscos críticos identificados e contexto do trabalho.

#### Contexto de Negócio
Auditoria e inspeções de segurança. Suporta verificações via mobile (tablet/smartphone) e desktop.

#### Colunas

| Coluna | Tipo | Descrição | PK | FK |
|--------|------|-----------|----|----|
| ID | string | Identificador único | ✓ | |
| SITE_ID | int | ID do site | | ✓ |
| WORK_AREA | string | Área de trabalho específica | | |
| EQUIPMENT_NUMBER_AREA | string | Número/código do equipamento (4mil+ items) | | |
| CRITICAL_RISK | string | Categoria de risco crítico (ver lista abaixo) | | |
| VERIFICATION_DATE | timestamp | Data/hora da verificação | | |
| VERIFIER_ID | int | ID do verificador | | ✓ |
| ID_UO | int | ID da unidade organizacional | | ✓ |
| TYPE | string | Manager/Operator/Supervisor Verification | | |
| SCHEDULED | int | Agendada (0=não, 1=sim) | | |
| MOBILE_SUBMISSION | int | Via mobile (0=não, 1=sim) | | |
| LANGUAGE | string | Portuguese (Brazil) / English | | |
| UNPLANNED_WORK | int | Trabalho não planejado (0=não, 1=sim) | | |
| WORKER_TYPE | string | Other/Shutdown/Construction/Development/etc. | | |
| TASK_TEXT | string | Descrição da tarefa | | |

#### Categorias de Riscos Críticos Disponíveis

<details>
<summary>Clique para expandir lista completa (40+ categorias)</summary>

- Impacto ferroviário em pessoa
- Atropelamento (RAC 03)
- Afogamento
- Falha de talude (RAC 08)
- Operações de perfuração de superfície
- Operações de içamento (RAC 05)
- Liberação de energia não controlada (RAC 04)
- Liberação de energia não controlada (outras)
- Colisão ferroviária
- Trabalho de escavação (RAC 08)
- Proximidade de correntes elétricas energizadas (RAC 10)
- Incidente de trânsito na área de construção civil (RAC 02/03)
- Atropelamento por veículo (RAC 02/03)
- Abertura de vala (RAC 08)
- Ignição não planejada de explosivos (RAC 09)
- Queda de materiais (RAC 01/05)
- Queda de materiais (outros) (RAC 05)
- Queda de materiais em armazéns
- Manutenção de Pneu (RAC 03)
- Capotamento e colisão de veículo (RAC 02/03)
- Carga e descarga de materiais (RAC 05)
- Queda de altura (RAC 01)
- Contato com eletricidade (RAC 10)
- Relâmpago
- Operações de Elevação de Helicópteros
- Espaço confinado (RAC 06)
- Colapso de estrutura (GPS)
- Incêndio por Trabalho a Quente (RAC 12)
- Aprisionamento e esmagamento (RAC 07)
- Falha na parede da barragem

</details>

---

### 3. vw_crm_verification_question - Respostas do Checklist

**Nome Completo**: `hs_franquia.gold_connect_bot.vw_crm_verification_question`

#### Descrição
Respostas detalhadas de cada pergunta do checklist aplicado durante uma verificação. Base para geração automática de ações corretivas.

#### Colunas Principais

| Coluna | Tipo | Descrição | PK |
|--------|------|-----------|----|
| DB_KEY | string | Chave única (VERIFICATION_ID + QUESTION_ID + seq) | ✓ |
| VERIFICATION_ID | string | ID da verificação pai | |
| CRITICAL_CONTROL | string | Nome do controle crítico | |
| QUESTION_ID | string | ID único da pergunta | |
| TEXT | string | Texto completo da pergunta | |
| COMMENT | string | Comentários do verificador | |
| EVIDENCE | int | Evidência coletada (0=não, 1=sim) | |
| **CRITICAL_CONTROL_NON_COMPLIANCE** | int | **Não conforme (0=OK, 1=NOK)** | |
| CRITICAL_CONTROL_COMPLIANCE | int | Conforme (0=NOK, 1=OK) | |
| CHECKLIST_ID | int | ID do checklist | |
| QUESTION_IDP | string | ID alternativo (pode incluir seção) | |

**Importante**: `CRITICAL_CONTROL_NON_COMPLIANCE = 1` indica não conformidade (NOK).

---

### 4. vw_crm_user - Usuários do Sistema

**Nome Completo**: `hs_franquia.gold_connect_bot.vw_crm_user`

#### ⚠️ ATENÇÃO - IDs de Usuário

Esta tabela possui DOIS identificadores diferentes:

| Coluna | Tipo | Uso | Para JOINs? |
|--------|------|-----|-------------|
| **ID** | string (UUID) | Identificador interno UUID | ❌ **NÃO USAR** |
| **USER_ID** | int | Identificador numérico | ✅ **SEMPRE USAR** |

**Regra**: Sempre use `USER_ID` (int) para relacionamentos com outras tabelas!

#### Colunas Principais

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| USER_ID | int | **ID para JOINs** |
| ID | string | UUID interno (não usar) |
| FULL_NAME | string | Nome completo |
| EMAIL | string | E-mail corporativo |
| USER_NAME | string | Nome de usuário |
| ROLE_CATEGORY | string | Operator/Supervisor/Manager |
| CRM_LEADERSHIP_ROLE | boolean | Papel de liderança |
| CORPORATE_GROUP | string | Grupo corporativo (Vale) |
| PRODUCT_GROUP_CRM | string | Grupo de produto |
| BUSINESS_UNIT_CRM | string | Unidade de negócio |
| CREATED_DATE | timestamp | Data de criação |
| LAST_LOGIN_DATE | timestamp | Último login |

---

### 5. vw_crm_location - Localizações

**Nome Completo**: `hs_franquia.gold_connect_bot.vw_crm_location`

#### Descrição
Cadastro hierárquico de localizações geográficas. Estrutura em árvore de até 7 níveis: país → região → complexo → site → área → subárea.

#### Colunas Principais

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| ID | string (UUID) | Identificador único |
| ID_SAP | int | Código SAP |
| ID_SITE | int | Identificador do site |
| TEXT_PT | string | Nome em português |
| TEXT_EN | string | Nome em inglês |
| LATITUDE | float | Coordenada geográfica |
| LONGITUDE | float | Coordenada geográfica |
| HIER_01 | string | Nível 1 - País |
| HIER_02 | string | Nível 2 - Região |
| HIER_03 | string | Nível 3 - Complexo |
| HIER_04 | string | Nível 4 - Site |
| HIER_05 | string | Nível 5 - Área |
| HIER_06 | string | Nível 6 - Subárea |
| HIER_07 | string | Nível 7 (folha) |

**Hierarquia**:
```
País (HIER_01)
 └─ Região (HIER_02)
     └─ Complexo (HIER_03)
         └─ Site (HIER_04)
             └─ Área (HIER_05)
                 └─ Subárea (HIER_06)
                     └─ Nível 7 (HIER_07)
```

---

### 6. vw_crm_verification_involved - Participantes

**Nome Completo**: `hs_franquia.gold_connect_bot.vw_crm_verification_involved`

#### Descrição
Registro de pessoas envolvidas em verificações (além do verificador principal).

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| VERIFICATION_ID | string | ID da verificação |
| USER_ID | int | ID do usuário |
| FUNCAO | string | COACH / ASSISTENTE / VERIFICADOR |

---

### 7. vw_general_de_para_hier_org_unit - Hierarquia Organizacional

**Nome Completo**: `hs_franquia.gold_connect_bot.vw_general_de_para_hier_org_unit`

#### Descrição
Informações de Unidade Organizacional da empresa. Estrutura hierárquica com 10 níveis.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_uo | int | ID único da UO (PK) |
| uo_level_01 | string | Nível 1 - "GRUPO VALE S/A" |
| uo_level_02 | string | Nível 2 - Presidência |
| uo_level_03 | string | Nível 3 - VPs e CEOs |
| uo_level_04 a 10 | string | Níveis hierárquicos subsequentes |

---

## Relacionamentos Entre Tabelas

### Diagrama de Relacionamentos

```
vw_crm_verification
    │
    ├──► vw_crm_location (SITE_ID)
    ├──► vw_crm_user (VERIFIER_ID → USER_ID)
    ├──► vw_general_de_para_hier_org_unit (ID_UO)
    │
    └──► vw_crm_verification_question (1:N)
         │
         └──► vw_crm_action (VERIFICATION_ID)
              │
              ├──► vw_crm_user (RESPONSIBLE_PERSON_ID → USER_ID)
              └──► vw_general_de_para_hier_org_unit (ID_UO)

vw_crm_verification_involved
    ├──► vw_crm_verification (VERIFICATION_ID)
    └──► vw_crm_user (USER_ID)
```

### Exemplos de JOINs

**Verificação com Verificador**:
```sql
SELECT v.*, u.FULL_NAME as verificador
FROM hs_franquia.gold_connect_bot.vw_crm_verification v
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_user u
  ON v.VERIFIER_ID = u.USER_ID
```

**Ações com Responsável**:
```sql
SELECT a.*, u.FULL_NAME as responsavel
FROM hs_franquia.gold_connect_bot.vw_crm_action a
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_user u
  ON a.RESPONSIBLE_PERSON_ID = u.USER_ID
```

---

## Queries para o Dashboard

### 1. Total de Verificações e % Não Conformes

```sql
SELECT
  COUNT(DISTINCT v.ID) as total_verificacoes,
  COUNT(DISTINCT CASE
    WHEN q.CRITICAL_CONTROL_NON_COMPLIANCE = 1
    THEN v.ID
  END) as verificacoes_nao_conformes,
  ROUND(
    COUNT(DISTINCT CASE WHEN q.CRITICAL_CONTROL_NON_COMPLIANCE = 1 THEN v.ID END) * 100.0 /
    NULLIF(COUNT(DISTINCT v.ID), 0),
    2
  ) as percentual_nao_conforme
FROM hs_franquia.gold_connect_bot.vw_crm_verification v
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_verification_question q
  ON v.ID = q.VERIFICATION_ID
WHERE v.VERIFICATION_DATE BETWEEN '2025-01-01' AND '2025-12-31'
```

### 2. Total de Controles e % Não Conformes

```sql
SELECT
  COUNT(*) as total_controles,
  SUM(CRITICAL_CONTROL_NON_COMPLIANCE) as controles_nao_conformes,
  ROUND(
    SUM(CRITICAL_CONTROL_NON_COMPLIANCE) * 100.0 / NULLIF(COUNT(*), 0),
    2
  ) as percentual_nao_conforme
FROM hs_franquia.gold_connect_bot.vw_crm_verification_question q
JOIN hs_franquia.gold_connect_bot.vw_crm_verification v
  ON q.VERIFICATION_ID = v.ID
WHERE v.VERIFICATION_DATE BETWEEN '2025-01-01' AND '2025-12-31'
```

### 3. Priorização de Ações (Gráfico de Barras)

```sql
SELECT
  CASE
    WHEN a.END_DATE < CURRENT_DATE AND a.COMPLETED_DATE IS NULL THEN 'Vencidas'
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
WHERE a.COMPLETED_DATE IS NULL
GROUP BY
  CASE
    WHEN a.END_DATE < CURRENT_DATE AND a.COMPLETED_DATE IS NULL THEN 'Vencidas'
    WHEN a.PRIORITY = 0 THEN 'S=0'
    WHEN a.PRIORITY = 1 THEN 'S=1'
    WHEN a.PRIORITY = 2 THEN 'S=2'
    WHEN a.PRIORITY = 3 THEN 'S=3'
    WHEN a.PRIORITY = 4 THEN 'S=4'
    WHEN a.PRIORITY > 4 THEN 'Posterior a S=4'
    ELSE 'Outros'
  END
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
  END
```

### 4. Lista de Ações em Aberto (Tabela)

```sql
SELECT
  a.ID as id_acao,
  a.VERIFICATION_ID as id_verificacao,
  u.FULL_NAME as responsavel,
  a.END_DATE as data_vencimento_acao,
  CASE
    WHEN a.END_DATE < CURRENT_DATE THEN 'Atrasado'
    ELSE 'Em Andamento'
  END as status_acao,
  a.TYPE as tipo
FROM hs_franquia.gold_connect_bot.vw_crm_action a
LEFT JOIN hs_franquia.gold_connect_bot.vw_crm_user u
  ON a.RESPONSIBLE_PERSON_ID = u.USER_ID
WHERE a.COMPLETED_DATE IS NULL
ORDER BY
  CASE WHEN a.END_DATE < CURRENT_DATE THEN 0 ELSE 1 END,
  a.END_DATE ASC
LIMIT 100
```

---

## Notas Importantes

### 🔑 IDs e Relacionamentos

1. **vw_crm_user**: Sempre usar `USER_ID` (int) para JOINs, NUNCA `ID` (UUID)
2. **VERIFICATION_ID**: String UUID usado em todos os relacionamentos de verificação
3. **ID_UO**: Inteiro usado para hierarquia organizacional

### 📊 Cálculos de Conformidade

- **Verificação não conforme**: Quando possui ao menos UMA pergunta com `CRITICAL_CONTROL_NON_COMPLIANCE = 1`
- **Controle não conforme**: Soma direta de `CRITICAL_CONTROL_NON_COMPLIANCE = 1`
- **Pergunta não conforme**: Mesmo que controle não conforme

### ⚡ Prioridades e Status

- **PRIORITY**: 1 = mais crítico → 4 = menos crítico
- **Ação em aberto**: `COMPLETED_DATE IS NULL`
- **Ação atrasada**: `END_DATE < CURRENT_DATE AND COMPLETED_DATE IS NULL`
- **Ação vencida**: Mesmo que atrasada (terminologia do dashboard)
- **Ver e Agir**: `FIXED_IN_FIELD = 1` (corrigido imediatamente no local)

### 🔍 Filtros Comuns

**Por data**:
```sql
WHERE VERIFICATION_DATE BETWEEN '2025-01-01' AND '2025-12-31'
```

**Por organização**:
```sql
JOIN hs_franquia.gold_connect_bot.vw_general_de_para_hier_org_unit org
  ON v.ID_UO = org.id_uo
WHERE org.uo_level_03 = 'Nome da UO'
```

**Por localização**:
```sql
JOIN hs_franquia.gold_connect_bot.vw_crm_location loc
  ON v.SITE_ID = loc.ID_SITE
WHERE loc.TEXT_PT = 'Nome do Local'
```

**Por tipo de verificação**:
```sql
WHERE TYPE IN ('Manager Verification', 'Operator Verification', 'Supervisor Verification')
```

### 📱 Campos Específicos

- **MOBILE_SUBMISSION = 1**: Verificação feita via tablet/smartphone
- **SCHEDULED = 1**: Verificação agendada (vs. ad-hoc)
- **UNPLANNED_WORK = 1**: Trabalho não planejado identificado
- **EVIDENCE = 1**: Foto ou evidência física coletada
