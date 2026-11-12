"""Safely resolve document-relative images into embedded data URIs."""
import base64
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from .file_handler import validate_path

MAX_IMAGE_BYTES = 5 * 1024 * 1024
IMAGE_MIME = {"image/png", "image/jpeg", "image/gif", "image/webp"}

def embed_local_images(html: str, document_path: str | None) -> str:
    """Embed allowed local images, never resolving a file outside configured roots."""
    if not document_path:
        return html
    base = validate_path(document_path).parent
    soup = BeautifulSoup(html, "html.parser")
    for image in soup.select("img[src]"):
        src = image.get("src", "")
        parsed = urlsplit(src)
        if parsed.scheme or parsed.netloc or src.startswith(("/", "\\")):
            continue
        relative = unquote(parsed.path)
        if not relative:
            continue
        try:
            target = validate_path(base / relative)
            if not target.is_file() or target.stat().st_size > MAX_IMAGE_BYTES:
                raise ValueError("Image missing or too large")
            mime = mimetypes.guess_type(target.name)[0]
            if mime not in IMAGE_MIME:
                raise ValueError("Unsupported image format")
            data = base64.b64encode(target.read_bytes()).decode("ascii")
            image["src"] = f"data:{mime};base64,{data}"
        except (OSError, ValueError, PermissionError):
            image["src"] = ""
            image["alt"] = image.get("alt", "") + " [image unavailable]"
    return str(soup)
