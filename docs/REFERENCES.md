# Referências do Projeto

Este arquivo contém links e referências para os boilerplates e recursos utilizados no desenvolvimento do Dashboard CRM.

## Frontend Dashboard

**Status**: Desenvolvimento customizado
**Tecnologia**: React
**Propósito**: Dashboard customizado para visualização de dados CRM com chatbot integrado

### Abordagem
- Dashboard será desenvolvido do zero com React
- Design pensado para integração nativa com o chatbot widget
- Componentes personalizados para as necessidades específicas do CRM
- Biblioteca de componentes a definir (Chakra UI, Material-UI, Ant Design, ou outra)

---

## Frontend Chatbot

**Template Base**: Databricks E2E Chatbot App (Next.js)
**URL**: https://github.com/databricks/app-templates/tree/main/e2e-chatbot-app
**Tecnologia**: Next.js

### ⚠️ ADAPTAÇÃO NECESSÁRIA

Este template está configurado como uma página full-page. Precisamos adaptar para:

**Objetivo**: Criar um **chatbot widget (embedded chat interface)** que:
- Fique fixo no canto inferior direito da página
- Tenha um botão circular (floating action button) para abrir/fechar
- Expanda uma janela de conversação quando clicado
- Seja integrado ao dashboard principal (não uma página separada)
- Mantenha o estado da conversa

**Referências de UI para o widget**:
- Botão circular flutuante (similar a Intercom, Drift, etc.)
- Janela popup/modal para o chat (aproximadamente 400x600px)
- Animações de expansão/contração
- Indicador de novas mensagens (badge)

---

## Backend - Endpoint do Chatbot

**Databricks Serving Endpoint**
**URL**: https://adb-116288240407984.4.azuredatabricks.net/serving-endpoints/connect_bot_prd/invocations

### Configuração
- Endpoint já deployado no Databricks
- Autenticação via Databricks token
- Aceita requests POST com mensagens do usuário
- Retorna respostas do chatbot

### Integração
```python
# Exemplo de chamada ao endpoint
import requests

headers = {
    "Authorization": f"Bearer {databricks_token}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [
        {"role": "user", "content": "Sua pergunta aqui"}
    ]
}

response = requests.post(
    "https://adb-116288240407984.4.azuredatabricks.net/serving-endpoints/connect_bot_prd/invocations",
    headers=headers,
    json=payload
)
```

---

## Estrutura das Tabelas

**Status**: Pendente
**Formato**: A definir (SQL DDL, JSON schema, ou documentação)

### Informações Necessárias
- Schema das tabelas CRM
- Relacionamentos entre tabelas
- Campos principais e tipos de dados
- Índices e constraints
- Exemplos de queries comuns

---

## Notas de Implementação

### Integração Dashboard + Chatbot Widget

1. **Dashboard Principal**: Desenvolvimento customizado com React
2. **Chatbot Widget**: Extrair componentes do template Databricks e adaptar
3. **Integração**: Montar o widget como um componente React que pode ser adicionado a qualquer página do dashboard
4. **Estado Global**: Considerar Context API ou Redux para gerenciar estado do chat

### Arquitetura de Componentes Sugerida

```
src/
  ├── components/
  │   ├── Dashboard/          # Componentes customizados do dashboard
  │   ├── ChatWidget/         # Chatbot widget adaptado
  │   │   ├── ChatButton.jsx  # Botão flutuante
  │   │   ├── ChatWindow.jsx  # Janela de chat
  │   │   ├── ChatMessage.jsx # Componentes de mensagem
  │   │   └── ChatWidget.jsx  # Container principal
  │   └── ...
  ├── services/
  │   └── chatService.js      # API calls para o endpoint
  └── ...
```

### Próximos Passos

- [ ] Definir biblioteca de componentes UI (Chakra UI, Material-UI, Ant Design, etc.)
- [ ] Criar estrutura base do dashboard React
- [ ] Clonar e estudar template de chatbot Databricks
- [ ] Receber estrutura das tabelas CRM
- [ ] Adaptar chatbot de full-page para widget embedded
- [ ] Integrar widget ao dashboard
- [ ] Conectar ao endpoint do Databricks
- [ ] Implementar queries das tabelas CRM
