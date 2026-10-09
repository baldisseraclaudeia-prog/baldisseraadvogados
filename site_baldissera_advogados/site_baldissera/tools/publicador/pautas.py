"""
Pautas previstas da página de Publicações (ordem do Dr. Luiz, 08/10/2026).

"As pautas previstas devem ficar somente na página principal das publicações. Nas outras,
pautas das matérias respectivas": a visão "Todas" mostra a próxima pauta de cada matéria;
cada filtro (#execucao-penal, #direito-penal...) mostra só as pautas daquela matéria.

Fonte única: pautas.json (ao lado). Este script reescreve public/publicacoes.html entre
<!-- PAUTAS-INICIO --> e <!-- PAUTAS-FIM -->. Pauta cujo "slug" já está publicado sai sozinha.
O filtro da própria página (função aplica) mostra a lista certa; sem JavaScript, só a geral.

Rodar à mão também serve:  python pautas.py
"""
import html
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PUB = AQUI.parents[1] / "public"
DADOS = AQUI / "pautas.json"

# mesma ordem e nomes das pílulas de publicacoes.html
AREAS = {"direito-penal": "Direito Penal", "tribunais-superiores": "Tribunais Superiores",
         "execucao-penal": "Execução Penal", "imobiliario": "Imobiliário", "civil": "Civil",
         "familia-e-sucessoes": "Família e Sucessões", "ambiental": "Ambiental"}


def pendentes(pub: Path) -> dict:
    """Pautas de cada matéria, sem as já publicadas."""
    dados = json.loads(DADOS.read_text(encoding="utf-8"))
    return {a: [p for p in dados.get(a, []) if not (p.get("slug") and (pub / f"{p['slug']}.html").exists())]
            for a in AREAS}


def bloco(pub: Path) -> str:
    por_area = pendentes(pub)
    esc = lambda t: html.escape(t, quote=False)
    geral = [f'<li><span class="pauta-tema">{esc(ps[0]["tema"])}</span><span class="pauta-area">{AREAS[a]}</span></li>'
             for a, ps in por_area.items() if ps]
    partes = ['<ol class="pautas sem-mes" data-pautas="todas">', *geral, "</ol>"]
    for a, ps in por_area.items():
        if not ps:
            continue
        partes.append(f'<ol class="pautas so-tema" data-pautas="{a}" data-nome="{AREAS[a]}" hidden>')
        partes += [f'<li><span class="pauta-tema">{esc(p["tema"])}</span></li>' for p in ps]
        partes.append("</ol>")
    return "\n".join(partes)


def atualizar(pub: Path = None) -> list:
    """Reescreve o bloco de pautas. Devolve os arquivos alterados (para o git add do publicador)."""
    import vitrines  # mesmo trocador de marcadores das outras vitrines
    pub = pub or PUB
    f = pub / "publicacoes.html"
    s = f.read_text(encoding="utf-8")
    novo = vitrines.trocar(s, "PAUTAS", bloco(pub))
    if novo != s:
        f.write_text(novo, encoding="utf-8", newline="\n")
        return [f]
    return []


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(AQUI))
    for f in atualizar():
        print("atualizado:", f.relative_to(PUB))
