"""Publicador do site Baldissera Advogados.

Recebe UMA publicação em JSON (o formato está em FORMATO.md, ao lado) e:
  1. gera a página publicacao-<slug>.html no padrão visual do site
     (o mesmo da publicação de referência "cadeia de custódia");
  2. encaixa o cartão no topo da lista em publicacoes.html (marcador NOVAS-PUBLICACOES);
  3. acrescenta a página ao sitemap.xml;
  4. (opcional) registra no git e envia ao GitHub, o que põe o site no ar.

O conteúdo vindo do JSON é tratado como DADO: todo texto é escapado; só **negrito**
e *itálico* viram marcação. Nenhum HTML do JSON chega cru à página.

Uso:
  python publicar.py gerar   pub.json          -> só grava os arquivos (prévia local)
  python publicar.py publicar pub.json --push  -> grava, registra no git e envia (vai ao ar)
  python publicar.py verificar pub.json        -> só confere o JSON e diz o que falta
"""
import argparse, datetime as dt, html, json, re, subprocess, sys, unicodedata
from pathlib import Path
from urllib.parse import quote

AQUI = Path(__file__).resolve().parent
SITE = AQUI.parents[1]                       # .../site_baldissera
PUB = SITE / "public"
REPO = SITE.parents[1]
BASE = "https://www.baldisseraadvogados.com.br"
MARCADOR = "<!-- NOVAS-PUBLICACOES"

MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
         "Setembro", "Outubro", "Novembro", "Dezembro"]

# Dados dos autores copiados da página advogados.html (fonte única: se mudar lá, mude aqui)
AUTORES = {
    "luiz": {"nome": "Luiz Henrique Baldissera", "iniciais": "L.H.B.",
             "titulo": "Advogado criminalista · OAB/PR 55.717 · OAB/SC 78.938-A",
             "oab_card": "OAB/PR 55.717 · OAB/SC 78.938-A",
             "bio": "Defesa criminal em ações penais de alta complexidade, habeas corpus e recursos perante STJ e STF, execução penal e sistema penitenciário federal.",
             "foto": "assets/images/luiz-henrique-baldissera.jpg", "perfil": "perfil-luiz.html"},
    "charys": {"nome": "Charys Baldissera", "iniciais": "C.B.",
               "titulo": "Advogada · OAB/PR 69.897", "oab_card": "OAB/PR 69.897",
               "bio": "Direito de Família, Direito das Sucessões e Direito Imobiliário, com ênfase em soluções patrimoniais e planejamento sucessório. Autora no portal Migalhas.",
               "foto": "assets/images/charys-baldissera.jpg", "perfil": "perfil-charys.html"},
    "karla": {"nome": "Karla da Costa Sampaio", "iniciais": "K.C.S.",
              "titulo": "Advogada criminalista · OAB/RS 66.523", "oab_card": "OAB/RS 66.523",
              "bio": "Mais de duas décadas em Tribunal do Júri, Direito Penal Econômico e Empresarial. Relatora da CDAP/OAB-RS desde 2011. Especialista pela PUCRS.",
              "foto": "assets/images/karla-sampaio.jpg", "perfil": "perfil-karla.html"},
    "anderson": {"nome": "Anderson Spanhol", "iniciais": "A.S.",
                 "titulo": "Advogado · OAB/PR 96.871", "oab_card": "OAB/PR 96.871",
                 "bio": "", "foto": "assets/images/anderson-spanhol.jpg", "perfil": "advogados.html"},
}
TIPOS = {"destaque", "paragrafo", "intertitulo", "caixa", "citacao"}


# ------------------------------------------------------------------ utilidades
def inline(t: str) -> str:
    """Escapa o texto e converte só **negrito** e *itálico*."""
    t = html.escape(t.strip(), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def plano(t: str) -> str:
    return re.sub(r"\*+", "", t or "").strip()


def attr(t: str) -> str:
    return html.escape(plano(t), quote=True)


def slugify(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)[:70].rstrip("-")


def verificar(p: dict) -> list:
    erros = []
    for campo in ("titulo", "subtitulo", "resumo", "area", "autor", "corpo"):
        if not p.get(campo):
            erros.append(f"falta o campo '{campo}'")
    if p.get("autor") and p["autor"] not in AUTORES:
        erros.append(f"autor desconhecido: {p['autor']} (use luiz, charys, karla ou anderson)")
    for i, b in enumerate(p.get("corpo") or []):
        if b.get("tipo") not in TIPOS:
            erros.append(f"bloco {i + 1}: tipo inválido '{b.get('tipo')}'")
        elif not (b.get("texto") or "").strip():
            erros.append(f"bloco {i + 1}: sem texto")
    txt = json.dumps(p, ensure_ascii=False)
    if "{{" in txt:
        erros.append("sobrou marcador {{...}} no texto")
    if re.search(r"<\s*(script|iframe|style)", txt, re.I):
        erros.append("o texto contém código de página (script, iframe ou style); por segurança nada foi publicado")
    return erros


def preparar(p: dict) -> dict:
    p = dict(p)
    p["data"] = p.get("data") or dt.date.today().isoformat()
    d = dt.date.fromisoformat(p["data"])
    p["_mes_ano"] = f"{MESES[d.month - 1]} de {d.year}"
    p["_mes_card"] = f"{MESES[d.month - 1]} · {d.year}"
    base = p.get("slug") or slugify(p.get("titulo_curto") or p["titulo"])
    base = re.sub(r"^publicacao-", "", base)
    slug = "publicacao-" + base
    n = 2
    while (PUB / f"{slug}.html").exists() and not p.get("sobrescrever"):
        slug = f"publicacao-{base}-{n}"; n += 1
    p["_slug"] = slug
    palavras = sum(len(plano(b.get("texto", "")).split()) + len(plano(b.get("titulo", "")).split()) for b in p["corpo"])
    p["_leitura"] = max(1, round(palavras / 250))
    p["_autor"] = AUTORES[p["autor"]]
    return p


# ------------------------------------------------------------------ página da publicação
def pagina(p: dict) -> str:
    idx = (PUB / "index.html").read_text(encoding="utf-8")
    contato = idx[idx.index('<div class="contact-bar">'):idx.index('<header class="b-header">')]
    cabecalho = idx[idx.index('<header class="b-header">'):idx.index("</header>") + 9]
    cabecalho = cabecalho.replace('<a href="index.html" class="active">', '<a href="index.html">').replace(
        '<a href="publicacoes.html">', '<a href="publicacoes.html" class="active">')
    rodape = idx[idx.index('<footer class="b-footer">'):idx.index("</body>")]
    a = p["_autor"]
    url = f"{BASE}/{p['_slug']}"
    titulo_curto = plano(p.get("titulo_curto") or p["titulo"])

    corpo = []
    for b in p["corpo"]:
        t = b["tipo"]
        if t == "destaque":
            corpo.append(f'<p style="font-family:var(--serif);font-size:24px;line-height:1.55;color:var(--navy);margin:0 0 32px;font-style:italic;border-left:2px solid var(--gold);padding-left:24px;">{inline(b["texto"])}</p>')
        elif t == "paragrafo":
            corpo.append(f'<p style="margin:0 0 22px;">{inline(b["texto"])}</p>')
        elif t == "intertitulo":
            corpo.append(f'<h2 style="font-family:var(--serif);font-weight:500;font-size:30px;color:var(--navy);margin:50px 0 22px;letter-spacing:.005em;line-height:1.3;">{inline(b["texto"])}</h2>')
        elif t == "caixa":
            rot = f'<p style="font-family:var(--serif);font-style:italic;font-weight:500;color:var(--gold);font-size:18px;margin:0 0 6px;letter-spacing:.04em;">{inline(b["rotulo"])}</p>\n' if b.get("rotulo") else ""
            tit = f'<h3 style="font-family:var(--serif);font-weight:500;font-size:24px;color:var(--navy);margin:0 0 14px;letter-spacing:.005em;line-height:1.25;">{inline(b["titulo"])}</h3>\n' if b.get("titulo") else ""
            corpo.append(f'<div style="background:var(--ivory);border-left:3px solid var(--gold);padding:30px 32px;margin:30px 0 22px;">\n{rot}{tit}<p style="font-size:14px;line-height:1.7;color:var(--text-muted);margin:0;">{inline(b["texto"])}</p>\n</div>')
        elif t == "citacao":
            fonte = f'<span style="display:block;margin-top:10px;font-style:normal;font-family:var(--sans);font-size:12px;letter-spacing:.04em;color:var(--text-muted);">{inline(b["fonte"])}</span>' if b.get("fonte") else ""
            corpo.append(f'<blockquote style="margin:30px 0;padding:22px 26px;background:var(--ivory);border-left:2px solid var(--navy);font-style:italic;font-size:15px;line-height:1.75;color:var(--text-soft);">{inline(b["texto"])}{fonte}</blockquote>')
    corpo.append(f'<p style="font-family:var(--serif);font-style:italic;color:var(--gold);font-size:15px;margin:50px 0 0;letter-spacing:.04em;text-align:right;">— {a["iniciais"]}</p>')

    refs = ""
    if p.get("referencias"):
        itens = "\n".join(
            f'<div style="background:var(--ivory-bg);border:0.5px solid var(--border-medium);border-radius:6px;padding:18px 22px;">\n'
            f'<p style="font-family:var(--serif);font-weight:500;font-size:16px;color:var(--navy);margin:0 0 6px;letter-spacing:.005em;">{inline(r.get("nome", ""))}</p>\n'
            f'<p style="font-size:13px;line-height:1.65;color:var(--text-muted);margin:0;">{inline(r.get("descricao", ""))}</p>\n</div>'
            for r in p["referencias"])
        refs = f"""
<!-- REFERÊNCIAS -->
<section style="padding:60px 40px;background:var(--ivory);border-top:0.5px solid var(--border-soft);border-bottom:0.5px solid var(--border-soft);">
<div style="max-width:680px;margin:0 auto;">
<p style="font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);font-weight:500;margin-bottom:16px;">referências</p>
<h2 style="font-family:var(--serif);font-weight:500;font-size:26px;color:var(--navy);margin:0 0 26px;letter-spacing:.01em;">Normas e julgados citados.</h2>
<div style="display:grid;grid-template-columns:1fr;gap:14px;">
{itens}
</div>
</div>
</section>
"""
    bio = f'<p style="font-size:13px;line-height:1.7;color:var(--text-muted);margin:0 0 12px;">{html.escape(a["bio"])}</p>\n' if a["bio"] else ""
    wa_txt = f"{plano(p['titulo'])}\n\n{plano(p['resumo'])}\n\nAnálise completa:\n{url}\n\n— Baldissera Advogados\nWhatsApp do escritório: https://wa.me/5545991029806"
    desc = attr(p["resumo"])[:300]

    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{attr(titulo_curto)} · Baldissera Advogados</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Baldissera Advogados">
<meta property="og:title" content="{attr(titulo_curto)} · Baldissera Advogados">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/images/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:author" content="{attr(a['nome'])}">
<meta property="article:published_time" content="{p['data']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(titulo_curto)} · Baldissera Advogados">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/images/og-default.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&display=swap">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="stylesheet" href="assets/css/style.css">
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>

{contato}{cabecalho}

<div class="breadcrumb"><a href="publicacoes.html">Publicações</a><span class="sep">/</span><span class="current">{inline(titulo_curto)}</span></div>

<!-- HERO DA PUBLICAÇÃO -->
<section style="padding:60px 40px 40px;background:var(--ivory-bg);">
<div style="max-width:760px;margin:0 auto;">
<p style="font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);font-weight:500;margin-bottom:18px;">PUBLICAÇÃO · {html.escape(p['area'])} · {p['_mes_ano']}</p>
<h1 style="font-family:var(--serif);font-weight:500;font-size:48px;line-height:1.15;letter-spacing:.005em;color:var(--navy);margin:0 0 22px;">{inline(p['titulo'])}</h1>
<p style="font-family:var(--serif);font-style:italic;font-size:21px;color:var(--gold-soft);line-height:1.5;margin:0 0 30px;letter-spacing:.005em;">{inline(p['subtitulo'])}</p>
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;font-size:12px;color:var(--text-muted);padding:18px 0;border-top:0.5px solid var(--border-medium);border-bottom:0.5px solid var(--border-medium);">
<span style="color:var(--gold);font-family:var(--serif);font-style:italic;font-size:14px;">por</span>
<span style="font-family:var(--serif);font-weight:500;font-size:15px;color:var(--navy);">{html.escape(a['nome'])}</span>
<span style="color:var(--gold-light);">·</span>
<span style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;">{html.escape(a['titulo'])}</span>
<span style="color:var(--gold-light);">·</span>
<span style="font-size:11px;letter-spacing:.04em;color:var(--text-light);">leitura: {p['_leitura']} min</span>
</div>
</div>
</section>

<!-- CORPO DO ARTIGO -->
<section style="padding:50px 40px 40px;background:var(--ivory-bg);">
<div style="max-width:680px;margin:0 auto;font-size:16px;line-height:1.85;color:var(--text-soft);">

{chr(10).join(corpo)}

</div>
</section>
{refs}
<!-- BLOCO AUTOR -->
<section style="padding:70px 40px;background:var(--ivory-bg);">
<div style="max-width:680px;margin:0 auto;background:var(--ivory);border:0.5px solid var(--gold-light);border-radius:8px;padding:34px 36px;display:grid;grid-template-columns:90px 1fr;gap:28px;align-items:start;">
<div style="padding:6px;background:var(--ivory-bg);border:0.5px solid var(--gold-light);">
<img src="{a['foto']}" alt="{html.escape(a['nome'])}" style="width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center top;display:block;">
</div>
<div>
<p style="font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);font-weight:500;margin:0 0 6px;">SOBRE {'A AUTORA' if p['autor'] in ('charys', 'karla') else 'O AUTOR'}</p>
<h3 style="font-family:var(--serif);font-weight:500;font-size:22px;color:var(--navy);margin:0 0 8px;letter-spacing:.01em;">{html.escape(a['nome'])}</h3>
<p style="font-family:var(--serif);font-style:italic;font-size:13px;color:var(--gold);margin:0 0 12px;">{html.escape(a['titulo'])}</p>
{bio}<a href="{a['perfil']}" style="font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);text-decoration:none;font-weight:500;">Ver perfil →</a>
</div>
</div>
</section>

<!-- NAVEGAÇÃO -->
<section style="padding:50px 40px 70px;background:var(--ivory);border-top:0.5px solid var(--border-soft);">
<div style="max-width:800px;margin:0 auto;text-align:center;">
<a href="publicacoes.html" style="display:inline-block;background:var(--ivory-bg);border:0.5px solid var(--border-medium);border-radius:8px;padding:24px 40px;text-decoration:none;">
<p style="font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:0 0 6px;">ver todas →</p>
<h4 style="font-family:var(--serif);font-weight:500;font-size:18px;color:var(--navy);margin:0;letter-spacing:.005em;">Publicações</h4>
</a>
</div>
</section>

<aside class="share-wa" style="max-width:760px;margin:48px auto 32px;padding:32px 24px 28px;border-top:0.5px solid var(--border-medium,#d8d3c5);border-bottom:0.5px solid var(--border-medium,#d8d3c5);text-align:center;">
<p style="font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold,#b08a3e);margin:0 0 16px;font-weight:500;">Achou útil? Encaminhe a colegas e clientes</p>
<a href="https://wa.me/?text={quote(wa_txt, safe='')}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;background:#25D366;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:32px;font-family:-apple-system,'Segoe UI',sans-serif;font-size:14px;font-weight:500;letter-spacing:.03em;line-height:1;box-shadow:0 2px 6px rgba(37,211,102,0.18);">Compartilhar no WhatsApp</a>
<p style="font-size:12px;color:var(--text-muted,#7a7468);margin:16px 0 0;font-style:italic;font-family:var(--serif,'Cormorant Garamond',Georgia,serif);line-height:1.45;">A mensagem inclui o resumo, o link para a análise completa e o contato direto do escritório pelo WhatsApp.</p>
</aside>
{rodape}</body>
</html>
"""


# ------------------------------------------------------------------ cartão e sitemap
def cartao(p: dict) -> str:
    a = p["_autor"]
    return f"""<a href="{p['_slug']}.html" style="background:var(--ivory);border:0.5px solid var(--gold-light);border-radius:8px;padding:36px 38px;display:block;text-decoration:none;transition:border-color 0.2s;">
<div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;">
<span style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-light);">{html.escape(p['area'])}</span>
<span style="color:var(--gold-light);font-family:var(--serif);">·</span>
<span style="font-size:11px;letter-spacing:.06em;color:var(--text-light);font-style:italic;font-family:var(--serif);">{p['_mes_card']}</span>
</div>
<h3 style="font-family:var(--serif);font-weight:500;font-size:30px;color:var(--navy);margin:0 0 14px;letter-spacing:.005em;line-height:1.25;">{inline(p['titulo'])}</h3>
<p style="font-family:var(--serif);font-style:italic;font-size:17px;color:var(--gold-soft);margin:0 0 20px;line-height:1.55;letter-spacing:.005em;">{inline(p['subtitulo'])}</p>
<p style="font-size:13.5px;line-height:1.75;color:var(--text-muted);margin:0 0 24px;">{inline(p['resumo'])}</p>
<div style="display:flex;align-items:center;justify-content:space-between;padding-top:18px;border-top:0.5px solid var(--border-medium);">
<div style="display:flex;align-items:center;gap:10px;">
<span style="font-family:var(--serif);font-style:italic;color:var(--gold);font-size:13px;">por</span>
<span style="font-family:var(--serif);font-weight:500;font-size:14px;color:var(--navy);">{html.escape(a['nome'])}</span>
<span style="font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-light);">· {html.escape(a['oab_card'])}</span>
</div>
<span style="font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-weight:500;">Ler →</span>
</div>
</a>
"""


def encaixar(p: dict):
    lista = PUB / "publicacoes.html"
    s = lista.read_text(encoding="utf-8")
    if f'href="{p["_slug"]}.html"' in s:
        return
    i = s.index(MARCADOR)
    i = s.index("\n", i) + 1
    lista.write_text(s[:i] + cartao(p) + s[i:], encoding="utf-8", newline="\n")
    sm = PUB / "sitemap.xml"
    t = sm.read_text(encoding="utf-8")
    loc = f"{BASE}/{p['_slug']}"
    if f"<loc>{loc}</loc>" not in t:
        t = t.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{p['data']}</lastmod>\n"
                                   f"    <changefreq>yearly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>")
        sm.write_text(t, encoding="utf-8", newline="\n")


def git(*args):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"git {' '.join(args)} falhou: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", choices=["verificar", "gerar", "publicar"])
    ap.add_argument("json")
    ap.add_argument("--push", action="store_true", help="envia ao GitHub (põe no ar)")
    ap.add_argument("--ramo", default="main")
    a = ap.parse_args()
    p = json.loads(Path(a.json).read_text(encoding="utf-8"))
    erros = verificar(p)
    if erros:
        print("NÃO PUBLICADO — corrigir:\n- " + "\n- ".join(erros)); sys.exit(2)
    if a.acao == "verificar":
        print("OK — pronto para publicar"); return
    if a.acao == "publicar":
        if git("status", "--porcelain", "--untracked-files=no"):
            raise SystemExit("a cópia do site tem alterações não registradas; nada foi feito")
        git("checkout", a.ramo)
        if a.push:
            git("pull", "--ff-only", "origin", a.ramo)
    p = preparar(p)
    (PUB / f"{p['_slug']}.html").write_text(pagina(p), encoding="utf-8", newline="\n")
    encaixar(p)
    url = f"{BASE}/{p['_slug']}"
    if a.acao == "publicar":
        git("add", "--", str(PUB / f"{p['_slug']}.html"), str(PUB / "publicacoes.html"), str(PUB / "sitemap.xml"))
        git("commit", "-m", f"Publicação: {plano(p.get('titulo_curto') or p['titulo'])} ({p['_autor']['nome']})")
        if a.push:
            git("push", "origin", a.ramo)
            print(json.dumps({"ok": True, "no_ar": True, "url": url, "arquivo": p["_slug"] + ".html"}, ensure_ascii=False))
            return
    print(json.dumps({"ok": True, "no_ar": False, "url": url, "arquivo": p["_slug"] + ".html"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
