from fastapi import UploadFile
import tempfile
import camelot
import pdfplumber
import re


async def read_pdf(file: UploadFile) -> dict:
    """
    Robust PDF reader for Purchase Orders.
    - Camelot: table extraction
    - pdfplumber: non-table text
    """

    # -----------------------------
    # Save uploaded PDF temporarily
    # -----------------------------
    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        pdf_path = tmp.name

    # -----------------------------
    # 1. Extract TABLES (Line Items)
    # -----------------------------
    tables = camelot.read_pdf(
        pdf_path,
        pages="all",
        flavor="lattice"  # best for bordered tables like PO
    )

    line_items = []
    for table in tables:
        df = table.df

        # Normalize header
        df.columns = df.iloc[0]
        df = df[1:]

        # Clean rows
        records = df.to_dict(orient="records")
        for r in records:
            cleaned = {k.strip(): (v.strip() if isinstance(v, str) else v)
                       for k, v in r.items()}
            line_items.append(cleaned)

    # -----------------------------
    # 2. Extract NON-TABLE TEXT
    # -----------------------------
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

    raw_text = "\n".join(full_text)

    # -----------------------------
    # 3. Metadata Extraction
    # -----------------------------
    def find(pattern):
        match = re.search(pattern, raw_text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    metadata = {
        "po_number": find(r"Purchase Order Number:\s*(.+)"),
        "po_date": find(r"Date:\s*(.+)"),
        "delivery_date": find(r"Delivery/Completion Date:\s*(.+)"),
        "payment_terms": find(r"Payment Terms:\s*(.+)"),
        "vendor_name": find(r"Vendor:\s*(?:Vendor No:.*\n)?(.+)"),
        "vendor_gstin": find(r"Vendor:.*GSTIN No\.\:\s*(.+)")
    }

    # -----------------------------
    # 4. Tax & Totals Extraction
    # -----------------------------
    taxes = {
        "sgst": find(r"SGST.*?:\s*([\d,]+\.\d{2})"),
        "cgst": find(r"CGST.*?:\s*([\d,]+\.\d{2})"),
        "total_tax": find(r"Total Tax:\s*([\d,]+\.\d{2})")
    }

    totals = {
        "total_value": find(r"Total Purchase Value.*?:\s*([\d,]+\.\d{2})"),
        "amount_in_words": find(r"Amount in Words:\s*(.+)")
    }

    # -----------------------------
    # 5. Final Structured Output
    # -----------------------------
    return {
        "raw_text": raw_text,
        "line_items": line_items,
        "metadata": metadata,
        "taxes": taxes,
        "totals": totals
    }
