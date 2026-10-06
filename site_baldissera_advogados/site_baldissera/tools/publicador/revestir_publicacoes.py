"""
Reveste as publicações já no ar com o visual "liturgia" (06/10/2026), sem tocar no texto.

Havia dois moldes: o do publicador (tudo em style="", desde 25/09/2026) e o antigo "post-wrap"
(com <style> próprio). Este script lê cada página publicada, separa o <head> técnico (preservado
como está: título, descrição, og, ficha de artigo), o cabeçalho da publicação, o corpo e as
referências, troca a aparência embutida por classes do molde novo e monta a página com
publicar.montar_publicacao(), a mesma função que gera as publicações novas.

Conferência embutida: o texto visível do corpo (e das referências) antes e depois tem de ser
idêntico, palavra por palavra; se não for, a página NÃO é gravada e o script mostra a diferença.

Uso:
  python revestir_publicacoes.py            # todas as publicacao-*.html
  python revestir_publicacoes.py <arquivo>  # só uma
  python revestir_publicacoes.py --ver      # só confere, não grava
"""
import datetime as dt
import difflib
import html
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import publicar as P  # noqa: E402

PUB = P.PUB


# ------------------------------------------------------------------ texto visível (para a conferência)
def texto(h: str) -> list:
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"<br\s*/?>", " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return t.split()


def diferenca(antes: list, depois: list) -> str:
    linhas = []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(a=antes, b=depois, autojunk=False).get_opcodes():
        if op != "equal":
            linhas.append(f"  {op}: «{' '.join(antes[a1:a2])}» -> «{' '.join(depois[b1:b2])}»")
    return "\n".join(linhas)


# ------------------------------------------------------------------ limpeza do corpo
def limpar_molde_a(c: str) -> str:
    """Molde do publicador: estilos embutidos -> classes."""
    def caixa(m):
        miolo = m.group(2)
        miolo = re.sub(r'<p style="[^"]*font-style:italic;font-weight:500;color:var\(--gold\)[^"]*">', '<p class="caixa-rotulo">', miolo, count=1)
        return '<div class="caixa">' + miolo + "</div>"
    c = re.sub(r'(?s)<div style="[^"]*border-left:3px solid var\(--gold\)[^"]*">(\s*)(.*?)</div>',
               lambda m: caixa(m), c)
    c = re.sub(r'<p style="[^"]*font-size:24px[^"]*">', '<p class="destaque">', c)
    c = re.sub(r'<p style="[^"]*font-style:italic;color:var\(--gold\);font-size:15px[^"]*">', '<p class="assinatura">', c)
    c = re.sub(r'<p style="[^"]*margin:0;font-style:italic;">', '<p class="italico">', c)
    c = re.sub(r'<span style="display:block[^"]*">', '<span class="fonte">', c)
    c = re.sub(r'\s+style="[^"]*"', "", c)
    return c.strip()


def limpar_molde_b(c: str) -> str:
    """Molde antigo "post-wrap": classes próprias -> classes do molde novo."""
    c = re.sub(r'<hr class="post-divider"\s*/?>', "", c)
    c = c.replace('<h2 class="post-section-label">', "<h2>")
    c = c.replace('class="post-signature"', 'class="assinatura"')
    c = c.replace('class="post-pull"', 'class="destaque"')
    c = c.replace('class="post-cite"', 'class="citacao"')
    c = c.replace('class="post-identification"', 'class="identificacao"')
    c = c.replace(' class="post-requisitos"', "")
    c = re.sub(r'\s+style="[^"]*"', "", c)
    return c.strip()


# ------------------------------------------------------------------ cartões da lista (área, data, STF/STJ)
def cartoes() -> dict:
    s = (PUB / "publicacoes.html").read_text(encoding="utf-8")
    d = {}
    for m in re.finditer(r'<a href="([^"]+)\.html" class="pub-card[^"]*"([^>]*)>', s):
        at = m.group(2)
        d[m.group(1)] = {k: re.search(fr'data-{k}="([^"]*)"', at).group(1) for k in ("area", "data", "superior")}
    return d


def interno(s: str, abre: str, fecha: str) -> str:
    i = s.index(abre)
    i = s.index(">", i) + 1
    return s[i:s.index(fecha, i)]


def revestir(arq: Path, meta: dict) -> tuple:
    s = arq.read_text(encoding="utf-8")
    slug = arq.stem
    head = s[:s.index("</head>")]
    b_molde = 'class="post-wrap"' in s

    titulo = re.sub(r"\s+", " ", re.sub(r'\s+style="[^"]*"', "", interno(s, "<h1", "</h1>"))).strip()
    if b_molde:
        subtitulo = interno(s, '<p class="post-deck"', "</p>")
        corpo_antigo = s[s.index('<hr class="post-divider"'):s.index('<aside class="share-wa"')]
        corpo = limpar_molde_b(corpo_antigo)
        refs_antigas, refs = "", []
    else:
        h1_fim = s.index("</h1>")
        subtitulo = interno(s[h1_fim:], "<p", "</p>")
        a = s.index("<!-- CORPO DO ARTIGO -->")
        a = s.index(">", s.index("<div", a)) + 1                  # dentro do <div> do corpo
        fim_corpo = s.index("<!-- REFERÊNCIAS -->") if "<!-- REFERÊNCIAS -->" in s else s.index("<!-- BLOCO AUTOR -->")
        b = s.rindex("</div>", a, s.rindex("</section>", a, fim_corpo))
        corpo_antigo = s[a:b]
        corpo = limpar_molde_a(corpo_antigo)
        refs, refs_antigas = [], ""
        if "<!-- REFERÊNCIAS -->" in s:
            r0 = s.index("<!-- REFERÊNCIAS -->"); r1 = s.index("<!-- BLOCO AUTOR -->")
            bloco = s[r0:r1]
            grade = bloco[bloco.index("<div", bloco.index("</h2>")):]
            for n, d in re.findall(r'<div[^>]*>\s*<p[^>]*>(.*?)</p>\s*<p[^>]*>(.*?)</p>\s*</div>', grade, re.S):
                refs.append((n.strip(), d.strip()))
            refs_antigas = " ".join(f"{n} {d}" for n, d in refs)
    subtitulo = re.sub(r"\s+", " ", re.sub(r'\s+style="[^"]*"', "", subtitulo)).strip()

    # autor: pelo link do perfil no bloco do autor ou pelo nome na assinatura
    autor = "luiz"
    for chave, a_ in P.AUTORES.items():
        if f'href="{a_["perfil"]}"' in s[s.find("BLOCO AUTOR"):] or a_["nome"] in corpo[-400:]:
            if chave != "anderson" or a_["nome"] in s:
                autor = chave
                break
    lei = re.search(r"leitura:\s*(\d+)\s*min", s)
    leitura = int(lei.group(1)) if lei else max(1, round(len(texto(corpo)) / 250))
    fig = re.search(r'<figure class="pub-fig lateral"><img src="([^"]+)" alt="([^"]*)"', s)
    data = dt.date.fromisoformat(meta["data"])
    wa = re.search(r'<aside class="share-wa"[^>]*>.*?<a href="([^"]+)"', s, re.S)
    # biografia do bloco "Sobre o autor" da página antiga (há publicações com texto próprio)
    bio = None
    if "<!-- BLOCO AUTOR -->" in s:
        blk = s[s.index("<!-- BLOCO AUTOR -->"):]
        m = re.search(r"</h3>\s*<p[^>]*>.*?</p>\s*<p[^>]*>(.*?)</p>", blk, re.S)
        if m:
            bio = m.group(1).strip()

    novo = P.montar_publicacao(
        head, slug=slug, titulo_html=titulo, subtitulo_html=subtitulo, area=P.AREAS[meta["area"]], area_slug=meta["area"],
        mes_ano=f"{P.MESES[data.month - 1]} de {data.year}", autor=autor, leitura=leitura,
        imagem_web=fig.group(1) if fig else None, imagem_alt=html.unescape(fig.group(2)) if fig else "",
        corpo=corpo, referencias=refs, bio=bio, wa_href=html.unescape(wa.group(1)) if wa else P.link_whatsapp({"_slug": slug, "titulo": titulo, "resumo": subtitulo}))

    # conferência: corpo + referências, antes e depois, palavra por palavra
    antes = texto(corpo_antigo) + texto(refs_antigas)
    novo_corpo = novo[novo.index('<div class="corpo">'):novo.index('<section class="autor-bloco"')]
    depois = texto(novo_corpo.replace("Normas e julgados citados", ""))
    return novo, antes, depois, {"molde": "B" if b_molde else "A", "autor": autor, "leitura": leitura,
                                 "refs": len(refs), "figura": bool(fig)}


def main():
    so_ver = "--ver" in sys.argv
    alvos = [Path(a) for a in sys.argv[1:] if not a.startswith("--")] or sorted(PUB.glob("publicacao-*.html"))
    meta = cartoes()
    falhas = 0
    for arq in alvos:
        arq = arq if arq.is_absolute() else PUB / arq.name
        if 'class="cabeca-pub' in arq.read_text(encoding="utf-8"):
            print(f"= {arq.name}: já está no visual novo"); continue
        novo, antes, depois, info = revestir(arq, meta[arq.stem])
        if antes != depois:
            falhas += 1
            print(f"✗ {arq.name}: o texto mudaria — NÃO gravado\n{diferenca(antes, depois)}")
            continue
        if not so_ver:
            arq.write_text(novo, encoding="utf-8", newline="\n")
        print(f"✓ {arq.name}: {len(antes)} palavras idênticas · {info}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
