import sys, pathlib
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:'Poppins',sans-serif;color:#fff;
 background:#0A1A33;position:relative}
.wrap{position:absolute;inset:0;padding:80px 84px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:18px;font-weight:700;font-size:30px;letter-spacing:.5px}
.dot{width:20px;height:20px;border-radius:50%;background:#FFC21A}
.tag{display:inline-block;background:#FFC21A;color:#0A1A33;font-weight:700;font-size:30px;
 padding:10px 24px;border-radius:999px;align-self:flex-start;margin-top:64px}
h1{font-family:'Inter Display','Inter',sans-serif;font-weight:900;font-size:138px;line-height:1.04;
 letter-spacing:-4px;margin-top:40px;text-transform:uppercase}
h1 em{font-style:normal;color:#FFC21A}
.sub{font-size:40px;line-height:1.3;margin-top:36px;max-width:820px;color:#DCE6F5}
.chips{display:flex;flex-wrap:wrap;gap:16px;margin-top:44px}
.chip{border:3px solid #6FA8E8;color:#fff;font-size:30px;font-weight:500;padding:10px 26px;border-radius:999px}
.foot{margin-top:auto}
.cta{display:flex;justify-content:space-between;align-items:flex-end;border-top:3px solid #24406A;padding-top:30px}
.cta b{display:block;font-size:36px;white-space:nowrap;font-weight:700}
.cta span{font-size:28px;color:#A9BDD9}
.hours{text-align:right;white-space:nowrap}
.hours b{color:#FFC21A}
.legal{font-size:20px;white-space:nowrap;color:#7D93B5;margin-top:22px;letter-spacing:.3px}
.ice{position:absolute;border-radius:28px;background:linear-gradient(135deg,rgba(150,200,255,.22),rgba(150,200,255,.04));
 border:2px solid rgba(180,215,255,.25);transform:rotate(18deg)}
"""

ICE = """
<div class="ice" style="width:260px;height:260px;right:-60px;top:120px"></div>
<div class="ice" style="width:170px;height:170px;right:150px;top:330px;transform:rotate(-12deg)"></div>
<div class="ice" style="width:120px;height:120px;right:30px;top:470px;transform:rotate(30deg)"></div>
"""

FOOT = """
<div class="foot">
 <div class="cta">
  <div><b>Peça pelo iFood ou WhatsApp</b><span>(61) 98341-7930 · QNP 36, Ceilândia Sul</span></div>
  <div class="hours"><span>Aberto todos os dias</span><b style="display:block;font-size:42px">até 00h</b></div>
 </div>
 <div class="legal">Beba com moderação. Venda de bebidas alcoólicas proibida para menores de 18 anos.</div>
</div>
"""

POSTS = {
 "post1-sextou": f"""{ICE}<div class="wrap">
  <div class="brand"><span class="dot"></span>DISTRIBUIDORA ALTERNATIVA</div>
  <div class="tag">Sexta-feira</div>
  <h1>Sextou<br><em>trincando</em></h1>
  <div class="sub">Cerveja estupidamente gelada, gelo e carvão pra começar o fim de semana do jeito certo.</div>
  <div class="chips"><span class="chip">Cervejas</span><span class="chip">Gelo</span><span class="chip">Carvão</span><span class="chip">Refri</span></div>
  {FOOT}</div>""",
 "post2-mercearia": f"""<div class="wrap">
  <div class="brand"><span class="dot"></span>DISTRIBUIDORA ALTERNATIVA</div>
  <div class="tag">Sábado</div>
  <h1>Faltou<br>alguma<br><em>coisa?</em></h1>
  <div class="sub">Bateu a fome? Resolve aqui, pertinho de casa, até meia-noite.</div>
  <div class="chips"><span class="chip">Chocolate</span><span class="chip">Miojo</span><span class="chip">Creme de leite</span><span class="chip">Biscoito</span><span class="chip">Sucos</span><span class="chip">Snacks</span></div>
  {FOOT}</div>""",
 "post3-domingo": f"""{ICE}<div class="wrap">
  <div class="brand"><span class="dot"></span>DISTRIBUIDORA ALTERNATIVA</div>
  <div class="tag">Domingo</div>
  <h1>Domingo<br>é dia de<br><em>churrasco</em></h1>
  <div class="sub">Carvão, gelo, cerveja e refri num pedido só. Abrimos às 9h.</div>
  <div class="chips"><span class="chip">Carvão</span><span class="chip">Gelo</span><span class="chip">Cerveja</span><span class="chip">Refri</span></div>
  {FOOT}</div>""",
}

STORY_CSS = BASE_CSS.replace("height:1350px", "height:1920px")
STORY = f"""{ICE}<div class="wrap" style="padding:220px 84px 300px">
  <div class="brand"><span class="dot"></span>DISTRIBUIDORA ALTERNATIVA</div>
  <div class="tag">Hoje</div>
  <h1 style="font-size:170px">Aberto<br>até<br><em>meia-<br>noite</em></h1>
  <div class="sub" style="font-size:46px">Bebidas geladas, snacks e tabacaria. Peça pelo iFood ou chama no WhatsApp.</div>
  <div class="foot">
   <div class="cta"><div><b>(61) 98341-7930</b><span>QNP 36, Ceilândia Sul</span></div></div>
   <div class="legal">Beba com moderação. Proibida a venda para menores de 18 anos.</div>
  </div></div>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, body in POSTS.items():
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.set_content(f"<html><head><style>{BASE_CSS}</style></head><body>{body}</body></html>")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=88)
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(f"<html><head><style>{STORY_CSS}</style></head><body>{STORY}</body></html>")
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT / "story-aberto.jpg"), type="jpeg", quality=88)
    b.close()
print("done")
