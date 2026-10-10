"""
Gera a página "Execução penal em linguagem simples" (public/execucao-penal-em-linguagem-simples.html)
a partir dos julgados explicados em tools/execucao/julgados/*.json (formato em FORMATO-JULGADO.md), no
molde do site (tools/molde.py). Também grava a lista "Julgamentos aguardados" da página de área
(area-execucao-penal.html, marcador JULGAMENTOS-AREA) e põe a página no sitemap.

Só entra julgado com situacao "publicar"; validar.py roda antes e trava se houver erro. Nunca editar o
HTML gerado: corrige-se o JSON e gera-se de novo.

Uso:  python3.12 tools/execucao/gerar_explicada.py [--contato A|B] [--rascunhos]
      --rascunhos inclui também os julgados em "rascunho"/"aguarda-selagem" (só para prévia local; marca cada bloco).
"""
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))             # molde
sys.path.insert(0, str(AQUI.parent / "publicador"))  # vitrines (e, dentro dele, pautas)
import comum  # noqa: E402
import molde  # noqa: E402
import validar  # noqa: E402

esc = comum.esc
PUBLIC = comum.PUBLIC
SLUG = "execucao-penal-em-linguagem-simples"
URL = f"{comum.BASE}/{SLUG}"
# A "Revisão da execução penal, por fases" só vai ao ar com o "publica" do Dr. Luiz. Com False, esta página não faz
# remissão a ela; trocar para True quando ela for ao ar (gera-se então esta página de novo, no mesmo envio).
REVISAO_NO_AR = True
REVISAO_PAGINA = "execucao-penal-revisao-por-fases.html"
REVISAO_HTML = ('<p class="ex-centro">Datas, frações e dias reconhecidos precisam estar corretamente registrados na execução. '
                'Um lançamento incorreto pode repercutir nos marcos seguintes. A revisão por fases começa pelo diagnóstico dos autos '
                'e indica as conferências adicionais pertinentes.</p>\n    '
                f'<p class="ex-centro"><a class="remissao" href="{REVISAO_PAGINA}">Revisão da execução penal, por fases</a></p>')
TITULO = "Execução penal em linguagem simples"
SUBTITULO = "O que o STJ e o STF decidiram sobre o cumprimento da pena, a quem pode alcançar e o que conferir."
DESCRICAO = ("Os julgados do STJ e do STF sobre o cumprimento da pena, sem juridiquês: a quem cada decisão pode alcançar, "
             "um exemplo em números, o que pode impedir o efeito, o documento que mostra e a tese oficial, para ler ou ouvir.")
PREAMBULO = ("Quem cumpre pena, e quem acompanha a execução de um parente, recebe decisões escritas numa língua que não é a "
             "de todos os dias. Esta página traduz cada uma delas: quem pode ser alcançado, o que muda em números, o que pode "
             "impedir o efeito e qual documento mostra se o direito foi aplicado. A tese oficial fica logo abaixo, inteira, "
             "com o endereço do tribunal e a data em que foi conferida.")
COMO_LER = [
    ("Tema repetitivo e repercussão geral", "Quando muitos processos levantam a mesma pergunta, o STJ (tema repetitivo) ou o STF "
     "(repercussão geral) escolhe um deles e fixa uma resposta que os demais juízes têm de seguir. No STF, o reconhecimento da repercussão geral só diz que a questão é relevante: para saber se o mérito já foi decidido, é preciso conferir a situação do tema. É por isso que cada bloco desta "
     "página traz o número do tema: ele identifica a questão discutida; a situação do tema informa se já existe tese firmada."),
    ("Em vigor, afetado, pendente", "\"Em vigor\" é a tese já fixada e aplicável. \"Afetado\" é o tema que o STJ escolheu para julgar e "
     "ainda não julgou. \"Repercussão geral reconhecida\" é a questão que o STF admitiu e ainda vai decidir. Nos pendentes, o bloco "
     "diz o que vale até o julgamento."),
    ("O limite de toda página", "Cada direito depende de condições que só os documentos do processo mostram. Por isso todo bloco "
     "termina com o documento que mostra, e a conferência começa por ele."),
]
MATERIAS = {  # ordem do sumário
    "detracao": "Da detração: o tempo que já conta",
    "progressao": "Da progressão de regime",
    "remicao": "Da remição: trabalho, estudo e leitura",
    "livramento": "Do livramento condicional",
    "indulto": "Do indulto e da comutação",
    "falta-grave": "Da falta grave e seus efeitos",
    "federal": "Do sistema penitenciário federal",
    "condicoes": "Das condições de cumprimento",
    "multa": "Da pena de multa",
}
NOME_CURTO = {"detracao": "Detração", "progressao": "Progressão", "remicao": "Remição", "livramento": "Livramento",
              "indulto": "Indulto", "falta-grave": "Falta grave", "federal": "Sistema federal", "condicoes": "Condições",
              "multa": "Multa"}
PALAVRAS = comum.PALAVRAS   # fonte única em tools/execucao/comum.py (09/10/2026), compartilhada com a Revisão por fases


def fmt_data(iso: str) -> str:
    if not iso:
        return ""
    a, m, d = iso.split("-")
    return f"{d}/{m}/{a}"


def situacao_linha(j: dict) -> str:
    s = j["selagem"]
    partes = [esc(s["situacao_publica"]).capitalize(), esc(s["rotulo_fonte"]) if s.get("rotulo_fonte") else f'{esc(s["tribunal"])}, {esc(s["classe"].split(" (")[0])}']
    if s.get("julgamento"):
        partes.append(f'tese fixada em {fmt_data(s["julgamento"])}')
    elif s.get("publicacao"):
        partes.append(f'acórdão de repercussão geral publicado em {fmt_data(s["publicacao"])}')
    partes.append(f'conferido em {fmt_data(s["verificado_em"])}')
    return " · ".join(partes)


def audio_html(j: dict) -> str:
    a = j.get("audio") or {}
    nar, tit = a.get("narracao") or {}, a.get("titular") or {}
    tem_nar = nar.get("arquivo") and (PUBLIC / nar["arquivo"]).exists()
    tem_tit = tit.get("arquivo") and (PUBLIC / tit["arquivo"]).exists()
    if not tem_nar and not tem_tit:
        return ('<div class="ex-audio ex-audio-vazio"><p class="ex-rotulo">Ouvir este julgado</p>'
                '<p class="ex-duracao">Áudio em preparação. O texto abaixo é o conteúdo integral.</p></div>')
    def dur(seg):
        if not seg:
            return ""
        m, s = divmod(int(seg), 60)
        return f"{m} min {s:02d} s" if m else f"{s} s"
    faixas = []
    if tem_nar:
        faixas.append(("narracao", "Narração (voz sintética)", nar["arquivo"], "audio/mpeg", dur(nar.get("duracao_s"))))
    if tem_tit:
        faixas.append(("titular", f"Na voz de {comum.AUTOR}", tit["arquivo"], "audio/mp4", dur(tit.get("duracao_s"))))
    botoes = "".join(f'<button type="button" class="topico{" ativo" if i == 0 else ""}" data-faixa="{k}" '
                     f'aria-pressed="{"true" if i == 0 else "false"}">{esc(n)}</button>' for i, (k, n, *_r) in enumerate(faixas))
    players = "".join(
        f'<p class="ex-faixa-nome" data-faixa="{k}">{esc(n)}{(" · " + d) if d else ""}</p>'
        f'<audio controls preload="none" data-faixa="{k}" aria-label="{esc(n)}: {esc(j["titulo"])}">'
        f'<source src="{arq}" type="{tipo}"></audio>' for k, n, arq, tipo, d in faixas)
    return (f'<div class="ex-audio" data-faixas><p class="ex-rotulo">Ouvir este julgado</p>'
            f'<div class="ex-faixas" role="group" aria-label="Escolher a voz"{"" if len(faixas) > 1 else " hidden"}>{botoes}</div>'
            f'{players}<p class="ex-duracao">O áudio resume o texto deste bloco; o texto traz as condições e os limites completos.</p></div>')


def bloco_rotulado(classe: str, rotulo: str, corpo: str) -> str:
    return f'<div class="ex-bloco {classe}"><p class="ex-rotulo">{esc(rotulo)}</p>{corpo}</div>'


def julgado_html(j: dict, rascunho: bool = False) -> str:
    s, rel = j["selagem"], j.get("relacionados") or {}
    pend = bool(j.get("pendente"))
    partes = [f'<article class="ex-julgado{" ex-pendente" if pend else ""}" id="{j["id"]}" data-materia="{j["materia"]}" '
              f'aria-labelledby="t-{j["id"]}">']
    if rascunho:
        partes.append('<p class="ex-rascunho">Rascunho: não revisado</p>')
    partes.append(f'<p class="ex-trib">{situacao_linha(j)}</p>')
    partes.append(f'<h3 id="t-{j["id"]}"><a class="ex-ancora" href="#{j["id"]}">{esc(j["titulo"])}</a></h3>')
    partes.append(audio_html(j))
    partes.append(bloco_rotulado("ex-alcance", "Quem pode ser alcançado", f'<p>{esc(j["alcance"])}</p>'))
    partes.append(bloco_rotulado("ex-parabola", "Para entender", f'<p>{esc(j["parabola"])}</p>'))
    if pend:
        if j.get("em_jogo"):
            partes.append(bloco_rotulado("ex-decidiu", "O que está em jogo", f'<p>{esc(j["em_jogo"])}</p>'))
        if j.get("ate_la"):
            partes.append(bloco_rotulado("ex-atela", "O que vale até o julgamento", f'<p>{esc(j["ate_la"])}</p>'))
    else:
        ex = j["exemplo"]
        partes.append(bloco_rotulado("ex-exemplo", "Em números (exemplo fictício)",
                                     f'<p class="ex-premissas">{esc(ex["premissas"])}</p><p>{esc(ex["texto"])}</p>'
                                     f'<p class="ex-conta">{esc(ex["conta"])}</p>'))
    partes.append(bloco_rotulado("ex-decidiu", "O que o tribunal decidiu", f'<p>{esc(j["decidiu"])}</p>'))
    partes.append(bloco_rotulado("ex-limites", "O que pode impedir ou reduzir o efeito",
                                 "<ul>" + "".join(f"<li>{esc(l)}</li>" for l in j["limites"]) + "</ul>"))
    partes.append(bloco_rotulado("ex-documento", "O documento que mostra", f'<p>{esc(j["documento"])}</p>'))
    ref = " · ".join(x for x in [esc(s["tribunal"]), esc(s["classe"]), esc(s.get("relator") or ""), esc(s.get("orgao") or ""),
                                 f'julgado em {fmt_data(s["julgamento"])}' if s.get("julgamento") else "",
                                 f'publicado em {fmt_data(s["publicacao"])}' if s.get("publicacao") else "",
                                 f'trânsito em julgado em {fmt_data(s["transito"])}' if s.get("transito") else ""] if x)
    rotulo_integra = j.get("rotulo_integra") or ("Ler a questão submetida, na íntegra" if pend else "Ler a tese oficial, na íntegra")
    partes.append(f'<details class="ex-integra"><summary>{esc(rotulo_integra)}</summary>'
                  f'<blockquote>{esc(s["tese_verbatim"])}<span class="rv-ref">{ref}</span></blockquote>'
                  f'<p class="ex-fonte"><a href="{s["url_oficial"]}" target="_blank" rel="noopener">Conferir no portal do {esc(s["tribunal"])}'
                  f'<span class="so-leitor"> (abre em nova aba, no site do tribunal)</span></a> · conferido em {fmt_data(s["verificado_em"])}'
                  f'{(" · " + esc(s["nota_situacao"])) if s.get("nota_situacao") else ""}</p></details>')
    links = []
    if rel.get("publicacao"):
        links.append(f'<a class="remissao" href="{rel["publicacao"]}">Análise completa no site</a>')
    if REVISAO_NO_AR:
        links.append(f'<a class="remissao" href="{REVISAO_PAGINA}{rel.get("revisao_ancora") or ""}">'
                     'Como isso é conferido na revisão da execução</a>')
    for b in rel.get("blocos") or []:
        links.append(f'<a class="remissao" href="#{b}">Ver o julgado relacionado</a>')
    partes.append('<p class="ex-ponte">' + " · ".join(links) + "</p>")
    wa = quote(f"{j['titulo']}\n\n{URL}#{j['id']}\n\n— Baldissera Advogados", safe="")
    partes.append(f'<p class="ex-compartilhar"><a class="botao" href="https://wa.me/?text={wa}" target="_blank" rel="noopener">'
                  'Encaminhar este julgado pelo WhatsApp</a></p>')
    partes.append("</article>")
    return "\n".join(partes)


def carregar(rascunhos: bool = False) -> list:
    js = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(validar.JULGADOS.glob("*.json"))]
    js = [j for j in js if j["situacao"] == "publicar" or rascunhos]
    return sorted(js, key=lambda j: (list(MATERIAS).index(j["materia"]), j.get("ordem", 0), j["id"]))


def corpo_html(js: list, contato: str, rascunhos: bool) -> str:
    vigor = [j for j in js if not j.get("pendente")]
    pend = [j for j in js if j.get("pendente")]
    materias = [m for m in MATERIAS if any(j["materia"] == m for j in vigor)]
    sumario = "".join(f'<a href="#m-{m}">{esc(NOME_CURTO[m])}</a>' for m in materias)
    if pend:
        sumario += '<a href="#aguardados">Julgamentos aguardados</a>'
    filtros = '<button class="topico ativo" type="button" data-filtro="todas" aria-pressed="true">Todas</button>' + "".join(
        f'<button class="topico" type="button" data-filtro="{m}" aria-pressed="false">{esc(NOME_CURTO[m])}</button>' for m in materias)
    out = [f'''  <p class="trilha"><a href="areas-de-atuacao.html">Áreas de atuação</a> / <a href="area-execucao-penal.html">Execução Penal</a> / Em linguagem simples</p>

  <section class="abertura abertura-area ex-abertura">
    <h1>{esc(TITULO)}</h1>
    <p class="ex-subtitulo">{esc(SUBTITULO)}</p>
    <p class="preambulo">{esc(PREAMBULO)}</p>
    <nav class="sumario" aria-label="Nesta página">{sumario}</nav>
  </section>

  <section class="secao" id="como-ler" aria-labelledby="t-como-ler">
    <header>
      <span class="numeral" aria-hidden="true">I</span>
      <h2 id="t-como-ler">Como ler esta página</h2>
    </header>
    <dl class="ex-como-ler">''']
    for t, d in COMO_LER:
        out.append(f"      <dt>{esc(t)}</dt><dd>{esc(d)}</dd>")
    out.append("    </dl>\n  </section>")
    out.append(f'''
  <section class="secao" id="vale" aria-labelledby="t-vale">
    <header>
      <span class="numeral" aria-hidden="true">II</span>
      <h2 id="t-vale">Do que já vale</h2>
      <p class="nota-secao">Leis, súmulas, temas repetitivos e decisões do STJ e do STF sobre o cumprimento da pena. Cada bloco identifica a fonte, seu alcance e seus limites, diz a quem pode alcançar e o que pode impedir o efeito.</p>
    </header>
    <div class="filtros" role="group" aria-label="Filtrar por matéria">{filtros}</div>
    <p id="ex-aviso" class="nota-secao centro" hidden></p>''')
    for m in materias:
        out.append(f'    <section class="ex-materia" id="m-{m}" data-materia="{m}" aria-labelledby="t-m-{m}">\n'
                   f'      <h3 class="ex-materia-titulo" id="t-m-{m}">{esc(MATERIAS[m])}</h3>')
        for j in (x for x in vigor if x["materia"] == m):
            out.append(julgado_html(j, rascunhos and j["situacao"] != "publicar"))
        out.append("    </section>")
    out.append("  </section>")
    if pend:
        out.append('''
  <section class="secao" id="aguardados" aria-labelledby="t-aguardados">
    <header>
      <span class="numeral" aria-hidden="true">III</span>
      <h2 id="t-aguardados">Do que ainda será julgado</h2>
      <p class="nota-secao">Questões que o STJ ou o STF já admitiram e ainda vão decidir. Cada bloco diz o que vale até o julgamento. Datas conforme os portais dos tribunais.</p>
    </header>''')
        for j in pend:
            out.append(julgado_html(j, rascunhos and j["situacao"] != "publicar"))
        out.append("  </section>")
    n = "IV" if pend else "III"
    out.append(f'''
  <section class="secao" id="palavras" aria-labelledby="t-palavras">
    <header>
      <span class="numeral" aria-hidden="true">{n}</span>
      <h2 id="t-palavras">Das palavras usadas nesta página</h2>
    </header>
    <dl class="ex-palavras">''')
    for t, d in PALAVRAS:
        out.append(f"      <dt>{esc(t)}</dt><dd>{esc(d)}</dd>")
    out.append("    </dl>\n  </section>")
    n2 = "VI" if pend else "V"
    out.append("\n  " + comum.publicacoes_html("V" if pend else "IV"))
    out.append(f'''
  <section class="secao" id="revisao" aria-labelledby="t-revisao">
    <header>
      <span class="numeral" aria-hidden="true">{n2}</span>
      <h2 id="t-revisao">{"Da revisão da execução penal, por fases" if REVISAO_NO_AR else "Do atendimento"}</h2>
    </header>
    {REVISAO_HTML if REVISAO_NO_AR else ""}
    {comum.contato_html(contato)}
    {comum.aviso_html()}
  </section>

{comum.autor_html()}

  <aside class="compartilhar" aria-label="Compartilhar">
    <p class="rotulo">Achou útil? Encaminhe a quem precisa entender</p>
    <p class="nota">Cada julgado tem o próprio endereço: o título é o link.</p>
    <p class="redes">{comum.redes_html()}</p>
  </aside>''')
    return "\n".join(out)


def head_html(js: list) -> str:
    t = f"{TITULO} · Baldissera Advogados"
    partes = []
    for j in js:
        s = j["selagem"]
        art = {"@type": "Article", "@id": f"{URL}#{j['id']}", "headline": j["titulo"], "inLanguage": "pt-BR",
               "author": {"@type": "Person", "name": comum.AUTOR}, "citation": s["url_oficial"],
               "dateModified": s["verificado_em"]}
        nar = (j.get("audio") or {}).get("narracao") or {}
        if nar.get("arquivo") and (PUBLIC / nar["arquivo"]).exists():
            art["audio"] = {"@type": "AudioObject", "contentUrl": f"{comum.BASE}/{nar['arquivo']}", "encodingFormat": "audio/mpeg",
                            "transcript": j["audio"]["roteiro"].strip()}
            if nar.get("duracao_s"):
                art["audio"]["duration"] = f"PT{int(nar['duracao_s'])}S"
        partes.append(art)
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": TITULO, "url": URL, "description": DESCRICAO,
          "inLanguage": "pt-BR", "isPartOf": {"@type": "WebSite", "name": "Baldissera Advogados", "url": comum.BASE},
          "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Áreas de atuação", "item": f"{comum.BASE}/areas-de-atuacao"},
              {"@type": "ListItem", "position": 2, "name": "Execução Penal", "item": f"{comum.BASE}/area-execucao-penal"},
              {"@type": "ListItem", "position": 3, "name": TITULO, "item": URL}]},
          "hasPart": partes}
    return f'''<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t}</title>
<link rel="canonical" href="{URL}">
<meta name="description" content="{esc(DESCRICAO)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Baldissera Advogados">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{esc(DESCRICAO)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{comum.BASE}/assets/images/capas/execucao-penal-em-linguagem-simples-og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{esc(DESCRICAO)}">
<meta name="twitter:image" content="{comum.BASE}/assets/images/capas/execucao-penal-em-linguagem-simples-og.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script defer src="/_vercel/insights/script.js"></script>
'''


DEPOIS = '''<script>
(function () {
  var botoes = document.querySelectorAll(".filtros .topico[data-filtro]"), secoes = document.querySelectorAll(".ex-materia[data-materia]");
  var aviso = document.getElementById("ex-aviso");
  if (!botoes.length) return;
  var nomes = {};
  Array.prototype.forEach.call(botoes, function (b) { nomes[b.getAttribute("data-filtro")] = b.textContent; });
  function aplica(filtro, gravaHash) {
    var n = 0;
    Array.prototype.forEach.call(secoes, function (s) {
      var ok = filtro === "todas" || s.getAttribute("data-materia") === filtro;
      s.hidden = !ok; if (ok) n += s.querySelectorAll(".ex-julgado").length;
    });
    Array.prototype.forEach.call(botoes, function (b) {
      var ativo = b.getAttribute("data-filtro") === filtro;
      b.classList.toggle("ativo", ativo); b.setAttribute("aria-pressed", ativo ? "true" : "false");
    });
    if (aviso) { aviso.textContent = n + (n === 1 ? " julgado" : " julgados") + (filtro === "todas" ? "" : " em " + nomes[filtro]); aviso.hidden = false; }
    if (gravaHash && history.replaceState) history.replaceState(null, "", filtro === "todas" ? location.pathname : "#m-" + filtro);
  }
  function filtroDoHash() {
    var h = (location.hash || "").replace("#", "");
    if (h.indexOf("m-") === 0 && nomes[h.slice(2)]) return h.slice(2);
    return "todas";
  }
  Array.prototype.forEach.call(botoes, function (b) { b.addEventListener("click", function () { aplica(b.getAttribute("data-filtro"), true); }); });
  window.addEventListener("hashchange", function () { aplica(filtroDoHash(), false); });
  aplica(filtroDoHash(), false);
  window.addEventListener("beforeprint", function () { Array.prototype.forEach.call(document.querySelectorAll("details"), function (d) { d.open = true; }); });
})();
</script>
'''


def lista_area(js: list) -> str:
    pend = [j for j in js if j.get("pendente")]
    if not pend:
        return '<li class="pauta-vazia">Lista em preparação.</li>'
    itens = []
    for j in pend:
        s = j["selagem"]
        itens.append(f'<li><span class="pauta-tema"><a href="{SLUG}.html#{j["id"]}">{esc(j["titulo"])}</a></span>'
                     f'<span class="pauta-situacao">{esc(s["tribunal"])} · {esc(s["situacao_publica"])}</span></li>')
    return "\n".join(itens)


def atualizar_area(js: list) -> list:
    import vitrines
    f = PUBLIC / "area-execucao-penal.html"
    s = f.read_text(encoding="utf-8")
    if "<!-- JULGAMENTOS-AREA-INICIO" not in s or "<!-- JULGAMENTOS-AREA-FIM -->" not in s:
        raise RuntimeError("area-execucao-penal.html: faltam os marcadores JULGAMENTOS-AREA")
    novo = vitrines.trocar(s, "JULGAMENTOS-AREA", lista_area(js))
    if novo != s:
        f.write_text(novo, encoding="utf-8", newline="\n")
        return [f]
    return []


def sitemap(hoje: str):
    sm = PUBLIC / "sitemap.xml"
    t = sm.read_text(encoding="utf-8")
    if f"<loc>{URL}</loc>" in t:
        i = t.index(f"<loc>{URL}</loc>")
        a = t.index("<lastmod>", i) + len("<lastmod>")
        b = t.index("</lastmod>", a)
        t = t[:a] + hoje + t[b:]
    else:
        t = t.replace("</urlset>", f"  <url>\n    <loc>{URL}</loc>\n    <lastmod>{hoje}</lastmod>\n"
                                   f"    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>")
    sm.write_text(t, encoding="utf-8", newline="\n")


def gerar(contato: str = None, rascunhos: bool = False) -> Path:
    erros = [x for x in validar.todos() if "(aviso)" not in x]
    if erros:
        for x in erros:
            print(x)
        sys.exit(f"{len(erros)} erro(s) nos julgados; nada gerado")
    js = carregar(rascunhos)
    destino = PUBLIC / f"{SLUG}.html"
    destino.write_text(molde.pagina(head_html(js), corpo_html(js, contato or comum.CONTATO_PADRAO, rascunhos), "Atuação", DEPOIS),
                       encoding="utf-8", newline="\n")
    n = len(destino.read_text(encoding="utf-8").split('<article class="ex-julgado'))- 1
    assert n == len(js), f"{n} artigos gerados para {len(js)} julgados"
    atualizar_area([j for j in js if j["situacao"] == "publicar"])
    sitemap(date.today().isoformat())
    return destino


if __name__ == "__main__":
    args = sys.argv[1:]
    contato = args[args.index("--contato") + 1].upper() if "--contato" in args else None
    print(gerar(contato, "--rascunhos" in args))
