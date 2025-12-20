# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dashboard CRM (Control Risk Management) - A workplace safety management dashboard with integrated chatbot, deployed on Databricks Apps.

## Project Structure

```
dash_crm/
├── docs/               # All documentation
│   ├── CLAUDE.md      # This file
│   ├── PROJECT_OVERVIEW.md
│   ├── REFERENCES.md
│   ├── DATABASE_SCHEMA.md  # Complete database documentation
│   ├── main.ipynb     # Databricks queries notebook
│   └── crm_table_metadata.csv
├── frontend/          # React app (dashboard + chatbot)
├── backend/           # Python backend (Databricks)
└── README.md          # Project overview
```

## Technology Stack

- **Frontend**: React
- **Backend**: Python (runs entirely on Databricks)
- **Deployment**: Databricks Apps
- **Integration**: Databricks SQL for data queries, Databricks APIs for chatbot

## Architecture

### Frontend (React)
- Dashboard visualization for CRM data
- Integrated chatbot interface
- Communicates with Databricks backend via REST APIs

### Backend (Python on Databricks)
- All backend logic runs on Databricks platform
- Handles data processing and queries from CRM tables
- Chatbot endpoint for AI-powered interactions
- Direct integration with Databricks SQL warehouse

### Data Layer
- CRM tables stored in Databricks
- Structured data for workplace safety metrics and risk management
- Accessed via Databricks SQL queries

## Development Commands

### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Backend (Databricks)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run locally (if applicable)
python app.py

# Deploy to Databricks Apps
databricks apps deploy
```

## Key Integration Points

1. **Databricks Apps Deployment**: Both frontend and backend are deployed as a Databricks App
2. **Chatbot Endpoint**: Python backend exposes REST endpoint for chatbot interactions
3. **CRM Data Access**: Backend queries Databricks tables directly using Databricks SQL
4. **Authentication**: Uses Databricks authentication/authorization mechanisms

## Database Documentation

**Complete schema documentation**: See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

### Main Tables
- `hs_franquia.gold_connect_bot.vw_crm_action` - Actions (corrective/preventive)
- `hs_franquia.gold_connect_bot.vw_crm_verification` - Safety verifications
- `hs_franquia.gold_connect_bot.vw_crm_verification_question` - Checklist responses
- `hs_franquia.gold_connect_bot.vw_crm_user` - Users (⚠️ Use USER_ID for JOINs, not ID)
- `hs_franquia.gold_connect_bot.vw_crm_location` - Locations hierarchy
- `hs_franquia.gold_connect_bot.vw_general_de_para_hier_org_unit` - Organizational units

### Key Points
- **Non-compliance**: `CRITICAL_CONTROL_NON_COMPLIANCE = 1` means NOK
- **Open actions**: `COMPLETED_DATE IS NULL`
- **Overdue actions**: `END_DATE < CURRENT_DATE AND COMPLETED_DATE IS NULL`
- **Priority**: 1 = critical, 4 = low

## Important Notes

- All backend code must be compatible with Databricks runtime environment
- Use Databricks SDK for Python (`databricks-sdk`) for platform integrations
- Frontend should handle authentication tokens from Databricks
- Chatbot responses may leverage Databricks AI/ML capabilities
- **Database queries**: Always refer to DATABASE_SCHEMA.md for correct table/column names and relationships
