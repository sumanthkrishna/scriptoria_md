"""Sanitize rendered Markdown, allowing safe HTML and controlled diagram markup."""
import bleach

TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    "h1","h2","h3","h4","h5","h6","p","pre","code","blockquote","hr","br",
    "table","thead","tbody","tr","th","td","img","input","del","s","div",
    "span","details","summary","sup","sub","figure","figcaption"
}
ATTRS = {"*": ["class","id","title"], "a":["href","title","rel"], "img":["src","alt","title"],
         "input":["type","checked","disabled"], "th":["align"], "td":["align"]}
PROTOCOLS = ["http","https","mailto","data"]

def sanitize_html(html: str) -> str:
    return bleach.clean(html, tags=TAGS, attributes=ATTRS, protocols=PROTOCOLS, strip=True)
