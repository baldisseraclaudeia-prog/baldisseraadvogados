"""Capa de publicação com a marca Baldissera Advogados.

Gera, para cada publicação, uma imagem PNG no padrão da casa em três formatos:
  og       1200x630  — prévia de link (WhatsApp, LinkedIn, Google)
  quadrado 1080x1080 — post de feed
  vertical 1080x1350 — post vertical (Instagram)

Desde 27/09/2026 a capa tem dois modos:
  * COM ILUSTRAÇÃO (p["_imagem_fonte"] aponta para o PNG gerado pelo diretor de arte):
    a ilustração ocupa o fundo; sobre ela, um véu marinho recebe a marca vetorial
    oficial, a área, o título e o rodapé com autor e site.
  * SEM ILUSTRAÇÃO: layout tipográfico anterior (marinho, marca, título, fio dourado).

A marca vem de public/assets/images/marca/baldissera-advogados-escuro.svg (vetor oficial,
versão para fundo escuro); se o arquivo faltar, cai no monograma em CSS.

Uso:
  python capa.py <publicacao.json> [--formatos og,quadrado,vertical] [--saida DIR] [--imagem ARQ.png]
Sem --saida grava em public/assets/images/capas/<slug>-<formato>.png
"""
import argparse, html, json, re, subprocess, sys, tempfile, unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import publicar as P  # reaproveita autores, slug, datas e a localização da ilustração

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FORMATOS = {"og": (1200, 630), "quadrado": (1080, 1080), "vertical": (1080, 1350)}
MARCA_SVG = P.PUB / "assets" / "images" / "marca" / "baldissera-advogados-escuro.svg"

NAVY, GOLD, GOLD_CLARO, IVORY = "#0F172A", "#9B7B3A", "#C9B98A", "#F5F1E8"


def nfc(t: str) -> str:
    """Junta letra e acento num só caractere (evita acento "solto" na fonte do título)."""
    return unicodedata.normalize("NFC", t or "")


def marca_html(largura: int) -> str:
    """Marca oficial em SVG embutido; sem o arquivo, monograma BA em CSS."""
    if MARCA_SVG.exists():
        svg = MARCA_SVG.read_text(encoding="utf-8")
        svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
        return f'<div class="marca" style="width:{largura}px">{svg}</div>'
    return (f'<div class="marca marca-css"><div class="cap"><span class="b">B</span><span class="a">A</span></div>'
            f'<div class="nome"><p>BALDISSERA</p><span>ADVOGADOS</span></div></div>')


def tamanho_titulo(n: int, base: int) -> int:
    return base if n <= 70 else base - 6 if n <= 100 else base - 12 if n <= 130 else base - 18


def html_capa(p: dict, w: int, h: int) -> str:
    a = p["_autor"]
    titulo = html.escape(nfc(P.plano(p["titulo"])))
    area = html.escape(nfc(p["area"]))
    autor = html.escape(a["nome"]); oab = html.escape(a["oab_card"])
    og = w == 1200
    vertical = h > w
    imagem = p.get("_imagem_fonte")
    margem = 36 if og else 48
    respiro = 72 if og else 92

    base_css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
body{{background:{NAVY};color:{IVORY};font-family:-apple-system,'Segoe UI',Roboto,sans-serif;position:relative}}
.moldura{{position:absolute;inset:{margem}px;border:1px solid rgba(201,185,138,.30);z-index:3}}
.conteudo{{position:absolute;inset:{respiro}px;display:flex;flex-direction:column;justify-content:space-between;z-index:4}}
.marca svg{{display:block;width:100%;height:auto}}
.marca-css{{display:flex;align-items:center;gap:18px}}
.cap{{font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-weight:500;font-size:54px;line-height:1;letter-spacing:-.08em;display:flex}}
.cap .b{{color:{GOLD_CLARO};transform:translateX(4px)}} .cap .a{{color:{IVORY};transform:translateX(-6px)}}
.nome{{border-left:1px solid rgba(245,241,232,.3);padding-left:18px}}
.nome p{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:26px;letter-spacing:.12em;line-height:1}}
.nome span{{display:block;font-size:10px;letter-spacing:.55em;margin-top:8px;color:{GOLD_CLARO}}}
.area{{font-size:{14 if og else 15}px;letter-spacing:.32em;text-transform:uppercase;color:{GOLD_CLARO};font-weight:600;margin-bottom:{22 if og else 26}px}}
h1{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;line-height:1.12;letter-spacing:.003em;color:{IVORY}}}
.fio{{width:88px;height:2px;background:{GOLD};margin-top:{28 if og else 34}px}}
.pe{{display:flex;justify-content:space-between;align-items:flex-end;font-size:{16 if og else 17}px;color:#C9C5B8}}
.pe b{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;font-size:{22 if og else 24}px;color:{IVORY};display:block;margin-bottom:4px}}
.site{{font-size:{14 if og else 15}px;letter-spacing:.08em;color:{GOLD_CLARO};text-align:right;line-height:1.55}}
.site .insta{{display:block;color:{IVORY};letter-spacing:.04em;font-size:{14 if og else 16}px}}
"""

    if imagem:
        # ---------- modo com ilustração ----------
        foto = Path(imagem).resolve().as_uri()
        if og:
            # ilustração inteira ao fundo; véu marinho forte à esquerda, onde ficam marca e título
            layout_css = f"""
.foto{{position:absolute;inset:0;background:url("{foto}") center right/cover no-repeat;z-index:1}}
.veu{{position:absolute;inset:0;z-index:2;background:
  linear-gradient(90deg, rgba(15,23,42,.97) 0%, rgba(15,23,42,.94) 34%, rgba(15,23,42,.66) 56%, rgba(15,23,42,.22) 78%, rgba(15,23,42,.08) 100%),
  linear-gradient(0deg, rgba(15,23,42,.88) 0%, rgba(15,23,42,0) 32%)}}
.meio{{flex:1;display:flex;flex-direction:column;justify-content:center;padding:14px 0;max-width:{int(w * 0.60)}px}}
h1{{font-size:{tamanho_titulo(len(titulo), 50)}px}}
"""
        else:
            # ilustração no alto (≈56 %), texto embaixo sobre véu que sobe
            alto = int(h * (0.50 if vertical else 0.54))
            layout_css = f"""
.foto{{position:absolute;left:0;right:0;top:0;height:{alto + 140}px;background:url("{foto}") center/cover no-repeat;z-index:1}}
.veu{{position:absolute;inset:0;z-index:2;background:
  linear-gradient(180deg, rgba(15,23,42,.72) 0%, rgba(15,23,42,.10) 22%, rgba(15,23,42,0) 38%, rgba(15,23,42,.55) {int((alto - 40) / h * 100)}%, rgba(15,23,42,.985) {int((alto + 120) / h * 100)}%, {NAVY} 100%)}}
.meio{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;padding:{alto - respiro - 40}px 0 {32 if vertical else 24}px;min-height:0}}
h1{{font-size:{tamanho_titulo(len(titulo), 60 if vertical else 52)}px;max-width:{w - 2 * respiro}px}}
"""
        camadas = '<div class="foto"></div><div class="veu"></div>'
    else:
        # ---------- modo tipográfico (sem ilustração) ----------
        layout_css = f"""
.meio{{flex:1;display:flex;flex-direction:column;justify-content:center;padding:{'40px 0' if vertical else '10px 0'}}}
h1{{font-size:{tamanho_titulo(len(titulo), 64 if og else 78) + (0 if og else 4)}px;max-width:{w - 200}px}}
"""
        camadas = ""

    # mesma largura em todos os formatos: na prévia de link (og) a marca menor deixava o
    # "ADVOGADOS" fraco (ajuste pedido pelo Dr. Luiz em 27/09/2026)
    largura_marca = 380
    return f"""<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=block" rel="stylesheet">
<style>{base_css}{layout_css}</style></head><body>
{camadas}
<div class="moldura"></div>
<div class="conteudo">
  {marca_html(largura_marca)}
  <div class="meio">
    <p class="area">{area}</p>
    <h1>{titulo}</h1>
    <div class="fio"></div>
  </div>
  <div class="pe"><div><b>{autor}</b>{oab}</div>
    <div class="site"><span class="insta">{html.escape(' · '.join('@' + u for u, _ in P.INSTAGRAM))}</span>baldisseraadvogados.com.br</div></div>
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
            subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                            f"--user-data-dir={Path(tmp) / 'perfil'}", "--virtual-time-budget=8000",
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
    ap.add_argument("--imagem", help="PNG da ilustração (sobrepõe o campo 'imagem' do JSON)")
    a = ap.parse_args()
    p = json.loads(Path(a.json).read_text(encoding="utf-8"))
    if isinstance(p.get("data"), dict) and "pub" in p["data"]:
        p = p["data"]
    if isinstance(p.get("pub"), dict):
        p = p["pub"]
    if a.slug:
        p["slug"], p["sobrescrever"] = a.slug, True
    if a.imagem:
        p["imagem"] = a.imagem
    p = P.preparar(p)
    saida = Path(a.saida) if a.saida else P.PUB / "assets" / "images" / "capas"
    print(json.dumps({"ok": True, "ilustracao": str(p.get("_imagem_fonte") or ""),
                      "capas": gerar(p, a.formatos.split(","), saida)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
