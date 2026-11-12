import base64
from utils.document_assets import embed_local_images

def test_embeds_allowed_image(tmp_path, monkeypatch):
    monkeypatch.setenv("SCRIPTORIA_ALLOWED_PATHS", str(tmp_path))
    folder = tmp_path / "docs"
    folder.mkdir()
    (folder / "image.png").write_bytes(b"PNG")
    doc = folder / "readme.md"
    doc.write_text("hello")
    result = embed_local_images('<img src="image.png">', str(doc))
    assert "data:image/png;base64," in result

def test_blocks_traversal(tmp_path, monkeypatch):
    folder = tmp_path / "docs"
    folder.mkdir()
    doc = folder / "readme.md"
    doc.write_text("hello")
    monkeypatch.setenv("SCRIPTORIA_ALLOWED_PATHS", str(folder))
    result = embed_local_images('<img src="../../secret.png">', str(doc))
    assert "data:image" not in result
    assert "image unavailable" in result

def test_external_urls_unchanged(tmp_path, monkeypatch):
    monkeypatch.setenv("SCRIPTORIA_ALLOWED_PATHS", str(tmp_path))
    doc = tmp_path / "a.md"
    doc.write_text("hello")
    assert "https://example.org/x.png" in embed_local_images('<img src="https://example.org/x.png">', str(doc))
