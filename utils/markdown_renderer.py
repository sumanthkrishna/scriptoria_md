"""GFM-like Markdown renderer with safe HTML and local Mermaid diagrams."""
import re
from pathlib import Path
from urllib.parse import urlparse
import markdown
from bs4 import BeautifulSoup
from .sanitizer import sanitize_html

EXTENSIONS = ["tables","fenced_code","codehilite","toc","sane_lists","attr_list",
              "pymdownx.tasklist","pymdownx.superfences","pymdownx.tilde"]

def render_markdown(source: str, base_dir=None):
    # Mermaid fences are converted into local diagram placeholders before Markdown parsing.
    diagrams = []
    def capture(match):
        diagrams.append(match.group(1))
        return "\n\nSCRIPTORIA_MERMAID_" + str(len(diagrams)-1) + "\n\n"
    source = re.sub(r"```mermaid\s*\n(.*?)\n```", capture, source, flags=re.S|re.I)
    html = markdown.markdown(source, extensions=EXTENSIONS, extension_configs={
        "codehilite":{"guess_lang":False}, "toc":{"permalink":False}})
    html = sanitize_html(html)
    for i, diagram in enumerate(diagrams):
        from html import escape
        html = html.replace("<p>SCRIPTORIA_MERMAID_" + str(i) + "</p>",
                            '<pre class="mermaid">' + escape(diagram) + '</pre>')
    return html

def headings(html):
    soup = BeautifulSoup(html,"html.parser")
    return [(int(tag.name[1]), tag.get_text(" ",strip=True), tag.get("id",""))
            for tag in soup.find_all(re.compile(r"^h[1-6]$"))]

def plain_text(html):
    return BeautifulSoup(html,"html.parser").get_text("\n",strip=True)

def search_matches(text, term):
    if not term:
        return 0
    return len(re.findall(re.escape(term), text, flags=re.I))
