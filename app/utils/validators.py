def is_purchase_order(text: str) -> bool:
    keywords = ["purchase order", "po number", "vendor", "quantity"]
    return any(k.lower() in text.lower() for k in keywords)

def is_invoice(text: str) -> bool:
    keywords = ["invoice", "invoice number", "tax", "total amount"]
    return any(k.lower() in text.lower() for k in keywords)
