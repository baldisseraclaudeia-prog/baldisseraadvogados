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
  python publicar.py testar pub.json --saida DIR -> gera só a página em DIR (não mexe no site)
  python publicar.py slug pub.json             -> diz o endereço (slug), a área oficial e se é julgado STF/STJ

Rodar pelo PowerShell: as capas (capa.py) usam o Edge em modo invisível, que não grava
a imagem quando chamado pelo Bash em sandbox.
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
# Ilustrações geradas pelo diretor de arte (agente baldissera-diretor-arte) ficam FORA do git,
# na pasta do painel; o publicador as copia (em JPG leve) para o site na hora de gerar.
IMAGENS_DIR = Path(r"C:\Users\LuizH\OneDrive\Área de Trabalho\SITE BALDISSERA ADVOGADOS\PAINEL-PUBLICACAO\IMAGENS")
if sys.platform == "darwin":  # Mac: a mesma pasta, pelo OneDrive do Mac
    IMAGENS_DIR = Path.home() / "Library/CloudStorage/OneDrive-Pessoal/Área de Trabalho/SITE BALDISSERA ADVOGADOS/PAINEL-PUBLICACAO/IMAGENS"
IMAGENS_SITE = PUB / "assets" / "images" / "publicacoes"
IMAGEM_LARGURA = 1600
LATERAL_LARGURA = 800            # capa quadrada ao lado do título (≈400 px na tela, dobro para tela retina)
ALT_PADRAO = "Ilustração editorial da publicação"
# REGRA do Dr. Luiz (27/09/2026): toda publicação leva os dois Instagram — na página e nas capas
INSTAGRAM = [("luizhbaldissera", "https://www.instagram.com/luizhbaldissera/"),
             ("baldisseraadvocacia", "https://www.instagram.com/baldisseraadvocacia/")]


def instagram_html() -> str:
    """Linha 'Siga no Instagram' do bloco de compartilhar (mesma em todos os moldes de página)."""
    links = ' <span style="color:var(--gold-light,#C9B98A);">·</span> '.join(
        f'<a href="{url}" target="_blank" rel="noopener" style="color:var(--navy,#0F172A);text-decoration:none;border-bottom:0.5px solid var(--gold-light,#C9B98A);">@{u}</a>'
        for u, url in INSTAGRAM)
    return (f'<p class="pub-insta" style="font-size:13px;letter-spacing:.02em;color:var(--text-muted,#7a7468);margin:18px 0 0;">'
            f'Siga no Instagram: {links}</p>')

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

# Ficha técnica (dados estruturados schema.org) — SEO de 04/10/2026.
# O escritório tem um identificador único (@id) definido na ficha da página inicial; artigos e
# perfis apontam para ele. As inscrições na OAB são as mesmas de AUTORES[...]["titulo"].
ESCRITORIO_ID = f"{BASE}/#escritorio"
LOGO = f"{BASE}/apple-touch-icon.png"
OABS = {"luiz": ["OAB/PR 55.717", "OAB/SC 78.938-A"], "charys": ["OAB/PR 69.897"],
        "karla": ["OAB/RS 66.523"], "anderson": ["OAB/PR 96.871"]}
LIMITE_TITULO = 60       # o Google mostra cerca de 60 caracteres do título
LIMITE_RESUMO = 160      # e cerca de 160 do resumo (PADRAO-EDITORIAL, seção 10)
SUFIXO_TITULO = " · Baldissera Advogados"


def json_ld(dados: dict) -> str:
    """Bloco <script type="application/ld+json">; '</' é escapado para não fechar o script."""
    corpo = json.dumps(dados, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{corpo}\n</script>'


def pessoa_ref(chave: str) -> dict:
    """Autor como pessoa: nome, cargo, OAB e o perfil no site (o @id liga à ficha do perfil)."""
    a = AUTORES[chave]
    pagina_perfil = f"{BASE}/{a['perfil'][:-5]}"            # perfil-luiz.html -> /perfil-luiz
    p = {"@type": "Person", "name": a["nome"], "jobTitle": a["titulo"].split(" · ")[0],
         "identifier": [{"@type": "PropertyValue", "propertyID": o.split(" ")[0], "value": o.split(" ", 1)[1]}
                        for o in OABS[chave]],
         "url": pagina_perfil, "worksFor": {"@id": ESCRITORIO_ID}}
    if a["perfil"].startswith("perfil-"):                   # só quem tem página própria ganha @id
        p["@id"] = f"{pagina_perfil}#pessoa"
    return p


def ficha_artigo(titulo: str, resumo: str, url: str, data: str, autor: str, imagem: str) -> str:
    """Ficha técnica de artigo (schema.org Article): título, resumo, data, autor com OAB, imagem."""
    return json_ld({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": titulo,
        "description": resumo,
        "url": url,
        "mainEntityOfPage": url,
        "datePublished": data,
        "inLanguage": "pt-BR",
        "image": imagem,
        "author": pessoa_ref(autor),
        "publisher": {"@type": "LegalService", "@id": ESCRITORIO_ID, "name": "Baldissera Advogados",
                      "url": BASE, "logo": LOGO},
    })

# As 7 áreas da lista de publicações (mesma ordem das pílulas de publicacoes.html).
# Chave = identificador usado em data-area e no #âncora da lista.
AREAS = {
    "direito-penal": "Direito Penal",
    "tribunais-superiores": "Tribunais Superiores",
    "execucao-penal": "Execução Penal",
    "imobiliario": "Imobiliário",
    "civil": "Civil",
    "familia-e-sucessoes": "Família e Sucessões",
    "ambiental": "Ambiental",
}
# Nomes alternativos que o publicador aceita e traduz para a área oficial (comparação sem acento/caixa)
AREA_ALIASES = {
    "penal": "direito-penal", "direito penal": "direito-penal", "processo penal": "direito-penal",
    "processual penal": "direito-penal", "direito processual penal": "direito-penal",
    "direito constitucional": "direito-penal",
    "tribunais superiores": "tribunais-superiores", "recursos aos tribunais superiores": "tribunais-superiores",
    "recursos a tribunais superiores": "tribunais-superiores", "recursos": "tribunais-superiores",
    "execucao penal": "execucao-penal", "direito imobiliario": "imobiliario", "imobiliario": "imobiliario",
    "civil": "civil", "direito civil": "civil", "familia e sucessoes": "familia-e-sucessoes",
    "familia": "familia-e-sucessoes", "sucessoes": "familia-e-sucessoes", "direito de familia": "familia-e-sucessoes",
    "direito das sucessoes": "familia-e-sucessoes", "ambiental": "ambiental", "direito ambiental": "ambiental",
}
# Sinais de que a publicação analisa julgado do STF/STJ (entra também na janela "Tribunais Superiores")
RE_SUPERIOR = re.compile(r"\bSTF\b|\bSTJ\b|Supremo Tribunal|Superior Tribunal de Justi|\bADPF\b|\bADI\b|\bREsp\b|\bAREsp\b|\bAgRg\b|\bRHC\b|\bRE\s?\d|Tema\s+\d+|repercuss[aã]o geral", re.I)


def normalizar_area(texto: str) -> "str | None":
    """Devolve a chave da área (ex.: 'execucao-penal') a partir de qualquer grafia aceita."""
    if not texto:
        return None

    def chave(t):
        t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
        return re.sub(r"\s+", " ", re.sub(r"[^a-z ]+", " ", t)).strip()

    if chave(texto) in AREA_ALIASES:
        return AREA_ALIASES[chave(texto)]
    # rótulos compostos ("Direito Penal · Lei de Drogas", "Direito Civil / Sucessões"): vale a primeira parte reconhecida
    for parte in re.split(r"[·•/|,;—–-]", texto):
        if chave(parte) in AREA_ALIASES:
            return AREA_ALIASES[chave(parte)]
    return None


def analisa_superior(p: dict) -> bool:
    """Detecta STF/STJ no título, subtítulo, resumo, citações e referências."""
    trechos = [p.get("titulo", ""), p.get("subtitulo", ""), p.get("resumo", "")]
    trechos += [r.get("nome", "") + " " + r.get("descricao", "") for r in p.get("referencias") or []]
    trechos += [b.get("fonte", "") for b in p.get("corpo") or [] if b.get("tipo") == "citacao"]
    return bool(RE_SUPERIOR.search(" ".join(trechos)))


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


def resumo_curto(texto: str, limite: int = 160) -> str:
    """Resumo para o Google: até 160 caracteres, cortado na última palavra inteira."""
    t = " ".join(plano(texto).split())
    if len(t) <= limite:
        return attr(t)
    corte = t[: limite - 1].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return attr(corte + "…")


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
    if p.get("area") and normalizar_area(p["area"]) is None:
        erros.append(f"área desconhecida: '{p['area']}' (use uma das 7: {', '.join(AREAS.values())})")
    for i, b in enumerate(p.get("corpo") or []):
        if b.get("tipo") not in TIPOS:
            erros.append(f"bloco {i + 1}: tipo inválido '{b.get('tipo')}'")
        elif not (b.get("texto") or "").strip():
            erros.append(f"bloco {i + 1}: sem texto")
    if p.get("resumo_google") and len(plano(p["resumo_google"])) > LIMITE_RESUMO:
        erros.append(f"resumo_google tem {len(plano(p['resumo_google']))} caracteres (máximo {LIMITE_RESUMO})")
    if p.get("titulo_google") and len(plano(p["titulo_google"]) + SUFIXO_TITULO) > LIMITE_TITULO:
        erros.append(f"titulo_google + '{SUFIXO_TITULO}' passa de {LIMITE_TITULO} caracteres")
    if p.get("imagem") and p["imagem"] is not True and localizar_imagem(p["imagem"]) is None:
        erros.append(f"ilustração não encontrada: {p['imagem']} (procurei em {IMAGENS_DIR})")
    txt = json.dumps(p, ensure_ascii=False)
    if "{{" in txt:
        erros.append("sobrou marcador {{...}} no texto")
    if re.search(r"<\s*(script|iframe|style)", txt, re.I):
        erros.append("o texto contém código de página (script, iframe ou style); por segurança nada foi publicado")
    return erros


def localizar_imagem(ref) -> "Path | None":
    """Acha o PNG da ilustração: caminho completo, nome na pasta IMAGENS (com ou sem .png)."""
    if not ref or ref is True:
        return None
    for cand in (Path(str(ref)), IMAGENS_DIR / str(ref), IMAGENS_DIR / f"{ref}.png"):
        if cand.is_file():
            return cand
    return None


def converter_imagem(fonte: Path, destino: Path, largura: int = IMAGEM_LARGURA, nitidez: bool = True) -> Path:
    """PNG grande -> JPG leve (nitidez leve), no padrão das imagens do site."""
    from PIL import Image, ImageFilter
    im = Image.open(fonte).convert("RGB")
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    if nitidez:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=110, threshold=2))
    destino.parent.mkdir(parents=True, exist_ok=True)
    im.save(destino, "JPEG", quality=84, optimize=True, progressive=True)
    return destino


def lateral_da_capa(capa_quadrada: Path, destino: Path) -> Path:
    """Capa quadrada (PNG 1080) -> JPG 800 px que vai ao lado do título na página (sem nitidez extra:
    a capa já tem texto nítido)."""
    return converter_imagem(capa_quadrada, destino, largura=LATERAL_LARGURA, nitidez=False)


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
    # área oficial (a pílula onde a publicação mora) e marca de julgado STF/STJ
    p["_area_slug"] = normalizar_area(p["area"]) or "direito-penal"
    p["area"] = AREAS[p["_area_slug"]]
    p["_superior"] = p["superior"] if isinstance(p.get("superior"), bool) else analisa_superior(p)
    # ilustração: campo "imagem" (caminho ou nome) ou, automaticamente, IMAGENS\<slug>.png;
    # "imagem": false desliga.
    if p.get("imagem") is False:
        fonte = None
    else:
        fonte = localizar_imagem(p.get("imagem")) or localizar_imagem(f"{slug}.png")
    p["_imagem_fonte"] = fonte
    # na página vai a CAPA QUADRADA (ilustração + logo + título) ao lado do título, estilo blog
    p["_imagem_web"] = f"assets/images/publicacoes/{slug}-lateral.jpg" if fonte else None
    p["_imagem_alt"] = plano(p.get("imagem_alt") or "") or ALT_PADRAO
    return p


# ------------------------------------------------------------------ página da publicação
# Visual "liturgia" (06/10/2026): cabeçalho, rodapé e recursos de <head> vêm de tools/molde.py;
# a mesma função montar_publicacao() serve à publicação nova (JSON) e ao revestimento das antigas.
sys.path.insert(0, str(AQUI.parent))
import molde  # noqa: E402

# página da área de cada chave de área (a trilha da publicação aponta para ela)
AREA_PAGINA = {"direito-penal": "area-direito-penal.html", "tribunais-superiores": "area-recursos-tribunais-superiores.html",
               "execucao-penal": "area-execucao-penal.html", "imobiliario": "area-direito-imobiliario.html",
               "civil": "area-direito-civil.html", "familia-e-sucessoes": "area-familia-sucessoes.html",
               "ambiental": "area-direito-ambiental.html"}
NOTA_WA = "A mensagem inclui o resumo, o link para a análise completa e o contato direto do escritório pelo WhatsApp."


def corpo_html(blocos: list, iniciais: str) -> str:
    """Blocos do JSON -> HTML do corpo, só com classes (nenhum style="")."""
    out = []
    for b in blocos:
        t = b["tipo"]
        if t == "destaque":
            out.append(f'<p class="destaque">{inline(b["texto"])}</p>')
        elif t == "paragrafo":
            out.append(f"<p>{inline(b['texto'])}</p>")
        elif t == "intertitulo":
            out.append(f"<h2>{inline(b['texto'])}</h2>")
        elif t == "caixa":
            rot = f'<p class="caixa-rotulo">{inline(b["rotulo"])}</p>\n' if b.get("rotulo") else ""
            tit = f"<h3>{inline(b['titulo'])}</h3>\n" if b.get("titulo") else ""
            out.append(f'<div class="caixa">\n{rot}{tit}<p>{inline(b["texto"])}</p>\n</div>')
        elif t == "citacao":
            fonte = f'<span class="fonte">{inline(b["fonte"])}</span>' if b.get("fonte") else ""
            out.append(f"<blockquote>{inline(b['texto'])}{fonte}</blockquote>")
    out.append(f'<p class="assinatura">— {iniciais}</p>')
    return "\n".join(out)


def montar_publicacao(head: str, *, slug: str, titulo_html: str, subtitulo_html: str, area: str, area_slug: str,
                      mes_ano: str, autor: str, leitura: int, imagem_web, imagem_alt: str, corpo: str,
                      referencias: list, wa_href: str, bio: str = None) -> str:
    """Página inteira da publicação no visual novo. `head` é o <head> técnico (preservado);
    `referencias` = [(nome_html, descricao_html)]; `corpo` já em HTML com classes."""
    a = AUTORES[autor]
    area_pag = AREA_PAGINA.get(area_slug, "publicacoes.html")
    figura = (f'\n  <figure><img src="{imagem_web}" alt="{html.escape(imagem_alt, quote=True)}" width="800" height="800" '
              f'fetchpriority="high" decoding="async"></figure>' if imagem_web else "")
    sem_fig = "" if imagem_web else " sem-figura"
    refs = ""
    if referencias:
        itens = "\n".join(f'<li><span class="ref-nome">{n}</span><span class="ref-desc">{dsc}</span></li>' for n, dsc in referencias)
        refs = f'\n<section class="referencias" aria-labelledby="t-refs">\n<h2 id="t-refs">Normas e julgados citados</h2>\n<ul>\n{itens}\n</ul>\n</section>'
    bio = bio if bio is not None else html.escape(a["bio"])     # a publicação revestida mantém a biografia que tinha
    bio = f'\n    <p class="bio">{bio}</p>' if bio else ""
    sobre = "Sobre a autora" if autor in ("charys", "karla") else "Sobre o autor"
    redes = " e ".join(f'<a href="{u}" target="_blank" rel="noopener">@{n}</a>' for n, u in INSTAGRAM)
    corpo_pag = f"""<p class="trilha"><a href="publicacoes.html">Publicações</a> / <a href="{area_pag}">{html.escape(area)}</a></p>

<article>
<header class="cabeca-pub{sem_fig}">
  <div>
    <p class="meta">{html.escape(area)}, {mes_ano.lower()}</p>
    <h1>{titulo_html}</h1>
    <p class="autoria">Por <a href="{a['perfil']}">{html.escape(a['nome'])}</a>, {html.escape(a['titulo'])}. Leitura de {leitura} {"minuto" if leitura == 1 else "minutos"}.</p>
  </div>{figura}
</header>

<p class="ementa"><span class="rotulo">Ementa</span>{subtitulo_html}</p>

<div class="corpo">
{corpo}
</div>
{refs}

<section class="autor-bloco" aria-label="{sobre}">
  <img src="{a['foto']}" alt="{html.escape(a['nome'])}" width="600" height="750" loading="lazy">
  <div>
    <p class="rotulo">{sobre}</p>
    <h2>{html.escape(a['nome'])}</h2>
    <p class="cargo">{html.escape(a['titulo'])}</p>{bio}
    <a class="remissao" href="{a['perfil']}">Ver perfil</a>
  </div>
</section>

<aside class="compartilhar" aria-label="Compartilhar">
  <p class="rotulo">Achou útil? Encaminhe a colegas e clientes</p>
  <a class="botao" href="{wa_href}" target="_blank" rel="noopener">Compartilhar no WhatsApp</a>
  <p class="nota">{NOTA_WA}</p>
  <p class="redes">No Instagram: {redes}</p>
</aside>

<p class="mais-publicacoes"><a class="remissao" href="publicacoes.html">Todas as publicações</a></p>
</article>"""
    return molde.pagina(head, corpo_pag, atual="Publicações")


def head_publicacao(p: dict) -> str:
    """<head> técnico da publicação nova (título, resumo, og, ficha de artigo)."""
    a = p["_autor"]
    url = f"{BASE}/{p['_slug']}"
    titulo_curto = plano(p.get("titulo_curto") or p["titulo"])
    desc = attr(p["resumo_google"]) if p.get("resumo_google") else resumo_curto(p["resumo"])
    titulo_aba = plano(p.get("titulo_google") or titulo_curto)
    ficha = ficha_artigo(plano(p["titulo"]), html.unescape(desc), url, p["data"], p["autor"],
                         f"{BASE}/assets/images/capas/{p['_slug']}-og.png")
    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{attr(titulo_aba)}{SUFIXO_TITULO}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Baldissera Advogados">
<meta property="og:title" content="{attr(titulo_curto)} · Baldissera Advogados">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<link rel="canonical" href="{url}">
<meta property="og:image" content="{BASE}/assets/images/capas/{p['_slug']}-og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:author" content="{attr(a['nome'])}">
<meta property="article:published_time" content="{p['data']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(titulo_curto)} · Baldissera Advogados">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/images/capas/{p['_slug']}-og.png">
{ficha}
<script defer src="/_vercel/insights/script.js"></script>
"""


def link_whatsapp(p: dict) -> str:
    url = f"{BASE}/{p['_slug']}"
    wa_txt = f"{plano(p['titulo'])}\n\n{plano(p['resumo'])}\n\nAnálise completa:\n{url}\n\n— Baldissera Advogados\nWhatsApp do escritório: https://wa.me/5545991029806"
    return f"https://wa.me/?text={quote(wa_txt, safe='')}"


def pagina(p: dict) -> str:
    return montar_publicacao(
        head_publicacao(p), slug=p["_slug"], titulo_html=inline(p["titulo"]), subtitulo_html=inline(p["subtitulo"]),
        area=p["area"], area_slug=p["_area_slug"], mes_ano=p["_mes_ano"], autor=p["autor"], leitura=p["_leitura"],
        imagem_web=p.get("_imagem_web"), imagem_alt="Capa da publicação: " + p["_imagem_alt"],
        corpo=corpo_html(p["corpo"], p["_autor"]["iniciais"]),
        referencias=[(inline(r.get("nome", "")), inline(r.get("descricao", ""))) for r in p.get("referencias") or []],
        wa_href=link_whatsapp(p))


# ------------------------------------------------------------------ cartão e sitemap
def capa_do_cartao(slug: str, titulo: str) -> str:
    """Miniatura da capa quadrada no cartão da lista (estilo blog)."""
    return (f'<img class="pub-card-capa" src="assets/images/publicacoes/{slug}-lateral.jpg" '
            f'alt="Capa da publicação: {attr(titulo)}" width="800" height="800" loading="lazy" decoding="async">')


def cartao(p: dict) -> str:
    """Cartão da lista de publicações (visual "liturgia"). Os atributos data-* alimentam o filtro
    de publicacoes.html, o bloco da home (home_recentes.py) e as páginas de área (area_recentes.py)."""
    a = p["_autor"]
    capa = (f'<img class="pub-card-capa" src="{p["_imagem_web"]}" alt="" width="800" height="800" loading="lazy" decoding="async">\n'
            if p.get("_imagem_web") else "")
    return (f'<a href="{p["_slug"]}.html" class="pub-card" data-area="{p["_area_slug"]}" data-superior="{1 if p["_superior"] else 0}" data-data="{p["data"]}">\n'
            f'{capa}<span class="pub-meta">{html.escape(p["area"])}, {p["_mes_ano"].lower()}</span>\n'
            f'<h3>{inline(p["titulo"])}</h3>\n'
            f'<p class="pub-resumo">{inline(p["resumo"])}</p>\n'
            f'<span class="pub-autor">{html.escape(a["nome"])}</span>\n'
            f'</a>\n')


def encaixar(p: dict):
    lista = PUB / "publicacoes.html"
    s = lista.read_text(encoding="utf-8")
    if f'href="{p["_slug"]}.html"' in s:
        return
    i = s.index(MARCADOR)
    i = s.index("\n", i) + 1
    lista.write_text(s[:i] + cartao(p) + s[i:], encoding="utf-8", newline="\n")
    import vitrines  # manchete e "Você sabia?" da home, publicações por área e índice da busca
    p["_vitrines"] = [str(f) for f in vitrines.atualizar_tudo(PUB)]
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
    ap.add_argument("acao", choices=["verificar", "slug", "testar", "gerar", "publicar"])
    ap.add_argument("json")
    ap.add_argument("--push", action="store_true", help="envia ao GitHub (põe no ar)")
    ap.add_argument("--ramo", default="main")
    ap.add_argument("--saida", help="pasta de saída do modo testar")
    a = ap.parse_args()
    p = json.loads(Path(a.json).read_text(encoding="utf-8"))
    # aceita também o documento da fila da página "Publicar no site" (a publicação vem no campo "pub")
    if isinstance(p.get("data"), dict) and "pub" in p["data"]:
        p = p["data"]
    if isinstance(p.get("pub"), dict):
        p = p["pub"]
    erros = verificar(p)
    if erros:
        print("NÃO PUBLICADO — corrigir:\n- " + "\n- ".join(erros)); sys.exit(2)
    if a.acao == "verificar":
        print("OK — pronto para publicar"); return
    if a.acao == "slug":
        # endereço que a publicação terá, área oficial e marca STF/STJ — usado pela rotina de minutas
        # para o diretor de arte gravar a ilustração com o nome certo (IMAGENS\<slug>.png)
        p = preparar(p)
        print(json.dumps({"slug": p["_slug"], "area": p["area"], "superior": p["_superior"],
                          "ilustracao": str(p["_imagem_fonte"] or "")}, ensure_ascii=False)); return
    if a.acao == "testar":
        p = preparar(p)
        destino = Path(a.saida or ".")
        destino.mkdir(parents=True, exist_ok=True)
        arq = destino / f"{p['_slug']}.html"
        import capa
        capas = capa.gerar(p, ["og", "quadrado", "vertical"], destino)
        pg = pagina(p)
        imagem = None
        if p.get("_imagem_fonte"):
            # a capa lateral ainda não está no ar: fica ao lado da prévia, com caminho local
            imagem = str(lateral_da_capa(destino / f"{p['_slug']}-quadrado.png", destino / f"{p['_slug']}-lateral.jpg"))
            pg = pg.replace(f'src="{p["_imagem_web"]}"', f'src="{p["_slug"]}-lateral.jpg"')
        # na prévia de teste os caminhos relativos apontam para o site no ar, para a página abrir com estilo e fotos
        arq.write_text(pg.replace('href="assets/', f'href="{BASE}/assets/').replace('src="assets/', f'src="{BASE}/assets/'),
                       encoding="utf-8", newline="\n")
        print(json.dumps({"ok": True, "no_ar": False, "teste": True, "arquivo": str(arq), "imagem": imagem, "capas": capas}, ensure_ascii=False)); return
    if a.acao == "publicar":
        if git("status", "--porcelain", "--untracked-files=no"):
            raise SystemExit("a cópia do site tem alterações não registradas; nada foi feito")
        git("checkout", a.ramo)
        if a.push:
            git("pull", "--ff-only", "origin", a.ramo)
    p = preparar(p)
    import capa
    capas = capa.gerar(p, ["og", "quadrado", "vertical"], PUB / "assets" / "images" / "capas")
    extras = []
    if p.get("_imagem_fonte"):
        extras.append(str(lateral_da_capa(PUB / "assets" / "images" / "capas" / f"{p['_slug']}-quadrado.png", PUB / p["_imagem_web"])))
    (PUB / f"{p['_slug']}.html").write_text(pagina(p), encoding="utf-8", newline="\n")
    encaixar(p)
    url = f"{BASE}/{p['_slug']}"
    saida = {"ok": True, "no_ar": False, "url": url, "arquivo": p["_slug"] + ".html",
             "imagem": extras[0] if extras else None, "capas": capas}
    if a.acao == "publicar":
        git("add", "--", str(PUB / f"{p['_slug']}.html"), str(PUB / "publicacoes.html"), str(PUB / "index.html"), str(PUB / "sitemap.xml"),
            *p.get("_vitrines", []), *extras, *capas)
        git("commit", "-m", f"Publicação: {plano(p.get('titulo_curto') or p['titulo'])} ({p['_autor']['nome']})")
        if a.push:
            git("push", "origin", a.ramo)
            saida["no_ar"] = True
    print(json.dumps(saida, ensure_ascii=False))


if __name__ == "__main__":
    main()
