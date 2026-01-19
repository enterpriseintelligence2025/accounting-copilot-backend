# Accounting Copilot – Backend Documentation

## 1. Backend Overview

The **Accounting Copilot Backend** is a FastAPI-based AI service that handles chat, invoice generation, and document reconciliation using LLM agents.

---

## 2. Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **LLM**: Azure OpenAI (GPT-4o-mini) via LangChain
- **PDF Processing**: pdfplumber, pypdf
- **Validation**: Pydantic
- **Server**: Uvicorn

---

## 3. Architecture

- Stateless REST API
- Agent-based business logic
- Streaming and JSON responses

---

## 4. Folder Structure

```text
Backend/
├── .env
├── Dockerfile
├── requirements.txt
└── app/
    ├── main.py
    ├── config.py
    ├── llm.py
    ├── schemas.py
    ├── agents/
    └── utils/
```

---

## 5. Core Agents

- **Chat Agent**: Conversational queries
- **Invoice Agent**: PO → Invoice extraction
- **Reconciliation Agent**: PO vs Invoice validation

---

## 6. API Endpoints

- `POST /chat`
- `POST /chat/stream`
- `POST /invoice/generate`
- `POST /reconcile`

---

## 7. Environment Variables

```env
AZURE_OPENAI_API_KEY=***
AZURE_OPENAI_ENDPOINT=***
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

---

## 8. Local Development

```bash
cd Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 9. Deployment

- Docker-based deployment
- Suitable for Azure Container Apps, ECS, or Kubernetes

---

## 10. Future Improvements

- Authentication & authorization
- Database persistence
- Background job processing
- Test coverage
