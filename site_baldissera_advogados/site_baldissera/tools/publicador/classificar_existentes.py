"""Organiza a lista de publicações por área (27/09/2026).

Roda UMA vez sobre o que já está no site e pode ser rodado de novo sem estragar (idempotente):
  1. em publicacoes.html, troca as pílulas "tópicos cobertos" por botões que filtram a lista,
     dá a cada cartão `class="pub-card" data-area data-superior data-data`, corrige o rótulo
     de área do cartão, reordena os cartões por data (mais recente no topo) e acrescenta o
     script do filtro;
  2. em cada publicacao-*.html, corrige o rótulo de área para o nome oficial (nos dois moldes
     de página: o do publicador e o antigo "post-wrap").

A classificação (área × julgado STF/STJ × data) foi aprovada pelo Dr. Luiz em 27/09/2026.
Publicações novas já saem classificadas pelo publicador (publicar.py: AREAS, analisa_superior, cartao).

Uso:  python classificar_existentes.py [--so-conferir]
"""
import argparse, html, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import publicar as P

# slug -> (área oficial, analisa julgado STF/STJ?, data da publicação)
CLASSIFICACAO = {
    "publicacao-adpf-347-na-execucao-penal": ("execucao-penal", True, "2026-09-27"),
    "publicacao-cadeia-de-custodia": ("direito-penal", False, "2026-01-15"),
    "publicacao-prova-digital-sem-hash": ("direito-penal", True, "2026-04-25"),
    "publicacao-colacao-doacao-dissimulada-resp-2171573-ms": ("familia-e-sucessoes", True, "2026-05-06"),
    "publicacao-domiciliar-humanitaria-6t-stj": ("direito-penal", True, "2026-05-26"),
    "publicacao-impronuncia-aresp-3065825-pe": ("direito-penal", True, "2026-04-27"),
    "publicacao-re-635659-ed-segundos-cannabis": ("direito-penal", True, "2025-02-01"),
    "publicacao-rif-coaf-re-1537165-sp": ("direito-penal", True, "2026-04-30"),
    "publicacao-tema-931-resp-2090454-sp": ("execucao-penal", True, "2026-05-06"),
}

PILULA = re.compile(r'<span style="padding:8px 18px;background:var\(--ivory-bg\);border:0\.5px solid var\(--gold-light\);font-size:12px;color:var\(--navy\);border-radius:40px;">([^<]+)</span>\n?')
CARTAO = re.compile(r'<a href="(publicacao-[a-z0-9-]+)\.html"[^>]*>.*?</a>\n', re.S)
ROTULO_CARTAO = re.compile(r'(<span style="font-size:11px;letter-spacing:\.1em;text-transform:uppercase;color:var\(--text-light\);">)([^<]*)(</span>)')
GRID = '<div style="display:grid;grid-template-columns:1fr;gap:18px;">'
MARCA_SCRIPT = "<!-- FILTRO-PUBLICACOES -->"

SCRIPT = r"""<!-- FILTRO-PUBLICACOES -->
<script>
(function () {
  var ORDEM = ["direito-penal", "tribunais-superiores", "execucao-penal", "imobiliario", "civil", "familia-e-sucessoes", "ambiental"];
  var NOMES = {"direito-penal": "Direito Penal", "tribunais-superiores": "Técnica recursal", "execucao-penal": "Execução Penal",
               "imobiliario": "Imobiliário", "civil": "Civil", "familia-e-sucessoes": "Família e Sucessões", "ambiental": "Ambiental"};
  var lista = document.getElementById("lista-publicacoes");
  var aviso = document.getElementById("lista-aviso");
  var botoes = document.querySelectorAll(".topico[data-filtro]");
  if (!lista || !botoes.length) return;
  var cards = Array.prototype.slice.call(lista.querySelectorAll("a.pub-card"));
  cards.sort(function (a, b) { return (b.getAttribute("data-data") || "").localeCompare(a.getAttribute("data-data") || ""); });

  function aplica(filtro, gravaHash) {
    Array.prototype.forEach.call(lista.querySelectorAll(".grupo-materia"), function (e) { e.parentNode.removeChild(e); });
    var visiveis = [];
    cards.forEach(function (c) {
      var area = c.getAttribute("data-area"), superior = c.getAttribute("data-superior") === "1";
      var ok = filtro === "todas" || (filtro === "tribunais-superiores" ? (superior || area === "tribunais-superiores") : area === filtro);
      c.classList.toggle("oculto", !ok);
      if (ok) visiveis.push(c);
    });
    if (filtro === "tribunais-superiores") {
      ORDEM.forEach(function (area) {
        var grupo = visiveis.filter(function (c) { return c.getAttribute("data-area") === area; });
        if (!grupo.length) return;
        var h = document.createElement("p"); h.className = "grupo-materia"; h.textContent = NOMES[area];
        lista.appendChild(h);
        grupo.forEach(function (c) { lista.appendChild(c); });
      });
    } else {
      visiveis.forEach(function (c) { lista.appendChild(c); });
    }
    cards.filter(function (c) { return c.classList.contains("oculto"); }).forEach(function (c) { lista.appendChild(c); });
    if (aviso) {
      if (!visiveis.length) { aviso.textContent = "Ainda não há publicações nesta área."; aviso.hidden = false; }
      else { aviso.textContent = visiveis.length + (visiveis.length === 1 ? " publicação" : " publicações"); aviso.hidden = false; }
    }
    Array.prototype.forEach.call(botoes, function (b) {
      var ativo = b.getAttribute("data-filtro") === filtro;
      b.classList.toggle("ativo", ativo); b.setAttribute("aria-pressed", ativo ? "true" : "false");
    });
    if (gravaHash && history.replaceState) history.replaceState(null, "", filtro === "todas" ? location.pathname : "#" + filtro);
  }
  function filtroDoHash() {
    var h = (location.hash || "").replace("#", "");
    return (h === "todas" || ORDEM.indexOf(h) >= 0) ? h : "todas";
  }
  Array.prototype.forEach.call(botoes, function (b) {
    b.addEventListener("click", function () { aplica(b.getAttribute("data-filtro"), true); });
  });
  window.addEventListener("hashchange", function () { aplica(filtroDoHash(), false); });
  aplica(filtroDoHash(), false);
})();
</script>
"""

CSS = """
/* ============================================
   LISTA DE PUBLICAÇÕES — filtro por área
   (botões .topico, cartões .pub-card) · 27/09/2026
   ============================================ */
.topico {
  padding: 8px 18px;
  background: var(--ivory-bg);
  border: 0.5px solid var(--gold-light);
  font-family: var(--sans);
  font-size: 12px;
  color: var(--navy);
  border-radius: 40px;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}
.topico:hover { border-color: var(--gold); }
.topico.ativo { background: var(--navy); border-color: var(--navy); color: var(--ivory); }
.topico:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.pub-card:hover { border-color: var(--gold) !important; }
.pub-card.oculto { display: none !important; }
.grupo-materia {
  font-size: 10px;
  letter-spacing: .3em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 500;
  margin: 26px 0 -4px;
  padding-bottom: 8px;
  border-bottom: 0.5px solid var(--border-medium);
}
.grupo-materia:first-of-type { margin-top: 0; }
.lista-aviso {
  text-align: center;
  font-family: var(--serif);
  font-style: italic;
  font-size: 15px;
  color: var(--text-muted);
  margin: -20px 0 26px;
}
"""


def ler(c: Path) -> str:
    return c.read_text(encoding="utf-8")


def gravar(c: Path, s: str):
    c.write_text(s, encoding="utf-8", newline="\n")


def lista_publicacoes(conferir: bool):
    arq = P.PUB / "publicacoes.html"
    s = ler(arq)
    # 1) pílulas -> botões
    if 'class="topico' not in s:
        nomes = PILULA.findall(s)
        botoes = ['<button type="button" class="topico ativo" data-filtro="todas" aria-pressed="true">Todas</button>']
        for nome in nomes:
            chave = P.normalizar_area(nome)
            if not chave:
                raise SystemExit(f"pílula sem área: {nome}")
            botoes.append(f'<button type="button" class="topico" data-filtro="{chave}" aria-pressed="false">{html.escape(P.AREAS[chave])}</button>')
        s = PILULA.sub("", s)
        s = s.replace('<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px;max-width:900px;margin:0 auto;">\n',
                      '<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px;max-width:900px;margin:0 auto;" role="group" aria-label="Filtrar publicações por área">\n'
                      + "\n".join(botoes) + "\n", 1)
        s = s.replace("<!-- Pílulas -->\n", "")
    # 2) grid com id + aviso
    if 'id="lista-publicacoes"' not in s:
        s = s.replace(GRID, '<p id="lista-aviso" class="lista-aviso" hidden></p>\n' + GRID.replace("<div ", '<div id="lista-publicacoes" ', 1), 1)
    # 3) cartões: atributos, rótulo e ordem
    i_marc = s.index(P.MARCADOR); i_marc = s.index("\n", i_marc) + 1
    achados = list(CARTAO.finditer(s, i_marc))
    if not achados:
        raise SystemExit("nenhum cartão encontrado depois do marcador")
    i0, fim = achados[0].start(), achados[-1].end()   # do primeiro ao último cartão
    cartoes = achados
    novos = []
    for m in achados:
        slug, texto = m.group(1), m.group(0)
        if slug not in CLASSIFICACAO:
            raise SystemExit(f"cartão sem classificação: {slug}")
        area, superior, data = CLASSIFICACAO[slug]
        texto = re.sub(r'<a href="' + re.escape(slug) + r'\.html"( class="pub-card"[^>]*?)?( style=)',
                       f'<a href="{slug}.html" class="pub-card" data-area="{area}" data-superior="{1 if superior else 0}" data-data="{data}"\\2', texto, count=1)
        texto = ROTULO_CARTAO.sub(lambda mm: mm.group(1) + html.escape(P.AREAS[area]) + mm.group(3), texto, count=1)
        novos.append((data, texto))
    novos.sort(key=lambda x: x[0], reverse=True)
    s = s[:i0] + "".join(t for _, t in novos) + s[fim:]
    # 4) script
    if MARCA_SCRIPT not in s:
        s = s.replace("</body>", SCRIPT + "</body>", 1)
    if conferir:
        print(f"publicacoes.html: {len(cartoes)} cartões classificados (conferência, nada gravado)")
    else:
        gravar(arq, s)
        print(f"publicacoes.html: {len(cartoes)} cartões classificados e reordenados; botões e filtro no lugar")


def paginas(conferir: bool):
    for slug, (area, superior, data) in CLASSIFICACAO.items():
        arq = P.PUB / f"{slug}.html"
        if not arq.exists():
            print(f"  {slug}: arquivo não existe, pulei"); continue
        s = ler(arq); nome = P.AREAS[area]; antes = s
        # molde do publicador: "PUBLICAÇÃO · <área> · <mês>"
        s = re.sub(r"(PUBLICAÇÃO · )([^·<]+?)( · )", lambda m: m.group(1) + html.escape(nome) + m.group(3), s, count=1)
        # molde antigo: <div class="post-meta"> <span>área</span> <span>subárea</span> ... <span>data</span>
        m = re.search(r'(<div class="post-meta">)(.*?)(</div>)', s, re.S)
        if m:
            spans = re.findall(r"<span>([^<]*)</span>", m.group(2))
            mantidos = [html.escape(nome)]
            for sp in spans[1:]:
                chave = P.normalizar_area(sp)
                eh_data = bool(re.search(r"\b(19|20)\d{2}\b", sp))
                if eh_data or chave is None:
                    mantidos.append(sp)          # data ou etiqueta descritiva ("Lei de Drogas") ficam
                # etiqueta que é outra área oficial (ou a mesma) sai, para não confundir
            recuo = re.match(r"\s*", m.group(2)).group(0) or "\n        "
            corpo = "".join(f"{recuo}<span>{x}</span>" for x in mantidos) + "\n      "
            s = s[:m.start()] + m.group(1) + corpo + m.group(3) + s[m.end():]
        if s != antes and not conferir:
            gravar(arq, s)
        print(f"  {slug}: área -> {nome}{' (alterado)' if s != antes else ' (já certo)'}")


def css(conferir: bool):
    arq = P.PUB / "assets" / "css" / "style.css"
    s = ler(arq)
    if ".topico" in s:
        print("style.css: bloco já existia"); return
    if not conferir:
        gravar(arq, s.rstrip("\n") + "\n" + CSS)
    print("style.css: bloco do filtro acrescentado")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-conferir", action="store_true")
    a = ap.parse_args()
    lista_publicacoes(a.so_conferir)
    paginas(a.so_conferir)
    css(a.so_conferir)


if __name__ == "__main__":
    main()
