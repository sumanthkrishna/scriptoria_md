from utils.export_video import sections_from_html

def test_sections():
    result = sections_from_html("<h1>Intro</h1><p>Hello world</p><h2>Next</h2><p>Another section</p>")
    assert len(result) == 2
    assert "Hello world" in result[0]["text"]

def test_empty():
    assert sections_from_html("") == []
