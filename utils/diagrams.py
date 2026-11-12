"""Extract Mermaid fenced blocks from Markdown without executing their contents."""
import re

MERMAID_FENCE = re.compile(r"^\s*```mermaid\s*\n(.*?)^\s*```\s*$", re.I | re.M | re.S)

def extract_mermaid(source: str):
    return [match.group(1).strip() for match in MERMAID_FENCE.finditer(source)]

def strip_mermaid(source: str):
    return MERMAID_FENCE.sub("\n\n[Mermaid diagram — see Diagrams tab]\n\n",source)
