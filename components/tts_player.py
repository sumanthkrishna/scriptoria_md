"""Browser SpeechSynthesis controls. No text is sent to a TTS server."""
import json
import streamlit.components.v1 as components

def tts_player(text):
    safe=json.dumps(text)
    components.html("""<div style="font:14px system-ui;display:flex;gap:6px;flex-wrap:wrap">
    <select id="voices" aria-label="Voice"></select>
    <select id="speed" aria-label="Speed"><option>.5</option><option>.75</option><option selected>1</option><option>1.25</option><option>1.5</option><option>2</option></select>
    <button onclick="play()">Play</button><button onclick="speechSynthesis.pause()">Pause</button>
    <button onclick="speechSynthesis.resume()">Resume</button>
    <button onclick="speechSynthesis.cancel()">Stop</button></div>
    <script>const content = """+safe+""";
    const voices=document.getElementById('voices');
    function load(){const old=voices.value;voices.innerHTML='';
    speechSynthesis.getVoices().forEach((v,i)=>{let o=document.createElement('option');o.value=i;o.textContent=v.name+' ('+v.lang+')';voices.appendChild(o)});
    if(old)voices.value=old}
    load();speechSynthesis.onvoiceschanged=load;
    function play(){speechSynthesis.cancel();let u=new SpeechSynthesisUtterance(content);
    u.rate=Number(document.getElementById('speed').value);
    u.voice=speechSynthesis.getVoices()[Number(voices.value)]||null;speechSynthesis.speak(u)}
    </script>""",height=70)
