"""Generate narrated 1080p scrolling-document videos.

Requires Chromium (Playwright), FFmpeg, edge-tts and MoviePy 1.x.
Edge TTS sends section text to Microsoft's speech service.
"""
import asyncio
from html import escape
import os
import tempfile
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from playwright.sync_api import sync_playwright

WIDTH, HEIGHT = 1920, 1080

def sections_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    result, current = [], None
    for node in soup.find_all(["h1", "h2", "h3", "p", "li", "pre", "table"]):
        if node.find_parent(["li", "table", "pre"]) and node.name in ("p", "li"):
            continue
        if node.name in ("h1", "h2", "h3"):
            current = {"title": node.get_text(" ", strip=True), "text": ""}
            result.append(current)
        else:
            if current is None:
                current = {"title": "Overview", "text": ""}
                result.append(current)
            current["text"] += node.get_text(" ", strip=True) + ". "
    return [s for s in result if s["title"] or s["text"]]

async def _narrate(items, directory, voice):
    import edge_tts
    for i, item in enumerate(items):
        speech = (item["title"] + ". " + item["text"]).strip()[:4500]
        if not speech:
            speech = "Section " + str(i+1)
        await edge_tts.Communicate(speech, voice).save(str(directory / f"audio_{i}.mp3"))

def export_video(html, title="Scriptoria", voice="en-US-AriaNeural", fps=12, progress=None):
    """Return MP4 bytes; each section scrolls during its own audio narration."""
    items = sections_from_html(html)
    if not items:
        raise ValueError("Document contains no narratable content")
    if len(items) > 40:
        raise ValueError("Video export supports up to 40 sections")
    if len(html.encode("utf-8")) > 1_000_000:
        raise ValueError("Document too large for video export")
    with tempfile.TemporaryDirectory(prefix="scriptoria-video-") as temp:
        folder = Path(temp)
        asyncio.run(_narrate(items, folder, voice))
        clips = []
        audios = []
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
                try:
                    page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1)
                    css = """body{margin:0;background:#f4f8fc;color:#19324a;font:32px/1.55 Arial,sans-serif}
                    article{padding:75px 120px;max-width:1500px;margin:auto;background:white}
                    h1,h2,h3{color:#1765a2}pre{white-space:pre-wrap;font-size:23px;background:#edf2f7;padding:22px}
                    table{border-collapse:collapse}td,th{border:1px solid #aaa;padding:12px}
                    img{max-width:100%}"""
                    page.set_content(f'<html><head><style>{css}</style></head><body><article><h1>{escape(title)}</h1>{html}</article></body></html>',
                                     wait_until="load", timeout=30000)
                    total_height = page.evaluate("document.documentElement.scrollHeight")
                    max_scroll = max(0, total_height - HEIGHT)
                    for i, item in enumerate(items):
                        audio = AudioFileClip(str(folder / f"audio_{i}.mp3"))
                        audios.append(audio)
                        duration = max(audio.duration, 0.2)
                        # Scroll progressively through the complete document.
                        start = max_scroll * i / len(items)
                        end = max_scroll * (i+1) / len(items)
                        count = max(1, int(duration * fps))
                        frames = []
                        for frame in range(count):
                            offset = start + (end-start) * frame / max(count-1, 1)
                            page.evaluate("(y) => window.scrollTo(0, y)", offset)
                            target = folder / f"frame_{i}_{frame}.png"
                            page.screenshot(path=str(target), animations="disabled")
                            frames.append(str(target))
                        from moviepy.editor import ImageSequenceClip
                        clip = ImageSequenceClip(frames, fps=fps).set_duration(duration).set_audio(audio)
                        clips.append(clip)
                        if progress:
                            progress((i+1)/len(items))
                finally:
                    browser.close()
            final = concatenate_videoclips(clips, method="compose")
            try:
                output = folder / "scriptoria.mp4"
                final.write_videofile(str(output), codec="libx264", audio_codec="aac",
                                      fps=fps, preset="ultrafast", threads=2, logger=None)
                return output.read_bytes()
            finally:
                final.close()
        finally:
            for clip in clips:
                clip.close()
            for audio in audios:
                audio.close()
