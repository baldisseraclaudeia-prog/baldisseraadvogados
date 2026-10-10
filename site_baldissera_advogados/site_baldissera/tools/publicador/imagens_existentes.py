"""Aplica o padrão visual das publicações às páginas que já estão no site (27/09/2026).

REGRA do Dr. Luiz (27/09/2026): capa quadrada com a logo AO LADO do título (estilo blog) e os
Instagram @luizhbaldissera e @baldisseraadvocacia em toda publicação.

Para cada public/publicacao-*.html:
  1. se houver ilustração em PAINEL-PUBLICACAO\\IMAGENS\\<slug>.png:
       - regenera as 3 capas com a ilustração de fundo (capa.py; rodapé com os Instagram);
       - converte a capa quadrada em public/assets/images/publicacoes/<slug>-lateral.jpg;
       - monta a grade "texto | capa" no topo da página, nos dois moldes:
           molde do publicador: dentro do hero (<!-- HERO DA PUBLICAÇÃO -->);
           molde antigo "post-wrap": envolve post-meta + título + subtítulo;
       - remove a figura larga 16:9 da versão anterior e o JPG dela, se existirem;
  2. em todas, acrescenta a linha "Siga no Instagram" no bloco de compartilhar.
Não mexe no texto de nenhuma publicação. Pode rodar de novo sem duplicar (idempotente).

⚠ Rodar pelo PowerShell (o Edge das capas não grava PNG quando chamado pelo Bash em sandbox).

Uso:  python imagens_existentes.py [--so-conferir] [--slug publicacao-x] [--sem-capas]
"""
import argparse, html, json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import publicar as P
import capa
import capas_existentes as CE

CAPAS = P.PUB / "assets" / "images" / "capas"
FIG_ANTIGA = re.compile(r'\n?\s*<figure class="pub-fig">.*?</figure>', re.S)


def alt_do_briefing(slug: str) -> str:
    b = P.IMAGENS_DIR / f"{slug}.briefing.md"
    if b.exists():
        t = b.read_text(encoding="utf-8")
        m = re.search(r"Alt sugerido[^\n]*\n+\s*`([^`]+)`", t) or re.search(r"Alt sugerido[^\n]*\n+\s*>?\s*\"?([^\n\"]{10,200})", t)
        if m:
            return m.group(1).strip()
    return P.ALT_PADRAO


def figura(slug: str, alt: str) -> str:
    return (f'<figure class="pub-fig lateral"><img src="assets/images/publicacoes/{slug}-lateral.jpg" '
            f'alt="{html.escape("Capa da publicação: " + alt, quote=True)}" width="800" height="800" '
            f'fetchpriority="high" decoding="async"></figure>')


def grade(s: str, fig: str) -> "tuple[str, str]":
    """Monta 'texto | capa' no topo da página. Devolve (html, molde)."""
    s = FIG_ANTIGA.sub("", s)
    if 'class="pub-hero-grid"' in s:
        return s, "já tinha"
    # molde "liturgia" (publicar.py: montar_publicacao): a figura entra no fim de <header class="cabeca-pub">
    if '<header class="cabeca-pub sem-figura">' in s:
        i = s.index('<header class="cabeca-pub sem-figura">')
        j = s.index("\n</header>", i)
        img = re.search(r'<img [^>]+>', fig).group(0)
        s = (s[:i] + '<header class="cabeca-pub">' + s[i + len('<header class="cabeca-pub sem-figura">'):j]
             + f"\n  <figure>{img}</figure>" + s[j:])
        return s, "liturgia"
    if '<header class="cabeca-pub">' in s:
        return s, "já tinha"
    # molde antigo: post-meta + h1.post-title + p.post-deck
    m = re.search(r'(\n[ \t]*)(<div class="post-meta">.*?<p class="post-deck">.*?</p>)', s, re.S)
    if m:
        ind = m.group(1)
        bloco = (f'{ind}<div class="pub-hero-grid">{ind}<div class="pub-hero-texto">{ind}'
                 + m.group(2) + f'{ind}</div>{ind}{fig}{ind}</div>')
        return s[:m.start()] + bloco + s[m.end():], "post-wrap"
    # molde do publicador
    i = s.find("<!-- HERO DA PUBLICAÇÃO -->")
    if i >= 0:
        a = s.find('<div style="max-width:760px;margin:0 auto;">', i)
        j = s.find("leitura:", i)
        k = s.find("</div>\n</div>\n</section>", j)
        if 0 < a < j < k:
            k += len("</div>")
            s = (s[:a] + '<div class="pub-hero-grid" style="max-width:1060px;margin:0 auto;">\n<div class="pub-hero-texto">'
                 + s[a + len('<div style="max-width:760px;margin:0 auto;">'):k] + "\n</div>\n" + fig + s[k:])
            return s, "publicador"
    return s, "SEM ÂNCORA"


def instagram(s: str) -> "tuple[str, bool]":
    if 'class="pub-insta"' in s:
        return s, False
    m = re.search(r'(<aside class="share-wa".*?)(\n?</aside>)', s, re.S)
    if not m:
        return s, False
    return s[:m.end(1)] + "\n" + P.instagram_html() + s[m.end(1):], True


def cartoes_com_capa(conferir: bool) -> int:
    """Na lista publicacoes.html, põe a miniatura da capa em cada cartão cuja capa lateral existe."""
    arq = P.PUB / "publicacoes.html"
    s = arq.read_text(encoding="utf-8")
    n = 0

    def troca(m):
        nonlocal n
        slug, card = m.group(1), m.group(0)
        if "com-capa" in card or "pub-card-capa" in card or not (P.IMAGENS_SITE / f"{slug}-lateral.jpg").exists():
            return card
        abre = card.index(">") + 1
        if "<h3" in card and '<span class="pub-meta">' in card:
            # cartão do molde "liturgia" (publicar.py: cartao): a miniatura vem antes da matéria, sem invólucro
            n += 1
            return (card[:abre] + f'\n<img class="pub-card-capa" src="assets/images/publicacoes/{slug}-lateral.jpg" '
                    'alt="" width="800" height="800" loading="lazy" decoding="async">' + card[abre:])
        tit = re.search(r"<h3[^>]*>(.*?)</h3>", card, re.S)
        titulo = re.sub(r"<[^>]+>", "", tit.group(1)).strip() if tit else slug
        fecha = card.rindex("</a>")
        n += 1
        return (card[:abre].replace('class="pub-card"', 'class="pub-card com-capa"', 1) + '\n<div class="pub-card-texto">'
                + card[abre:fecha] + "</div>\n" + P.capa_do_cartao(slug, html.unescape(titulo)) + "\n" + card[fecha:])

    novo = re.sub(r'<a href="(publicacao-[a-z0-9-]+)\.html" class="pub-card[^"]*"[^>]*>.*?</a>', troca, s, flags=re.S)
    if n and not conferir:
        arq.write_text(novo, encoding="utf-8", newline="\n")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-conferir", action="store_true")
    ap.add_argument("--slug")
    ap.add_argument("--sem-capas", action="store_true", help="não regenera as capas (só HTML)")
    a = ap.parse_args()
    for f in sorted(P.PUB.glob("publicacao-*.html")):
        slug = f.stem
        if a.slug and slug != a.slug:
            continue
        s = f.read_text(encoding="utf-8")
        fonte = P.localizar_imagem(f"{slug}.png")
        molde, capas = "sem ilustração", []
        if fonte:
            alt = alt_do_briefing(slug)
            s, molde = grade(s, figura(slug, alt))
            if not a.so_conferir:
                if not a.sem_capas:
                    p = P.preparar(CE.dados(f))
                    p["_imagem_fonte"] = fonte
                    capas = capa.gerar(p, ["og", "quadrado", "vertical"], CAPAS)
                P.lateral_da_capa(CAPAS / f"{slug}-quadrado.png", P.IMAGENS_SITE / f"{slug}-lateral.jpg")
                velho = P.IMAGENS_SITE / f"{slug}.jpg"      # figura larga da versão anterior
                if velho.exists():
                    velho.unlink()
        s, insta = instagram(s)
        if not a.so_conferir:
            f.write_text(s, encoding="utf-8", newline="\n")
        print(json.dumps({"pagina": f.name, "ilustracao": fonte.name if fonte else None, "grade": molde,
                          "instagram": insta, "capas": len(capas)}, ensure_ascii=False))
    print(json.dumps({"lista": "publicacoes.html", "cartoes_com_capa": cartoes_com_capa(a.so_conferir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
