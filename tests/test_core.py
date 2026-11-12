import pytest
from utils.markdown_renderer import render_markdown, headings, search_matches
from utils.file_handler import validate_path, fetch_url
from utils.sanitizer import sanitize_html

def test_render():
    html=render_markdown("# Hello\n\n| A | B |\n|---|---|\n|1|2|")
    assert "<h1" in html and "<table>" in html

def test_sanitize():
    assert "onerror" not in sanitize_html('<img src="x" onerror="alert(1)">')
    assert "<script" not in sanitize_html('<script>alert(1)</script>')

def test_headings():
    assert headings(render_markdown("# Title"))[0][1]=="Title"

def test_search():
    assert search_matches("abc ABC","abc")==2

def test_paths(tmp_path,monkeypatch):
    monkeypatch.setenv("SCRIPTORIA_ALLOWED_PATHS",str(tmp_path))
    assert validate_path(tmp_path)==tmp_path.resolve()
    with pytest.raises(PermissionError): validate_path(tmp_path.parent)

def test_url_rejects_http():
    with pytest.raises(ValueError): fetch_url("http://example.com")
