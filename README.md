# Scriptoria — Enterprise Markdown Studio

Streamlit document reader supporting Markdown, HTML, local folders, multi-file uploads, HTTPS sources, search, recent documents, browser text-to-speech, PDF, Word, PowerPoint and narrated MP4 export.

## Windows quick start

```powershell
git clone https://github.com/sumanthkrishna/scriptoria_md.git
cd scriptoria_md
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -q
streamlit run app.py
```

Install [FFmpeg](https://ffmpeg.org/download.html) and ensure `ffmpeg` is available on PATH for video exports. Visit http://localhost:8501.

## Docker

```bash
docker build -t scriptoria .
docker run --rm -p 8501:8501 -e SCRIPTORIA_ALLOWED_PATHS=/app/docs scriptoria
```

## Settings

- `SCRIPTORIA_ALLOWED_PATHS`: semicolon-separated allowed filesystem roots (default: home directory).
- `MERMAID_INK_URL`: HTTPS Mermaid image rendering endpoint (optional).
- `HTTP_PROXY` and `HTTPS_PROXY`: proxy configuration for supporting services.

## Security and privacy

The application sanitizes Markdown HTML and restricts local filesystem browsing. Remote URLs are limited to public HTTPS destinations; use an authenticated gateway before deploying to multiple users. Optional NTLM credentials are held only in the active session. Browser Web Speech API voices may depend on network access. MP4 narration uses **Microsoft Edge TTS**, which transmits document text to an external service. Do not use it for confidential material unless authorized.

## Status and limitations

- PDF, DOCX and PPTX exports cover common document elements but not all rich media or diagrams.
- Mermaid PNG export requires an explicitly configured renderer; embedded Mermaid preview remains incomplete.
- Video export uses Chromium screenshots, MoviePy and FFmpeg. It scrolls proportionally through document sections rather than anchoring each screenshot precisely to headings.
- Large MP4 jobs are synchronous and can consume substantial memory and disk.
- This is a development application, not a security-certified multi-tenant service.

See [video notes](docs/video.md) and [sample document](docs/sample.md).
