# Dashboard CRM - Frontend

Dashboard React para visualização de dados do sistema de Gerenciamento de Riscos Críticos (Control Risk Management).

## 🚀 Tecnologias

- **React 18** com **TypeScript**
- **Vite** - Build tool
- **Chakra UI** - Biblioteca de componentes
- **Recharts** - Biblioteca de gráficos
- **Axios** - Cliente HTTP
- **date-fns** - Manipulação de datas
- **React Context API** - Gerenciamento de estado

## 🎨 Paleta de Cores Vale

```typescript
{
  primary: '#007E7A',      // Verde Vale - cor principal
  secondary: '#ECB11F',    // Amarelo - atenção/warning
  tertiary: '#E37222',     // Laranja
  danger: '#BB133E',       // Vermelho - dados negativos/erro
  info: '#3D7EDB',         // Azul - informações neutras
  cyan: '#00B0CA',
  success: '#69BE28',      // Verde claro - dados positivos/sucesso
  warning: '#DFDF00',      // Amarelo limão - atenção
  gray: '#747678',         // Cinza - dados neutros
}
```

## 📁 Estrutura do Projeto

```
src/
├── components/
│   ├── Dashboard/
│   │   ├── MetricsCards.tsx           # 3 cards de métricas principais
│   │   ├── ActionPriorityChart.tsx    # Gráfico de barras (priorização)
│   │   ├── ActionsTable.tsx           # Tabela de ações em aberto
│   │   └── FilterBar.tsx              # Barra de filtros
│   ├── Layout/
│   │   ├── Header.tsx                 # Header com logo e tabs
│   │   └── MainLayout.tsx             # Layout principal
│   └── Common/
│       ├── LoadingSpinner.tsx         # Componente de loading
│       └── ErrorAlert.tsx             # Componente de erro
├── context/
│   └── DashboardContext.tsx           # Context API para estado global
├── services/
│   ├── api.ts                         # Configuração Axios
│   └── dashboardService.ts            # Serviço de dados (com mocks)
├── types/
│   └── dashboard.types.ts             # Tipos TypeScript
├── pages/
│   └── DashboardPage.tsx              # Página principal
├── theme.ts                           # Tema Chakra UI customizado
├── App.tsx                            # App principal
└── main.tsx                           # Entry point
```

## 🏃 Como Executar

### Instalação

```bash
npm install
```

### Desenvolvimento

```bash
npm run dev
```

O dashboard estará disponível em: http://localhost:5173

### Build para Produção

```bash
npm run build
```

### Preview da Build

```bash
npm run preview
```

## 📊 Funcionalidades Implementadas

### ✅ Métricas Principais
- 3 cards com totais e percentuais de não conformidade
- Cores dinâmicas baseadas em thresholds:
  - Verde: < 5% (positivo)
  - Amarelo: 5-10% (atenção)
  - Vermelho: > 10% (negativo)

### ✅ Gráfico de Priorização
- Gráfico de barras horizontal com Recharts
- 7 categorias: Vencidas, S=0, S=1, S=2, S=3, S=4, Posterior a S=4
- Cores da paleta Vale aplicadas por prioridade

### ✅ Tabela de Ações
- Tabela responsiva com dados paginados
- Colunas: ID Ação, ID Verificação, Responsável, Data, Status, Tipo
- Badges coloridos para status (Atrasado/Em Andamento)
- Paginação funcional

### ✅ Filtros
- 4 filtros principais: Organização, Localização, Tipo, Data
- Botão "Aplicar filtros" para refresh
- Display de última atualização

### ✅ Header
- Logo Vale e título
- Tabs: FMDS, Detalhamento, Ações
- Botões de idioma PT/EN
- Versão do sistema

## 🔄 Estado e Dados

Atualmente, o dashboard utiliza **dados mock** para desenvolvimento independente do backend.

Os dados mock estão em `src/services/dashboardService.ts` e incluem:
- Métricas baseadas na imagem de referência fornecida
- 7 ações de exemplo
- Prioridades com contagens realistas

## 🔌 Integração com Backend (Próximo Passo)

Para conectar ao backend Python:

1. Configure as variáveis de ambiente em `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_DATABRICKS_ENDPOINT=https://adb-116288240407984.4.azuredatabricks.net
VITE_CHATBOT_ENDPOINT=/serving-endpoints/connect_bot_prd/invocations
```

2. Atualize `dashboardService.ts` para fazer chamadas reais:
```typescript
async getMetrics(filters: DashboardFilters): Promise<MetricsData> {
  const response = await api.post('/api/metrics', filters);
  return response.data;
}
```

3. O backend deve expor endpoints REST:
   - `POST /api/metrics` - Retorna métricas principais
   - `POST /api/action-priorities` - Retorna dados do gráfico
   - `POST /api/actions` - Retorna ações paginadas
   - `GET /api/filter-options` - Retorna opções de filtros

## 📱 Responsividade

O dashboard é totalmente responsivo:
- **Desktop** (1920px+): Layout em grid 3 colunas
- **Tablet** (768-1919px): Layout em 2 colunas
- **Mobile** (< 768px): Layout vertical (stack)

## 🎯 Próximas Funcionalidades

- [ ] Chatbot widget (canto inferior direito)
- [ ] Integração com backend Python
- [ ] Autenticação Databricks
- [ ] Mais filtros avançados (modal)
- [ ] Exportação de dados
- [ ] Dark mode (opcional)
- [ ] Internacionalização (i18n)

## 📝 Notas de Desenvolvimento

- Todos os componentes são **funcionais** com TypeScript
- Estado gerenciado com **Context API**
- Componentes seguem padrão de **composição**
- Cores seguem **paleta oficial Vale**
- Código preparado para **testes** (Jest + RTL no futuro)
