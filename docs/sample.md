# Welcome to Scriptoria

## Enterprise Markdown viewer

Scriptoria supports **bold**, *italic*, tables, tasks, diagrams, and exports.

### Feature matrix

| Capability | Status |
|---|---|
| Markdown rendering | Available |
| PDF, DOCX, PPTX | Available |
| Browser TTS | Available |

- [x] Open documents
- [x] Render Markdown
- [ ] Review exported files

```python
def hello():
    print("Hello from Scriptoria")
```

```mermaid
flowchart LR
    A[Markdown] --> B[Sanitize]
    B --> C[Read]
    C --> D[Export]
```

> Documents are sanitized before display.
