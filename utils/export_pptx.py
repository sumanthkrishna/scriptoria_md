"""Section-based presentation export."""
from io import BytesIO
from bs4 import BeautifulSoup
from pptx import Presentation
from pptx.util import Inches,Pt

def export_pptx(html, title="Scriptoria"):
    prs=Presentation()
    prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
    first=prs.slides.add_slide(prs.slide_layouts[0])
    first.shapes.title.text=title
    first.placeholders[1].text="Generated with Scriptoria"
    sections=[]
    current=None
    for el in BeautifulSoup(html,"html.parser").find_all(["h1","h2","h3","p","li","pre"]):
        if el.name.startswith("h"):
            current={"title":el.get_text(" ",strip=True),"items":[]}
            sections.append(current)
        else:
            if current is None:
                current={"title":"Overview","items":[]};sections.append(current)
            current["items"].append(el.get_text(" ",strip=True))
    for section in sections:
        chunks=[section["items"][i:i+7] for i in range(0,len(section["items"]),7)] or [[]]
        for chunk in chunks:
            slide=prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text=section["title"][:120]
            frame=slide.placeholders[1].text_frame;frame.clear()
            for idx,item in enumerate(chunk):
                p=frame.paragraphs[0] if idx==0 else frame.add_paragraph()
                p.text=item[:350];p.font.size=Pt(20)
    buf=BytesIO();prs.save(buf);return buf.getvalue()
