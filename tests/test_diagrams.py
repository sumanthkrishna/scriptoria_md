from utils.diagrams import extract_mermaid,strip_mermaid

def test_extract_multiple():
    md="# A\n```mermaid\nflowchart LR\n A-->B\n```\nText\n```mermaid\nsequenceDiagram\n A->>B: Hi\n```"
    diagrams=extract_mermaid(md)
    assert len(diagrams)==2
    assert diagrams[0].startswith("flowchart")
    assert "sequenceDiagram" in diagrams[1]

def test_strip_does_not_execute():
    source="```mermaid\nflowchart LR\n A-->B\n```"
    assert "A-->B" not in strip_mermaid(source)
