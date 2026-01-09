from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# -------- Chat --------
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

# -------- File-based --------
class FileResponse(BaseModel):
    status: str
    data: Dict[str, Any] | None = None
    issues: List[str] | None = None
    next_steps: List[str] | None = None


class LineItem(BaseModel):
    sno: int
    description: str
    hsn_code: str
    quantity: int
    unit_rate: float
    amount: float

class Party(BaseModel):
    name: str
    address: str
    gstin: Optional[str] = None
    state: str

class Tax(BaseModel):
    cgst: Optional[float] = 0
    sgst: Optional[float] = 0
    igst: Optional[float] = 0

class InvoiceSchema(BaseModel):
    po_number: str
    invoice_date: str
    delivery_date: str
    payment_terms: str
    amount_in_words: str

    vendor: Party
    ship_to: Party
    sold_to: Party

    line_items: List[LineItem]
    subtotal: float
    taxes: Tax
    total_amount: float
    notes: List[str]
