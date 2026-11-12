"""Isolated Mermaid diagram preview inside Streamlit's component iframe.

For fully offline preview, install a vetted Mermaid bundle at
static/mermaid.min.js. Otherwise an external CDN is used.
"""
import json
from pathlib import Path
import streamlit.components.v1 as components

LOCAL_BUNDLE = Path("static/mermaid.min.js")
CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

def mermaid_viewer(diagrams):
    if not diagrams:
        return
    local = LOCAL_BUNDLE.read_text(encoding="utf-8") if LOCAL_BUNDLE.is_file() else None
    loader = "<script>" + local.replace("</script", "<\\/script") + "</script>" if local else f'<script src="{CDN}"></script>'
    payload = json.dumps(diagrams).replace("<", "\\u003c").replace(">", "\\u003e")
    page = """<!doctype html><html><head><meta charset="utf-8">
    <style>body{font:15px system-ui;margin:0;color:#19324a}
    .diagram{background:#fff;border:1px solid #d6e0e8;border-radius:10px;margin:12px 0;padding:16px;overflow:auto}
    .error{color:#a12c2c;white-space:pre-wrap}</style></head><body>
    <div id="diagrams"></div>""" + loader + """
    <script>
    const diagrams = """ + payload + """;
    (async function(){
      const root=document.getElementById('diagrams');
      if(!window.mermaid){root.textContent='Mermaid JavaScript unavailable. Check network or install local bundle.';return;}
      mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'default'});
      for(let i=0;i<diagrams.length;i++){
        const wrap=document.createElement('div');wrap.className='diagram';root.appendChild(wrap);
        try{
          const rendered=await mermaid.render('scriptoria_diagram_'+i,diagrams[i]);
          wrap.innerHTML=rendered.svg;
        }catch(error){
          const el=document.createElement('pre');el.className='error';
          el.textContent='Diagram '+(i+1)+' could not render: '+error.message;wrap.appendChild(el);
        }
      }
    })();
    </script></body></html>"""
    components.html(page, height=min(850,max(240,300*len(diagrams))), scrolling=True)
