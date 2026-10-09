"""
Pautas previstas (ordem do Dr. Luiz, 08/10/2026; páginas de área em 09/10/2026).

"As pautas previstas devem ficar somente na página principal das publicações. Nas outras,
pautas das matérias respectivas": em publicacoes.html a visão "Todas" mostra a próxima pauta
de cada matéria e cada filtro (#execucao-penal, #direito-penal...) mostra só as daquela matéria.
Nas páginas de área listadas em PAGINAS_AREA entram só as pautas da própria matéria, entre
<!-- PAUTAS-AREA-INICIO --> e <!-- PAUTAS-AREA-FIM -->, e só as que o Dr. Luiz já escolheu
(campo "situacao_publica"; a lista é dele, nunca do agente).

Fonte única: pautas.json (ao lado). "tema" é texto público em linguagem leiga; "fonte" e
"situacao" são internos e não vão ao site; "situacao_publica" (público, só na página de área)
admite: "julgamento previsto", "em vigor", "aguarda o STF". Pauta cujo "slug" já está publicado
sai sozinha. Marcador ausente numa página de área é erro (nunca silêncio).

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

# páginas de área que recebem as pautas da própria matéria (marcador PAUTAS-AREA)
PAGINAS_AREA = {"execucao-penal": "area-execucao-penal.html"}

SITUACOES_PUBLICAS = ("julgamento previsto", "em vigor", "aguarda o STF")

esc = lambda t: html.escape(t, quote=False)


def pendentes(pub: Path) -> dict:
    """Pautas de cada matéria, sem as já publicadas."""
    dados = json.loads(DADOS.read_text(encoding="utf-8"))
    return {a: [p for p in dados.get(a, []) if not (p.get("slug") and (pub / f"{p['slug']}.html").exists())]
            for a in AREAS}


def bloco(pub: Path) -> str:
    por_area = pendentes(pub)
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


def bloco_area(pub: Path, area: str) -> str:
    """Lista da página de área: só as pautas da matéria que o Dr. Luiz já escolheu."""
    escolhidas = []
    for p in pendentes(pub).get(area, []):
        sp = p.get("situacao_publica")
        if not sp:
            continue
        if sp not in SITUACOES_PUBLICAS:
            raise ValueError(f'pautas.json: situacao_publica "{sp}" fora da lista {SITUACOES_PUBLICAS}')
        escolhidas.append(p)
    if not escolhidas:
        return '<li class="pauta-vazia">Pautas desta matéria em definição.</li>'
    return "\n".join(f'<li><span class="pauta-tema">{esc(p["tema"])}</span>'
                     f'<span class="pauta-situacao">{esc(p["situacao_publica"])}</span></li>' for p in escolhidas)


def atualizar(pub: Path = None) -> list:
    """Reescreve os blocos de pautas. Devolve os arquivos alterados (para o git add do publicador)."""
    import vitrines  # mesmo trocador de marcadores das outras vitrines
    pub = pub or PUB
    mudados = []
    f = pub / "publicacoes.html"
    s = f.read_text(encoding="utf-8")
    novo = vitrines.trocar(s, "PAUTAS", bloco(pub))
    if novo != s:
        f.write_text(novo, encoding="utf-8", newline="\n"); mudados.append(f)
    for area, nome in PAGINAS_AREA.items():
        f = pub / nome
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8")
        if "<!-- PAUTAS-AREA-INICIO" not in s or "<!-- PAUTAS-AREA-FIM -->" not in s:
            raise RuntimeError(f"{nome}: faltam os marcadores PAUTAS-AREA (a seção de pautas sumiu?)")
        novo = vitrines.trocar(s, "PAUTAS-AREA", bloco_area(pub, area))
        if novo != s:
            f.write_text(novo, encoding="utf-8", newline="\n"); mudados.append(f)
    return mudados


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(AQUI))
    for f in atualizar():
        print("atualizado:", f.relative_to(PUB))
