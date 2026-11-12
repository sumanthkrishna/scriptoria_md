# Security and deployment notes

Scriptoria is intended for a trusted workstation or a protected internal environment.

- Keep Streamlit behind authentication and TLS; never expose unrestricted local-folder browsing publicly.
- Set `SCRIPTORIA_ALLOWED_PATHS` to the narrowest directories possible.
- Local images are resolved through the same allowed-root checks and limited to 5 MB each.
- Remote documents use HTTPS and reject private DNS/IP destinations, but public DNS rebinding and redirect edge cases still require network-level egress restrictions.
- Uploaded HTML/Markdown is sanitized; avoid treating sanitizer configuration as a complete isolation boundary.
- Never persist NTLM credentials or include them in diagnostic logs.
- Edge TTS sends narration text to an external provider. Mermaid PNG rendering may also send diagram source externally.
- Large documents, exported videos, and external images require resource limits and deployment-specific controls.

## Release gate

Before promoting to production: complete dependency vulnerability scanning, security review, authenticated deployment, browser CSP review, integration tests, export openability checks and load tests.
