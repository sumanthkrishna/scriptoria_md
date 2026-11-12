"""Safe local file browsing, uploads and URL downloads."""
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from requests_ntlm import HttpNtlmAuth

MAX_BYTES = 15 * 1024 * 1024

def allowed_roots():
    return [Path(p).expanduser().resolve() for p in os.getenv("SCRIPTORIA_ALLOWED_PATHS", str(Path.home())).split(";") if p.strip()]

def validate_path(path):
    candidate = Path(path).expanduser().resolve()
    if not any(candidate == root or root in candidate.parents for root in allowed_roots()):
        raise PermissionError("Path is outside SCRIPTORIA_ALLOWED_PATHS")
    return candidate

def list_markdown_files(root):
    root = validate_path(root)
    if not root.is_dir():
        raise ValueError("Not a directory")
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in (".md", ".markdown") and not p.is_symlink())

def read_markdown(path):
    path = validate_path(path)
    if path.suffix.lower() not in (".md", ".markdown", ".html", ".htm"):
        raise ValueError("Unsupported file type")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("File too large")
    return path.read_text(encoding="utf-8-sig")

def fetch_url(url, username="", password="", domain=""):
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are supported")
    # SSRF guard: reject loopback, private and link-local IPs, including DNS results.
    import socket, ipaddress
    host = parsed.hostname
    if not host:
        raise ValueError("Missing hostname")
    def check_host(name):
        for info in socket.getaddrinfo(name, None):
            ip = ipaddress.ip_address(info[4][0])
            if not ip.is_global:
                raise ValueError("Non-public network destination blocked")
    check_host(host)
    auth = HttpNtlmAuth((domain + "\\" if domain else "") + username, password) if username else None
    session = requests.Session()
    session.trust_env = False
    current = url
    for _ in range(5):
        check_host(urlparse(current).hostname)
        response = session.get(current, timeout=(5,20), verify=True, auth=auth,
                               allow_redirects=False, stream=True)
        if response.status_code in (301,302,303,307,308):
            current = urljoin(current, response.headers["Location"])
            if urlparse(current).scheme != "https":
                raise ValueError("Insecure redirect blocked")
            continue
        response.raise_for_status()
        chunks, size = [], 0
        for chunk in response.iter_content(65536):
            size += len(chunk)
            if size > MAX_BYTES:
                raise ValueError("Remote document too large")
            chunks.append(chunk)
        return b"".join(chunks).decode("utf-8-sig"), current
    raise ValueError("Too many redirects")
