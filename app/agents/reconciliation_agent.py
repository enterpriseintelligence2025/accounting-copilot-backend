from app.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
import json

SYSTEM_PROMPT = """
You are an invoice reconciliation auditor.

Check:
- Every field in the invoice against the purchase order
- Correctness of tax calculations
- Dates consistency
- PO vs Invoice amounts
- Line item quantity & price
- GST structure:
  - Same state → CGST+SGST
  - Different state → IGST
- Vendor, buyer mismatch
- Also include information about the discrepancies found to serve as justification for the reconciliation summary.

Output STRICT JSON:
{
  "status": "success" | "failure",
  "issues": [{type,description}],
  "next_steps": [],
  "reconciliation_summary": {
    "tax_check": "",
    "amount_match": true,
    "vendor_match": true
  }
}
"""

def reconcile(po_text: str, invoice_text: str) -> dict:
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=f"PURCHASE ORDER:\n{po_text}\n\nINVOICE:\n{invoice_text}"
            )
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.content)
