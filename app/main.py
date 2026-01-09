from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest, ChatResponse, FileResponse
from app.agents.chat_agent import chat, stream_chat
from app.agents.invoice_agent import generate_invoice
from app.agents.reconciliation_agent import reconcile
from app.utils.pdf_loader import read_pdf
from app.utils.validators import is_purchase_order, is_invoice
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agentic Finance Backend")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
def chat_route(req: ChatRequest):
    reply = chat([m.dict() for m in req.messages])
    return {"reply": reply}


@app.post("/chat/stream")
async def chat_stream_route(request: Request):
    body = await request.json()
    messages = body["messages"]

    def event_generator():
        for token in stream_chat(messages):
            yield token

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )


@app.post("/invoice/generate", response_model=FileResponse)
async def invoice_route(file: UploadFile = File(...)):
    pdf_data = await read_pdf(file)

    if not is_purchase_order(pdf_data["raw_text"]):
        return {
            "status": "failure",
            "issues": ["File is not a valid Purchase Order"],
            "next_steps": ["Upload a valid PO PDF"]
        }

    try:
        data = generate_invoice(pdf_data["raw_text"])
        return {"status": "success", "data": data}

    except ValueError as e:
        return {
            "status": "failure",
            "issues": ["Invoice extraction failed due to schema mismatch"],
            "next_steps": [
                "Retry generation",
                "Verify PO document structure"
            ]
        }



@app.post("/reconcile", response_model=FileResponse)
async def reconcile_route(
    po: UploadFile = File(...),
    invoice: UploadFile = File(...)
):
    po_text = await read_pdf(po)
    invoice_text = await read_pdf(invoice)

    if not is_purchase_order(po_text["raw_text"]) or not is_invoice(invoice_text["raw_text"]):
        return {
            "status": "failure",
            "issues": ["Invalid PO or Invoice document"],
            "next_steps": ["Upload correct PDF documents"]
        }

    return {
        "status": "success",
        "data": reconcile(po_text["raw_text"], invoice_text["raw_text"])
    }
