"""
Publicações recentes na página inicial (04/10/2026).

Lê os cartões de public/publicacoes.html, escolhe as 3 mais recentes (data-data)
e reescreve o bloco da home entre os marcadores RECENTES-INICIO e RECENTES-FIM.
O publicar.py chama atualizar() a cada publicação nova; rodar à mão também serve:

    python home_recentes.py
"""
import re
import sys
from pathlib import Path

PUB = Path(__file__).resolve().parents[2] / "public"
INICIO = "<!-- RECENTES-INICIO"
FIM = "<!-- RECENTES-FIM -->"
QUANTAS = 3

CARTAO = re.compile(r'<a href="([^"]+\.html)" class="pub-card[^"]*"[^>]*data-data="(\d{4}-\d{2}-\d{2})"[^>]*>(.*?)</a>', re.S)
SPANS = re.compile(r"<span[^>]*>([^<]*)</span>")
TITULO = re.compile(r"<h3[^>]*>(.*?)</h3>", re.S)
CAPA = re.compile(r'<img class="pub-card-capa" src="([^"]+)"')


def recentes(n: int = QUANTAS) -> list:
    s = (PUB / "publicacoes.html").read_text(encoding="utf-8")
    itens = []
    for ordem, m in enumerate(CARTAO.finditer(s)):
        href, data, miolo = m.groups()
        spans = SPANS.findall(miolo)
        titulo = TITULO.search(miolo)
        capa = CAPA.search(miolo)
        if not titulo or len(spans) < 3:
            continue
        itens.append({"href": href, "data": data, "ordem": ordem, "area": spans[0].strip(),
                      "mes": spans[2].strip().replace(" · ", " de "), "titulo": titulo.group(1).strip(),
                      "capa": capa.group(1) if capa else None})
    # mais recente primeiro; no mesmo dia, vale a ordem da lista (a mais nova fica no topo)
    itens.sort(key=lambda i: (i["data"], -i["ordem"]), reverse=True)
    return itens[:n]


def bloco(itens: list) -> str:
    linhas = []
    for i in itens:
        # sem loading="lazy": no computador as capas aparecem logo na abertura da página
        capa = (f'<img src="{i["capa"]}" alt="" width="800" height="800" decoding="async">'
                if i["capa"] else '<span class="rec-sem-capa" aria-hidden="true"></span>')
        linhas.append(f'<li><a class="rec-item" href="{i["href"]}">{capa}'
                      f'<span class="rec-texto"><span class="rec-meta">{i["area"]} · {i["mes"]}</span>'
                      f'<span class="rec-titulo">{i["titulo"]}</span></span></a></li>')
    return "\n".join(linhas)


def atualizar(pub: Path = PUB) -> bool:
    """Reescreve o bloco da home. Devolve True se o arquivo mudou."""
    global PUB
    PUB = pub
    home = PUB / "index.html"
    s = home.read_text(encoding="utf-8")
    if INICIO not in s or FIM not in s:
        return False
    a = s.index("\n", s.index(INICIO)) + 1
    b = s.index(FIM)
    novo = s[:a] + bloco(recentes()) + "\n" + s[b:]
    if novo == s:
        return False
    home.write_text(novo, encoding="utf-8", newline="\n")
    return True


if __name__ == "__main__":
    mudou = atualizar()
    print("home atualizada" if mudou else "home já estava em dia (ou sem marcadores)")
    sys.exit(0)
