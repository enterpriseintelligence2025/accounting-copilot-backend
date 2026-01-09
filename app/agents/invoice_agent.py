from app.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas import InvoiceSchema
import json
from pydantic import ValidationError

SYSTEM_PROMPT = """
You are a financial agent whose job is to create proper invoice in compliance in with the Indian financial laws from the available purchase order information.

IMPORTANT OUTPUT RULES (MANDATORY):
- All financial figures MUST match the calculations exactly
- Do NOT round any numbers
- Output a SINGLE, FLAT JSON object
- DO NOT nest under keys like "purchase_order", "invoice", "data"
- ALL fields MUST exist at the top level
- Field names MUST EXACTLY match the schema
- Do NOT rename fields
- Do NOT omit fields
- If a value is missing, infer it or use null

TAX RULES (INDIA GST):
- If vendor.state == ship_to.state:
    cgst = 9%
    sgst = 9%
    igst = 0
- Else:
    igst = 18%
    cgst = 0
    sgst = 0
- Total tax must be exactly 18%

OUTPUT FORMAT:
Return ONLY valid JSON.
No explanations.
No markdown.
No nesting.

Schema (top-level):
{
  po_number: string,
  invoice_date: string,
  delivery_date: string,
  payment_terms: string,
  amount_in_words: string,
  vendor: { name, address, gstin, state },
  ship_to: { name, address, state },
  sold_to: { name, address, gstin, state },
  line_items: [
    { sno, description, hsn_code, quantity, unit_rate, amount }
  ],
  subtotal: number,
  taxes: { cgst, sgst, igst },
  total_amount: number,
  notes: string[]
}
"""

def generate_invoice(po_text: str) -> dict:
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=po_text)
        ],
        response_format={"type": "json_object"}
    )

    parsed = json.loads(response.content)

    try:
        return InvoiceSchema(**parsed).dict()
    except ValidationError as e:
        raise ValueError(
            f"LLM output did not match invoice schema: {e.errors()}"
        )