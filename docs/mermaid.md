# Mermaid rendering

Mermaid diagrams are previewed in an isolated Streamlit component iframe using
Mermaid JavaScript with strict Mermaid security mode.

By default the component downloads Mermaid JavaScript from jsDelivr. This
**requires network access** and is not an offline configuration. To enable
offline preview, place an independently reviewed Mermaid 11.x distribution at
`static/mermaid.min.js`. Do not substitute arbitrary untrusted JavaScript.

PNG downloads use the separately configured `MERMAID_INK_URL` endpoint.
The diagram source is sent to that external service. Preview and PNG export
therefore have different network/privacy properties.

Mermaid diagrams are not yet automatically embedded in PDF/DOCX/PPTX exports.
Do not use diagrams containing sensitive information with an external renderer
without appropriate authorization.
