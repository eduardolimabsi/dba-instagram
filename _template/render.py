"""Padrão visual @dbalternativa — gera as artes da semana.

Uso: python3 _template/render.py <pasta_saida> <arquivo_semana.json>

O JSON tem uma lista "pecas"; cada peça tem:
  arquivo  : nome do .jpg
  formato  : "post" (1080x1350) ou "story" (1080x1920)
  modelo   : "chamada" (tipográfico) | "foto" (foto real da loja no topo) | "oferta" (produto + preço)
  tag      : texto da etiqueta amarela (ex.: "Sexta-feira")
  titulo   : linhas do título; use *palavra* para destacar em amarelo; \n quebra linha
  sub      : frase de apoio
  chips    : lista curta de itens (opcional)
  foto     : caminho da foto (modelo "foto"), relativo à raiz do repositório
  preco    : ex. "19,99" (modelo "oferta" — só com oferta REAL enviada pelo Eduardo)
  alcool   : true se a peça fala de bebida alcoólica (adiciona aviso legal)
"""
import sys, json, pathlib, base64, html, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SPEC = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))

def data_uri(rel):
    p = ROOT / rel
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

LOGO = data_uri("_assets/logo.png")

# Cores da marca: preto e amarelo da fachada, vermelho do logo.
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--preto:#0D0D0D;--amarelo:#FFC400;--vermelho:#D8261C;--cinza:#B9B9B9}
body{width:1080px;height:var(--h);overflow:hidden;background:var(--preto);color:#fff;
 font-family:'Poppins',sans-serif;position:relative}
.faixa{position:absolute;right:120px;top:-80px;width:34px;height:520px;background:var(--amarelo);
 transform:rotate(22deg);border-radius:4px}
.faixa.b{right:58px;top:-40px;height:380px;opacity:.35}
.wrap{position:absolute;inset:0;padding:var(--pad);display:flex;flex-direction:column}
.logo{width:250px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.6))}
.tag{display:inline-block;background:var(--amarelo);color:var(--preto);font-weight:700;font-size:30px;
 padding:8px 24px;border-radius:8px;align-self:flex-start;margin-top:34px;text-transform:uppercase;letter-spacing:1px}
h1{font-family:'Inter Display','Inter',sans-serif;font-weight:900;font-size:var(--fs);line-height:1.04;
 letter-spacing:-3px;margin-top:26px;text-transform:uppercase}
h1 em{font-style:normal;color:var(--amarelo)}
.sub{font-size:38px;line-height:1.32;margin-top:28px;color:#E6E6E6;max-width:900px}
.chips{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}
.chip{border:3px solid var(--amarelo);color:#fff;font-size:29px;font-weight:500;padding:8px 24px;border-radius:999px}
.foto{position:absolute;left:0;top:0;width:1080px;height:var(--fh);background-size:cover;background-position:center}
.foto:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,13,13,.15) 35%,var(--preto) 100%)}
.preco{display:flex;align-items:flex-start;gap:8px;margin-top:30px;color:var(--amarelo);font-family:'Inter Display',sans-serif;font-weight:900}
.preco small{font-size:56px;margin-top:22px}.preco b{font-size:190px;line-height:1;letter-spacing:-6px}
.foot{margin-top:auto}
.cta{display:flex;justify-content:space-between;align-items:flex-end;border-top:4px solid var(--amarelo);padding-top:26px}
.cta b{display:block;font-size:36px;font-weight:700;white-space:nowrap}
.cta span{font-size:27px;color:var(--cinza);white-space:nowrap}
.hr{text-align:right;white-space:nowrap}.hr b{color:var(--amarelo);font-size:46px}
.legal{font-size:20px;color:#8E8E8E;margin-top:18px;white-space:nowrap}
"""

def titulo_html(t):
    t = html.escape(t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")

def peca_html(p):
    story = p.get("formato") == "story"
    h = 1920 if story else 1350
    modelo = p.get("modelo", "chamada")
    fs = p.get("tamanho", 150 if story else 132)
    pad = "150px 84px 230px" if story else "70px 84px 64px"
    fh = 1000 if story else 700
    partes = []
    if modelo == "foto":
        partes.append(f'<div class="foto" style="background-image:url({data_uri(p["foto"])})"></div>')
    else:
        partes.append('<div class="faixa"></div><div class="faixa b"></div>')
    corpo = [f'<img class="logo" src="{LOGO}">']
    if modelo == "foto":
        corpo.append(f'<div style="height:{fh-430 if not story else fh-520}px"></div>')
    if p.get("tag"): corpo.append(f'<div class="tag">{html.escape(p["tag"])}</div>')
    corpo.append(f'<h1 style="--fs:{fs}px">{titulo_html(p["titulo"])}</h1>')
    if modelo == "oferta" and p.get("preco"):
        corpo.append(f'<div class="preco"><small>R$</small><b>{html.escape(p["preco"])}</b></div>')
    if p.get("sub"): corpo.append(f'<div class="sub">{html.escape(p["sub"])}</div>')
    if p.get("chips"):
        corpo.append('<div class="chips">' + "".join(f'<span class="chip">{html.escape(c)}</span>' for c in p["chips"]) + "</div>")
    legal = "Beba com moderação. Venda de bebidas alcoólicas proibida para menores de 18 anos." if p.get("alcool") else ""
    if story:
        foot = f"""<div class="foot"><div class="cta"><div><b>(61) 98341-7930</b><span>QNP 36, Ceilândia Sul · iFood e WhatsApp</span></div></div>
        {f'<div class="legal">{legal}</div>' if legal else ''}</div>"""
    else:
        foot = f"""<div class="foot"><div class="cta">
         <div><b>Peça pelo iFood ou WhatsApp</b><span>(61) 98341-7930 · QNP 36, Ceilândia Sul</span></div>
         <div class="hr"><span>Todos os dias</span><b style="display:block">até 00h</b></div></div>
        {f'<div class="legal">{legal}</div>' if legal else ''}</div>"""
    corpo.append(foot)
    body = "".join(partes) + f'<div class="wrap" style="--pad:{pad}">' + "".join(corpo) + "</div>"
    return h, f'<html><head><style>{CSS}</style></head><body style="--h:{h}px;--fh:{fh}px">{body}</body></html>'

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for p in SPEC["pecas"]:
        h, doc = peca_html(p)
        pg = b.new_page(viewport={"width": 1080, "height": h})
        pg.set_content(doc); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / p["arquivo"]), type="jpeg", quality=88)
        pg.close()
    b.close()
print("ok")
