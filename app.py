"""Scriptoria enterprise Markdown reader."""
import hashlib
import html as html_lib
from pathlib import Path
import streamlit as st
from utils.file_handler import list_markdown_files,read_markdown,fetch_url,validate_path
from utils.markdown_renderer import render_markdown,headings,plain_text,search_matches
from utils.export_pdf import export_pdf
from utils.export_docx import export_docx
from utils.export_pptx import export_pptx
from utils.mermaid_export import mermaid_png
from utils.export_video import export_video
from utils.document_assets import embed_local_images
from components.tts_player import tts_player

st.set_page_config(page_title="Scriptoria",page_icon="📖",layout="wide",initial_sidebar_state="expanded")
st.markdown(Path("static/styles.css").read_text(),unsafe_allow_html=True)

for key,default in {"content":"","filename":"","recent":[],"source":"Welcome","doc_hash":"","downloads":{}}.items():
    if key not in st.session_state: st.session_state[key]=default

def activate(name,content,source):
    digest=hashlib.sha256(content.encode()).hexdigest()
    if digest!=st.session_state.doc_hash or name!=st.session_state.filename:
        st.session_state.downloads={}
    st.session_state.update(content=content,filename=name,source=source,doc_hash=digest)
    st.session_state.recent=([name]+[x for x in st.session_state.recent if x!=name])[:5]

with st.sidebar:
    st.title("📖 SCRIPTORIA")
    st.caption("Enterprise Markdown Studio")
    source=st.radio("Document source",["Upload","Local folder","HTTPS URL","Sample"],label_visibility="visible")
    if source=="Upload":
        uploaded=st.file_uploader("Drop Markdown or HTML files",type=["md","markdown","html","htm"],accept_multiple_files=True)
        if uploaded:
            selected=st.selectbox("Active document",[f.name for f in uploaded])
            file=next(f for f in uploaded if f.name==selected)
            if st.button("Open uploaded document"):
                activate(file.name,file.getvalue().decode("utf-8-sig"),"Upload")
    elif source=="Local folder":
        root=st.text_input("Allowed folder",value=str(Path.home()))
        if st.button("Browse folder"):
            try: st.session_state.folder_files=[str(p) for p in list_markdown_files(root)]
            except Exception as exc: st.error(str(exc))
        files=st.session_state.get("folder_files",[])
        if files:
            selected=st.selectbox("Markdown files",files)
            if st.button("Open local document"):
                try: activate(Path(selected).name,read_markdown(selected),selected)
                except Exception as exc: st.error(str(exc))
    elif source=="HTTPS URL":
        url=st.text_input("HTTPS document URL")
        with st.expander("Optional NTLM credentials"):
            domain=st.text_input("Domain")
            username=st.text_input("Username")
            password=st.text_input("Password",type="password")
        if st.button("Fetch document"):
            try:
                content,final=fetch_url(url,username,password,domain)
                activate(Path(final.split("?")[0]).name or "Remote document",content,final)
            except Exception as exc: st.error(str(exc))
    else:
        if st.button("Load sample"):
            activate("sample.md",Path("docs/sample.md").read_text(),"Bundled sample")
    st.divider()
    theme=st.selectbox("Theme",["Default","GitHub","Academic","Compact","Dark"])
    search=st.text_input("Find in document",placeholder="Search text")
    st.caption("Recent documents")
    for name in st.session_state.recent: st.write("• "+name)

if not st.session_state.content:
    st.title("Welcome to Scriptoria")
    st.write("Upload a Markdown file, browse an allowed folder, load an HTTPS URL, or open the bundled sample.")
    st.info("Choose **Sample** in the sidebar to explore the reader.")
    st.stop()

content=st.session_state.content
name=st.session_state.filename
rendered=render_markdown(content)
if st.session_state.source not in ('Upload', 'Bundled sample') and Path(st.session_state.source).is_absolute():
    try:
        rendered=embed_local_images(rendered, st.session_state.source)
    except (ValueError, PermissionError, OSError):
        st.warning('Local images could not be resolved safely.')
text=plain_text(rendered)
st.title("📖 "+name)
st.caption(st.session_state.source+"  ·  "+str(len(content.split()))+" words  ·  "+str(len(content))+" characters")
if search:
    st.info(str(search_matches(text,search))+" matches for “"+search+"”")
toc=headings(rendered)
if toc:
    with st.expander("Table of contents",expanded=False):
        for level,title,anchor in toc:
            st.markdown("　"*(level-1)+"• "+title)
tab_read,tab_audio,tab_pdf,tab_word,tab_slides,tab_video=st.tabs(["📄 Read","🔊 Listen","📕 PDF","📝 Word","📊 Slides","🎬 Video"])
with tab_read:
    st.markdown('<article class="reading-canvas theme-'+theme+'">'+rendered+'</article>',unsafe_allow_html=True)
    st.caption("Use the browser Print command to print this document.")
    if "mermaid" in rendered:
        st.info("Mermaid diagram preview requires the bundled Mermaid JavaScript asset; PNG export requires a configured renderer.")
        import re
        diagrams=re.findall(r'<pre class="mermaid">(.*?)</pre>',rendered,re.S)
        for i,diagram in enumerate(diagrams):
            if st.button("Generate Mermaid PNG "+str(i+1)):
                try:
                    data=mermaid_png(html_lib.unescape(diagram))
                    st.download_button("Download diagram "+str(i+1),data,file_name=f"diagram-{i+1}.png",mime="image/png")
                except Exception as exc: st.error(str(exc))
with tab_audio:
    st.caption("Browser Web Speech API: voices and offline support depend on the browser.")
    tts_player(text[:50000])
def export_tab(label,func,extension,mime):
    key=extension
    if st.button("Generate "+label,key="gen_"+key):
        try:
            with st.spinner("Generating "+label+"…"):
                st.session_state.downloads[key]=(st.session_state.doc_hash,func(rendered,Path(name).stem))
            st.success(label+" is ready")
        except Exception as exc: st.error(str(exc))
    cached=st.session_state.downloads.get(key)
    if cached and cached[0]==st.session_state.doc_hash:
        st.download_button("Download "+label,cached[1],file_name=Path(name).stem+"."+extension,mime=mime,key="dl_"+key)
with tab_pdf: export_tab("PDF",export_pdf,"pdf","application/pdf")
with tab_word: export_tab("Word",export_docx,"docx","application/vnd.openxmlformats-officedocument.wordprocessingml.document")
with tab_slides: export_tab("PowerPoint",export_pptx,"pptx","application/vnd.openxmlformats-officedocument.presentationml.presentation")
with tab_video:
    st.caption("Create a 1920×1080 MP4 with section narration and scrolling screenshots.")
    st.warning("Video narration uses external Microsoft Edge TTS. Document text is sent to that service. Do not use for confidential material without authorization.")
    voice=st.selectbox("Narration voice",["en-US-AriaNeural","en-US-GuyNeural","en-GB-SoniaNeural"])
    st.caption("Requires Playwright Chromium and FFmpeg. Video rendering can be slow.")
    if st.button("Generate MP4"):
        try:
            with st.spinner("Rendering narration, screenshots and MP4…"):
                bar=st.progress(0)
                video=export_video(rendered,Path(name).stem,voice=voice,progress=bar.progress)
                st.session_state.downloads["mp4"]=(st.session_state.doc_hash,video)
            st.success("Video generated")
        except Exception as exc:
            st.error("Video generation failed: "+str(exc))
    cached=st.session_state.downloads.get("mp4")
    if cached and cached[0]==st.session_state.doc_hash:
        st.download_button("Download MP4",cached[1],file_name=Path(name).stem+".mp4",mime="video/mp4")
