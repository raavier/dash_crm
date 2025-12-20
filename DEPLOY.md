# Guia de Deploy - Dashboard CRM no Databricks Apps

## Pré-requisitos

1. ✅ Databricks Workspace configurado
2. ✅ Secret scope `connectdata-kv-prd` com key `cnx-databricks-hs-community`
3. ✅ SQL Warehouse e Serving Endpoint já criados
4. ✅ Databricks CLI instalado (opcional, mas recomendado)

## Passo 1: Build do Frontend

```bash
cd frontend
npm install  # Se ainda não instalou
npm run build
```

Isso criará a pasta `frontend/dist` com os arquivos otimizados.

## Passo 2: Verificar Estrutura de Arquivos

Certifique-se que sua estrutura está assim:

```
dash_crm/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   └── ...
├── frontend/
│   └── dist/          # Gerado pelo build
│       ├── index.html
│       └── assets/
├── databricks.yml      # Configuração do bundle
├── .databricks-app.json  # Configuração do app
└── requirements.txt    # Dependências Python
```

## Passo 3: Deploy via Databricks UI

### 3.1 Criar App no Databricks

1. Acesse: `https://adb-116288240407984.4.azuredatabricks.net/#apps`
2. Clique em **"Create new app"**
3. Configure:
   - **Name**: `dash_crm`
   - **Resources**:
     - SQL Warehouse: `Warehouse SQL - X-Small` (ou o seu)
       - Permission: `Can use`
       - Resource key: `sql-warehouse`
     - Serving endpoint: `connect_bot_prd`
       - Permission: `Can query`
       - Resource key: `serving-endpoint`
   - **Compute size**: `Medium - Up to 2 vCPU, 6 GB memory`

4. Clique em **"Create app"**

### 3.2 Upload do Código

Após criar o app, você verá a interface de deploy. Faça upload dos seguintes arquivos/pastas:

```
Selecione a pasta raiz: dash_crm/
```

O Databricks vai fazer upload de:
- `backend/` (todo o código Python)
- `frontend/dist/` (build do React)
- `requirements.txt`
- `databricks.yml`
- `.databricks-app.json`

### 3.3 Aguardar Deploy

O Databricks vai:
1. Instalar dependências Python (`requirements.txt`)
2. Iniciar o servidor Uvicorn
3. Servir o frontend via FastAPI
4. Expor a URL pública do app

Tempo estimado: 5-10 minutos.

## Passo 4: Verificar Deploy

Quando o deploy terminar, você verá:
- ✅ Status: **Running**
- 🌐 URL do app: `https://adb-116288240407984.4.azuredatabricks.net/apps/dash_crm`

### Testes Pós-Deploy

1. **Acessar a URL**: Deve carregar o dashboard
2. **Verificar métricas**: Dados devem carregar do SQL Warehouse
3. **Testar chatbot**: Clicar no botão azul e enviar uma mensagem
4. **Verificar logs**: Databricks Apps > Logs (se houver erro)

## Passo 5: Troubleshooting

### Erro: "Application failed to start"

**Solução**: Verifique os logs no Databricks Apps UI

Causas comuns:
- Dependências faltando no `requirements.txt`
- Secret scope não encontrado
- SQL Warehouse ou Serving Endpoint sem permissão

### Erro: "Frontend não carrega"

**Solução**: 
1. Verifique se `frontend/dist` foi criado corretamente
2. Execute `npm run build` novamente
3. Verifique logs do FastAPI para ver se está servindo arquivos estáticos

### Erro: "Chatbot não responde"

**Solução**:
1. Verifique se o endpoint `connect_bot_prd` está rodando
2. Confirme que a permissão "Can query" foi dada
3. Teste o endpoint diretamente via API

### Erro: "Token inválido"

**Solução**:
1. Verifique se o secret existe:
   ```bash
   databricks secrets list --scope connectdata-kv-prd
   ```
2. Confirme que a key é `cnx-databricks-hs-community`
3. Se necessário, recrie o token:
   ```bash
   databricks secrets put --scope connectdata-kv-prd --key cnx-databricks-hs-community
   ```

## Passo 6: Atualizar Deploy (CI/CD)

Para fazer updates após mudanças no código:

### Via UI:
1. Databricks Apps > `dash_crm` > **Settings**
2. Clique em **"Redeploy"**
3. Upload dos arquivos atualizados

### Via CLI (Recomendado):
```bash
# Build frontend
cd frontend && npm run build && cd ..

# Deploy via Databricks CLI
databricks bundle deploy -t dev

# Ou para produção
databricks bundle deploy -t prod
```

## Configurações Opcionais

### Variáveis de Ambiente Customizadas

Edite `.databricks-app.json` para adicionar mais env vars:

```json
{
  "env": [
    {
      "name": "CACHE_TTL",
      "value": "7200"
    }
  ]
}
```

### Escalar Compute Size

Se o app estiver lento, aumente o compute:
1. Apps > Settings > Compute size
2. Escolha: `Large - Up to 4 vCPU, 16 GB memory`

## URLs Importantes

- **App**: https://adb-116288240407984.4.azuredatabricks.net/apps/dash_crm
- **Logs**: https://adb-116288240407984.4.azuredatabricks.net/apps/dash_crm/logs
- **Settings**: https://adb-116288240407984.4.azuredatabricks.net/apps/dash_crm/settings

## Próximos Passos

Após deploy bem-sucedido:
- [ ] Configurar monitoramento (Databricks Apps Metrics)
- [ ] Adicionar autenticação SSO (se necessário)
- [ ] Configurar alertas para erros
- [ ] Documentar acesso para usuários finais
