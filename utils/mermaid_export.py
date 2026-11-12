"""Mermaid PNG rendering via configured external rendering endpoint."""
import os
import requests

def mermaid_png(source: str) -> bytes:
    endpoint = os.getenv("MERMAID_INK_URL", "").strip()
    if not endpoint:
        raise RuntimeError("Set MERMAID_INK_URL to a trusted Mermaid rendering service")
    if not endpoint.startswith("https://"):
        raise ValueError("Mermaid renderer must use HTTPS")
    import base64
    encoded = base64.urlsafe_b64encode(source.encode()).decode().rstrip("=")
    response = requests.get(endpoint.rstrip("/") + "/img/" + encoded, timeout=20, verify=True)
    response.raise_for_status()
    if not response.headers.get("Content-Type","").startswith("image/"):
        raise ValueError("Renderer did not return an image")
    return response.content
