"""DOCX export preserving headings, paragraphs, lists, tables and code blocks."""
from io import BytesIO
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt

def export_docx(html, title="Scriptoria"):
    doc = Document()
    doc.add_heading(title,0)
    soup = BeautifulSoup(html,"html.parser")
    for el in soup.find_all(recursive=False):
        tag = el.name
        if tag in ("h1","h2","h3","h4","h5","h6"):
            doc.add_heading(el.get_text(" ",strip=True), level=min(int(tag[1]),4))
        elif tag in ("p","blockquote","pre"):
            p = doc.add_paragraph(el.get_text(" ",strip=True))
            if tag == "pre":
                p.style = "No Spacing"
                for run in p.runs: run.font.name = "Courier New"; run.font.size = Pt(9)
        elif tag in ("ul","ol"):
            for li in el.find_all("li",recursive=False):
                doc.add_paragraph(li.get_text(" ",strip=True),style="List Bullet" if tag=="ul" else "List Number")
        elif tag == "table":
            rows = el.find_all("tr")
            if rows:
                width = max(len(r.find_all(["td","th"],recursive=False)) for r in rows)
                table = doc.add_table(rows=len(rows), cols=width)
                table.style = "Table Grid"
                for i,r in enumerate(rows):
                    for j,c in enumerate(r.find_all(["td","th"],recursive=False)):
                        table.cell(i,j).text = c.get_text(" ",strip=True)
    buf=BytesIO();doc.save(buf);return buf.getvalue()
