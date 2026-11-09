"""Finaliza um vídeo vertical no padrão @dbalternativa (logo + título + rodapé).

Uso: python3 _template/reel.py <video_entrada.mp4> <saida.mp4> <spec.json>
spec: {"titulo": "...*destaque*...", "sub": "...", "tamanho": 120, "alcool": true, "entra": 1.0}
Área de baixo (300px) e lateral direita ficam livres para a interface do Reels.
"""
import sys, json, pathlib, re, subprocess, tempfile
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "_template/render.py").read_text(encoding="utf-8")
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)
ns = {}; exec(re.search(r"(def data_uri.*?\n\n)", src, re.S).group(1), {"ROOT": ROOT, "base64": __import__("base64")}, ns)
exec(re.search(r"(def titulo_html.*?\n\n)", src, re.S).group(1), {"html": __import__("html"), "re": re}, ns)
LOGO = ns["data_uri"]("_assets/logo.png"); titulo_html = ns["titulo_html"]
import html as H

entrada, saida, spec = sys.argv[1], sys.argv[2], json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))
legal = "Beba com moderação. Venda de bebidas alcoólicas proibida para menores de 18 anos." if spec.get("alcool") else ""
BASE = f"<style>{CSS} body{{background:transparent!important}} .wrap{{padding:0 84px}}</style>"
logo_html = f"""<html><head>{BASE}</head><body style="--h:1920px">
<div style="position:absolute;left:0;top:0;width:1080px;height:420px;background:linear-gradient(180deg,rgba(13,13,13,.55),rgba(13,13,13,0))"></div>
<img class="logo" src="{LOGO}" style="position:absolute;left:84px;top:150px;width:230px"></body></html>"""
texto_html = f"""<html><head>{BASE}</head><body style="--h:1920px">
<div style="position:absolute;left:0;top:880px;width:1080px;height:1040px;background:linear-gradient(180deg,rgba(13,13,13,0),rgba(13,13,13,.88) 30%,rgba(13,13,13,.95))"></div>
<div style="position:absolute;left:84px;right:170px;bottom:300px">
<h1 style="--fs:{spec.get('tamanho',120)}px;margin-top:0">{titulo_html(spec['titulo'])}</h1>
<div class="sub" style="font-size:36px;margin-top:20px">{H.escape(spec.get('sub',''))}</div>
<div class="cta" style="margin-top:30px;padding-top:20px;display:block">
<b style="font-size:34px">Peça pelo iFood ou WhatsApp · (61) 98341-7930</b>
<span style="display:block;font-size:26px">QNP 36 CJ J LT 02 · Ceilândia Sul · Todos os dias até 00h</span></div>
{f'<div class="legal" style="font-size:19px;white-space:normal">{legal}</div>' if legal else ''}
</div></body></html>"""

tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    for nome, doc in (("logo", logo_html), ("texto", texto_html)):
        pg.set_content(doc); pg.wait_for_timeout(400)
        pg.screenshot(path=str(tmp/f"{nome}.png"), omit_background=True)
    b.close()
t = spec.get("entra", 1.0)
fc = (f"[0:v]scale=1080:1920:flags=lanczos,setsar=1[v];[1:v]format=rgba[l];"
      f"[2:v]format=rgba,fade=in:st={t}:d=0.5:alpha=1[t];[v][l]overlay=0:0[a];[a][t]overlay=0:0:shortest=1,format=yuv420p[out]")
subprocess.run(["ffmpeg","-v","error","-y","-i",entrada,"-loop","1","-i",str(tmp/"logo.png"),"-loop","1","-i",str(tmp/"texto.png"),
  "-filter_complex",fc,"-map","[out]","-map","0:a?","-c:v","libx264","-preset","slow","-crf","20","-r","30",
  "-c:a","aac","-b:a","128k","-movflags","+faststart","-shortest",saida], check=True)
print("ok", saida)
