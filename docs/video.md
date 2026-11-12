# Video export

The Video tab produces a 1920×1080 MP4 using Playwright Chromium screenshots,
MoviePy 1.x and Edge TTS narration. Install dependencies from requirements.txt,
then run `python -m playwright install chromium` and install FFmpeg.

**Privacy:** Edge TTS is an external Microsoft service. Section text is sent to
that service to generate narration. Do not export confidential documents unless
your organization's data handling policy permits this.

The video export is CPU, memory and disk intensive. Large documents may take
minutes and use significant temporary disk space. Export is limited to 40 sections
and 1 MB HTML input. Video is generated synchronously and stored in Streamlit
session memory until the document changes.

**Limitations:** Scrolling is proportional to section count rather than precisely
aligned to each heading's screen position. Interactive Mermaid diagrams and
remote image loading may not render in Chromium. This feature is not offline.
