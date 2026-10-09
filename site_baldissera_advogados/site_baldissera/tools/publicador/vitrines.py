"""
Vitrines automáticas do site (visual "liturgia", 06/10/2026).

A cada publicação nova, o publicador chama atualizar_tudo(), que lê os cartões de
public/publicacoes.html e reescreve, entre marcadores <!-- X-INICIO --> e <!-- X-FIM -->:

  RECENTES          home: manchete (a mais nova, grande) + as três seguintes ao lado
  SABIA             home: "Você sabia?" — a frase de efeito prático (o resumo do cartão, texto já
                    publicado) das publicações mais recentes, uma por matéria antes de repetir,
                    cada uma com o link da sua publicação. Nenhuma frase é escrita aqui.
  PUBLICACOES-AREA  páginas de área: as publicações daquela matéria
  PAUTAS            publicacoes.html: pautas previstas por matéria (pautas.py + pautas.json)
  (arquivo)         public/assets/busca.json — índice da busca "O que você procura?"

Rodar à mão também serve:  python vitrines.py
"""
import html
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PUB = AQUI.parents[1] / "public"
MAX_SABIA = 5

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]
NOME_AREA = {"direito-penal": "Direito Penal", "tribunais-superiores": "Tribunais Superiores",
             "execucao-penal": "Execução Penal", "imobiliario": "Imobiliário", "civil": "Civil",
             "familia-e-sucessoes": "Família e Sucessões", "ambiental": "Ambiental"}
# página de área -> como escolher as publicações dela
PAGINAS_AREA = {
    "area-direito-penal.html": lambda c: c["area"] == "direito-penal",
    "area-recursos-tribunais-superiores.html": lambda c: c["superior"] or c["area"] == "tribunais-superiores",
    "area-execucao-penal.html": lambda c: c["area"] == "execucao-penal",
    "area-direito-imobiliario.html": lambda c: c["area"] == "imobiliario",
    "area-direito-civil.html": lambda c: c["area"] == "civil",
    "area-familia-sucessoes.html": lambda c: c["area"] == "familia-e-sucessoes",
    "area-direito-ambiental.html": lambda c: c["area"] == "ambiental",
    "area-leiloes.html": lambda c: "leil" in (c["titulo"] + " " + c["resumo"]).lower(),
}

# páginas do portal de execução penal que também listam as publicações da matéria (ordem do Dr. Luiz, 09/10/2026);
# fora de PAGINAS_AREA para não entrarem na busca como "Área de atuação"
PAGINAS_PORTAL = {
    "execucao-penal-em-linguagem-simples.html": lambda c: c["area"] == "execucao-penal",
    "execucao-penal-revisao-por-fases.html": lambda c: c["area"] == "execucao-penal",
}

CARTAO = re.compile(r'(?s)<a href="([^"]+\.html)" class="pub-card[^"]*"([^>]*)>(.*?)</a>')


def _attr(at: str, k: str) -> str:
    m = re.search(fr'data-{k}="([^"]*)"', at)
    return m.group(1) if m else ""


def _texto(h: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


def cartoes(pub: Path = None) -> list:
    """Cartões da lista, do mais novo para o mais antigo (no mesmo dia vale a ordem da lista)."""
    s = ((pub or PUB) / "publicacoes.html").read_text(encoding="utf-8")
    itens = []
    for ordem, m in enumerate(CARTAO.finditer(s)):
        href, at, miolo = m.groups()
        tit = re.search(r"(?s)<h3[^>]*>(.*?)</h3>", miolo)
        res = re.search(r'(?s)<p class="pub-resumo">(.*?)</p>', miolo)
        img = re.search(r'<img class="pub-card-capa" src="([^"]+)"', miolo)
        if not tit:
            continue
        data = _attr(at, "data")
        a, mth = data[:4], int(data[5:7]) if len(data) >= 7 else 1
        itens.append({"href": href, "data": data, "ordem": ordem, "area": _attr(at, "area"),
                      "superior": _attr(at, "superior") == "1", "titulo_html": tit.group(1).strip(),
                      "titulo": _texto(tit.group(1)), "resumo_html": res.group(1).strip() if res else "",
                      "resumo": _texto(res.group(1)) if res else "", "capa": img.group(1) if img else None,
                      "mes": f"{MESES[mth - 1]} de {a}"})
    itens.sort(key=lambda i: (i["data"], -i["ordem"]), reverse=True)
    return itens


def trocar(s: str, marca: str, miolo: str) -> str:
    ini, fim = f"<!-- {marca}-INICIO", f"<!-- {marca}-FIM -->"
    if ini not in s or fim not in s:
        return s
    a = s.index("\n", s.index(ini)) + 1
    return s[:a] + (miolo + "\n" if miolo else "") + s[s.index(fim):]


def meta(c: dict) -> str:
    return f'{NOME_AREA.get(c["area"], "")}, {c["mes"]}'


def _img(c: dict, lazy=True) -> str:
    if not c["capa"]:
        return ""
    return (f'<img src="{c["capa"]}" alt="" width="800" height="800"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


# ------------------------------------------------------------------ home: manchete
def capa_horizontal(c: dict, pub: Path) -> str:
    """Manchete: a capa 1200x630 (feita para formato horizontal); sem ela, a quadrada."""
    slug = c["href"][:-5]
    og = f"assets/images/capas/{slug}-og.png"
    if (pub / og).exists():
        return f'<img src="{og}" alt="" width="1200" height="630" decoding="async">'
    return _img(c, lazy=False)


def bloco_recentes(cs: list, pub: Path = None) -> str:
    if not cs:
        return ""
    p, resto = cs[0], cs[1:4]
    lista = "\n".join(
        f'<li><a href="{c["href"]}">{_img(c)}<span><span class="pub-data">{meta(c)}</span>'
        f'<span class="lista-titulo">{c["titulo_html"]}</span></span></a></li>' for c in resto)
    return (f'<div class="manchete">\n<article class="manchete-principal">\n<a href="{p["href"]}">\n{capa_horizontal(p, pub or PUB)}\n'
            f'<span class="pub-data">{meta(p)}</span>\n<span class="manchete-titulo">{p["titulo_html"]}</span>\n</a>\n'
            f'<p>{p["resumo_html"]}</p>\n</article>\n<ul class="manchete-lista">\n{lista}\n</ul>\n</div>')


# ------------------------------------------------------------------ home: "Você sabia?"
def frase(resumo: str) -> str:
    """Primeira frase do resumo (ou as duas primeiras, se a primeira for curta demais)."""
    # não corta depois de abreviatura ("Rel. Min. Fulano", "art. 5º")
    partes = re.split(r"(?<!\bMin\.)(?<!\bRel\.)(?<!\bDes\.)(?<!\bart\.)(?<!\bArt\.)(?<!\bn\.)(?<!\bDr\.)(?<!\bDra\.)(?<!\bProf\.)(?<!\bProfa\.)(?<!\bSr\.)(?<!\bSra\.)(?<!\bInc\.)(?<!\binc\.)(?<!\bfls\.)(?<!\bfl\.)(?<!\bp\.)(?<!\bv\.)(?<!\bAg\.)(?<!\barts\.)(?<!\bArts\.)(?<!\bEx\.)(?<!\bExmo\.)(?<!\bExma\.)(?<!\bMin\.)(?<!\bnº\.)(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÀÇ])", resumo.strip())
    # frase que só identifica o julgado ("Comentário ao REsp ...") não informa: usa a seguinte
    if len(partes) > 1 and re.match(r"Coment[áa]rio (ao|à|a)\b", partes[0]):
        partes = partes[1:]
    f = partes[0]
    if len(f) < 90 and len(partes) > 1:
        f += " " + partes[1]
    return f


def bloco_sabia(cs: list) -> str:
    escolhidos, areas = [], set()
    for c in cs:                                  # primeiro, uma por matéria
        if c["resumo"] and c["area"] not in areas:
            escolhidos.append(c); areas.add(c["area"])
        if len(escolhidos) == MAX_SABIA:
            break
    for c in cs:                                  # completa com as mais recentes
        if len(escolhidos) == MAX_SABIA:
            break
        if c["resumo"] and c not in escolhidos:
            escolhidos.append(c)
    return "\n".join(
        f'<li>\n<p class="sabia-area">{NOME_AREA.get(c["area"], "")}</p>\n'
        f'<p class="sabia-frase">{html.escape(frase(c["resumo"]))}</p>\n'
        f'<a class="sabia-link" href="{c["href"]}">Ler a publicação</a>\n</li>' for c in escolhidos)


# ------------------------------------------------------------------ páginas de área
def bloco_area(cs: list) -> str:
    if not cs:
        return ('<li class="pub-vazia"><p>Ainda não há publicações nesta matéria. '
                '<a href="publicacoes.html">Ver todas as publicações</a>.</p></li>')
    return "\n".join(
        f'<li><a href="{c["href"]}">{_img(c)}<span class="pub-data">{c["mes"][0].upper() + c["mes"][1:]}</span>'
        f'<span class="pub-titulo">{c["titulo_html"]}</span></a></li>' for c in cs)


# ------------------------------------------------------------------ índice da busca
def indice(cs: list, pub: Path) -> list:
    itens = [{"tipo": "Publicação", "titulo": c["titulo"], "area": NOME_AREA.get(c["area"], ""), "data": c["mes"],
              "resumo": c["resumo"], "url": c["href"]} for c in cs]
    paginas = [("Área de atuação", f) for f in PAGINAS_AREA] + [
        ("Página", "areas-de-atuacao.html"), ("Página", "advogados.html"), ("Advogado", "perfil-luiz.html"),
        ("Advogada", "perfil-charys.html"), ("Advogada", "perfil-karla.html"), ("Página", "contato.html"),
        ("Página", "agendar.html"), ("Página", "sobre.html"),
        ("Página", "execucao-penal-em-linguagem-simples.html"), ("Página", "execucao-penal-revisao-por-fases.html")]
    for tipo, nome in paginas:
        f = pub / nome
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8")
        h1 = re.search(r"(?s)<h1[^>]*>(.*?)</h1>", s)
        desc = re.search(r'<meta name="description" content="([^"]*)"', s)
        if h1:
            itens.append({"tipo": tipo, "titulo": _texto(h1.group(1)).rstrip("."), "area": "", "data": "",
                          "resumo": html.unescape(desc.group(1)) if desc else "", "url": nome})
    return itens


# ------------------------------------------------------------------ tudo
def atualizar_tudo(pub: Path = None) -> list:
    """Reescreve as vitrines. Devolve a lista de arquivos alterados (para o git add do publicador)."""
    pub = pub or PUB
    cs = cartoes(pub)
    mudados = []

    home = pub / "index.html"
    s = home.read_text(encoding="utf-8")
    novo = trocar(trocar(s, "RECENTES", bloco_recentes(cs, pub)), "SABIA", bloco_sabia(cs))
    if novo != s:
        home.write_text(novo, encoding="utf-8", newline="\n"); mudados.append(home)

    for nome, filtro in {**PAGINAS_AREA, **PAGINAS_PORTAL}.items():
        f = pub / nome
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8")
        novo = trocar(s, "PUBLICACOES-AREA", bloco_area([c for c in cs if filtro(c)]))
        if novo != s:
            f.write_text(novo, encoding="utf-8", newline="\n"); mudados.append(f)

    import pautas                     # pautas previstas por matéria (publicacoes.html), 08/10/2026
    mudados += pautas.atualizar(pub)

    busca = pub / "assets" / "busca.json"
    dados = json.dumps(indice(cs, pub), ensure_ascii=False, indent=1) + "\n"
    if not busca.exists() or busca.read_text(encoding="utf-8") != dados:
        busca.write_text(dados, encoding="utf-8", newline="\n"); mudados.append(busca)
    return mudados


if __name__ == "__main__":
    for f in atualizar_tudo():
        print("atualizado:", f.relative_to(PUB))
    sys.exit(0)
