"""Capa de publicação com a marca Baldissera Advogados.

Gera, para cada publicação, uma imagem PNG no padrão da casa (marinho, monograma BA,
título em Cormorant, fio dourado) em três formatos:
  og       1200x630  — prévia de link (WhatsApp, LinkedIn, Google)
  quadrado 1080x1080 — post de feed
  vertical 1080x1350 — post vertical (Instagram)

Uso:
  python capa.py <publicacao.json> [--formatos og,quadrado,vertical] [--saida DIR]
Sem --saida grava em public/assets/images/capas/<slug>-<formato>.png
"""
import argparse, html, json, re, subprocess, sys, tempfile, unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import publicar as P  # reaproveita autores, slug e datas

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FORMATOS = {"og": (1200, 630), "quadrado": (1080, 1080), "vertical": (1080, 1350)}


def nfc(t: str) -> str:
    """Junta letra e acento num só caractere (evita acento "solto" na fonte do título)."""
    return unicodedata.normalize("NFC", t or "")


def html_capa(p: dict, w: int, h: int) -> str:
    a = p["_autor"]
    titulo = html.escape(nfc(P.plano(p["titulo"])))
    # título grande, reduzido conforme o comprimento e o formato
    n = len(titulo)
    base = 64 if w == 1200 else 78
    tam = base if n <= 70 else base - 8 if n <= 100 else base - 16 if n <= 130 else base - 22
    vertical = h > w
    return f"""<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=block" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
body{{background:#0F172A;color:#F5F1E8;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;position:relative}}
.moldura{{position:absolute;inset:{36 if w == 1200 else 48}px;border:1px solid rgba(201,185,138,.28)}}
.conteudo{{position:absolute;inset:{76 if w == 1200 else 96}px;display:flex;flex-direction:column;justify-content:space-between}}
.marca{{display:flex;align-items:center;gap:18px}}
.cap{{font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-weight:500;font-size:54px;line-height:1;letter-spacing:-.08em;display:flex}}
.cap .b{{color:#C9A962;transform:translateX(4px)}} .cap .a{{color:#F5F1E8;transform:translateX(-6px)}}
.nome{{border-left:1px solid rgba(245,241,232,.3);padding-left:18px}}
.nome p{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:26px;letter-spacing:.12em;line-height:1}}
.nome span{{display:block;font-size:10px;letter-spacing:.55em;margin-top:8px;color:#C9B98A}}
.meio{{flex:1;display:flex;flex-direction:column;justify-content:center;padding:{'40px 0' if vertical else '10px 0'}}}
.area{{font-size:15px;letter-spacing:.32em;text-transform:uppercase;color:#C9A962;font-weight:600;margin-bottom:26px}}
h1{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:{tam}px;line-height:1.12;letter-spacing:.003em;max-width:{w - 200}px}}
.fio{{width:88px;height:2px;background:#9B7B3A;margin-top:34px}}
.pe{{display:flex;justify-content:space-between;align-items:flex-end;font-size:17px;color:#C9C5B8}}
.pe b{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;font-size:24px;color:#F5F1E8;display:block;margin-bottom:4px}}
.site{{font-size:15px;letter-spacing:.08em;color:#C9B98A}}
</style></head><body>
<div class="moldura"></div>
<div class="conteudo">
  <div class="marca"><div class="cap"><span class="b">B</span><span class="a">A</span></div>
    <div class="nome"><p>BALDISSERA</p><span>ADVOGADOS</span></div></div>
  <div class="meio">
    <p class="area">{html.escape(nfc(p['area']))}</p>
    <h1>{titulo}</h1>
    <div class="fio"></div>
  </div>
  <div class="pe"><div><b>{html.escape(a['nome'])}</b>{html.escape(a['oab_card'])}</div>
    <div class="site">baldisseraadvogados.com.br</div></div>
</div>
</body></html>"""


def gerar(p: dict, formatos, saida: Path) -> list:
    saida.mkdir(parents=True, exist_ok=True)
    feitos = []
    with tempfile.TemporaryDirectory() as tmp:
        for f in formatos:
            w, h = FORMATOS[f]
            src = Path(tmp) / f"{f}.html"
            src.write_text(html_capa(p, w, h), encoding="utf-8")
            out = saida / f"{p['_slug']}-{f}.png"
            subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            f"--user-data-dir={Path(tmp) / 'perfil'}", "--virtual-time-budget=6000",
                            f"--window-size={w},{h}", f"--screenshot={out}", src.as_uri()],
                           capture_output=True, timeout=120)
            if not out.exists():
                raise SystemExit(f"não consegui gerar a capa {f}")
            feitos.append(str(out))
    return feitos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--formatos", default="og,quadrado,vertical")
    ap.add_argument("--saida")
    ap.add_argument("--slug", help="endereço já publicado (sem .html), para não gerar um novo")
    a = ap.parse_args()
    p = json.loads(Path(a.json).read_text(encoding="utf-8"))
    if isinstance(p.get("data"), dict) and "pub" in p["data"]:
        p = p["data"]
    if isinstance(p.get("pub"), dict):
        p = p["pub"]
    if a.slug:
        p["slug"], p["sobrescrever"] = a.slug, True
    p = P.preparar(p)
    saida = Path(a.saida) if a.saida else P.PUB / "assets" / "images" / "capas"
    print(json.dumps({"ok": True, "capas": gerar(p, a.formatos.split(","), saida)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
