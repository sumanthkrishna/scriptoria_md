"""Styled PDF export using xhtml2pdf."""
from io import BytesIO
from xhtml2pdf import pisa

def export_pdf(html, title="Scriptoria"):
    css = """@page {size:a4; margin:22mm;} body {font-family:Helvetica; color:#19324a;}
    h1,h2,h3 {color:#1765a2;} pre {background:#f1f4f8; padding:10px;}
    table {border-collapse:collapse;} th,td {border:1px solid #b9c9d7; padding:6px;}"""
    document = f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><h1>{title}</h1>{html}</body></html>'
    output = BytesIO()
    result = pisa.CreatePDF(document, dest=output)
    if result.err:
        raise RuntimeError("PDF generation failed")
    return output.getvalue()
