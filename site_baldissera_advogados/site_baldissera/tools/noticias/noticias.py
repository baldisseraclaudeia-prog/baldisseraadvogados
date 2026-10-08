"""
Notícias dos tribunais na página inicial — STJ, STF e Corte Interamericana de Direitos Humanos.

Decisões do Dr. Luiz (04/10/2026):
- para cada tribunal, "Últimas notícias" (as 5 mais recentes, todas) e, em quadro separado,
  "Destaques em matéria penal" (decisão criminal favorável à defesa);
- atualização automática diária (rotina noticias-stj-site, 7h), sem revisão de advogado;
- no site só aparecem título, data, resumo e link do próprio tribunal — nada redigitado.
  QUEM ESCOLHE os destaques é a rotina (lê o texto); este programa só recebe LINKS e tira o
  resto da fonte oficial. Regra da casa: título com nome de parte/vítima não aparece (ocultar).

Fontes (conferidas em 04/10/2026):
- STJ: feed oficial https://res.stj.jus.br/hrestp-c-portalp/RSS.xml (página "Conteúdos por feed
  (RSS)" do portal). Lido direto.
- STF: feed do portal de notícias https://noticias.stf.jus.br/feed/?post_type=postsnoticias.
  O STF barra leitura por programa simples; a leitura passa pelo navegador automático do
  ambiente scrapling-mcp (C:\\Users\\LuizH\\scrapling-mcp\\.venv), com o Chrome da máquina.
- Corte IDH: página oficial de comunicados em português
  https://www.corteidh.or.cr/comunicados_prensa.cfm?lang=pt (o link de cada item é o PDF do
  comunicado, em português quando existe; senão, em espanhol).

    python noticias.py candidatos --fonte stj|stf|corteidh [--dias 7]
    python noticias.py registrar  --fonte stj|stf|corteidh <arquivo.json>
        arquivo: {"avaliadas":[links], "destaques":[{"link","motivo"}], "ocultar":[links],
                  "materias": {link: ["direito-penal", "execucao-penal", ...]}}
        (desde 06/10/2026, "materias" classifica a notícia nas páginas de área; a matéria é
        decidida pela rotina, que lê o texto — este programa não adivinha por palavra-chave;
        os destaques penais entram sozinhos na página de Direito Penal)
    python noticias.py atualizar [--push]      # reescreve os quadros dos três; --push põe no ar

A última linha da saída é sempre um JSON {"ok": ...}. Fonte fora do ar = o quadro dela fica como estava.

Visual "liturgia" (06/10/2026): na home, os três tribunais em colunas alinhadas (as 5 últimas de
cada um) e a hora real da última atualização; os destaques e as notícias classificadas por matéria
vão para as páginas de área (marcadores NOTICIAS-AREA-INICIO/FIM em public/area-*.html).
"""
import argparse
import base64
import datetime as dt
import email.utils
import html
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[3]
HOME = REPO / "site_baldissera_advogados" / "site_baldissera" / "public" / "index.html"
# navegador automático: Windows (scrapling-mcp) ou Mac (scrapling instalado pelo uv, 07/10/2026)
NAVEGADOR_PY = next((p for p in (Path(r"C:\Users\LuizH\scrapling-mcp\.venv\Scripts\python.exe"),
                               Path.home() / ".local" / "share" / "uv" / "tools" / "scrapling" / "bin" / "python")
                     if p.exists()), Path(r"C:\Users\LuizH\scrapling-mcp\.venv\Scripts\python.exe"))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36 (site Baldissera Advogados; noticias.py)"}
ULTIMAS, MAX_DESTAQUES = 5, 4
MAX_AREA = 6
PUBLIC = HOME.parent
# matéria (chave) -> página de área; os destaques penais vão para "direito-penal"
AREAS = {"direito-penal": "area-direito-penal.html", "tribunais-superiores": "area-recursos-tribunais-superiores.html",
         "execucao-penal": "area-execucao-penal.html", "imobiliario": "area-direito-imobiliario.html",
         "civil": "area-direito-civil.html", "familia-e-sucessoes": "area-familia-sucessoes.html",
         "ambiental": "area-direito-ambiental.html", "leiloes": "area-leiloes.html"}
NOME_TRIBUNAL = {"stj": "Superior Tribunal de Justiça", "stf": "Supremo Tribunal Federal",
                 "corteidh": "Corte Interamericana de Direitos Humanos"}
BRASILIA = dt.timezone(dt.timedelta(hours=-3))
CONTEUDO = "{http://purl.org/rss/1.0/modules/content/}encoded"
MESES = {"jan": 1, "fev": 2, "feb": 2, "mar": 3, "abr": 4, "apr": 4, "mai": 5, "may": 5, "jun": 6, "jul": 7,
         "ago": 8, "aug": 8, "set": 9, "sep": 9, "out": 10, "oct": 10, "nov": 11, "dez": 12, "dic": 12, "dec": 12,
         "ene": 1, "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
         "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12, "enero": 1, "febrero": 2,
         "marzo": 3, "mayo": 5, "junio": 6, "julio": 7, "septiembre": 9, "setiembre": 9, "octubre": 10,
         "noviembre": 11, "diciembre": 12}


# ------------------------------------------------------------------ utilidades
def limpo(t: str) -> str:
    t = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", t or "")).replace("\u200b", "").split())
    return re.sub(r"\s+([,.;:)])", r"\1", t)  # espa\u00e7o que sobra das etiquetas antes da pontua\u00e7\u00e3o


def baixar(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()


def baixar_navegador(url: str) -> bytes:
    """Abre a página no Chrome automático (para sites que barram programa simples)."""
    if not NAVEGADOR_PY.exists():
        raise RuntimeError("ambiente do navegador automático não encontrado (scrapling-mcp)")
    codigo = ("import sys,base64;from scrapling.fetchers import DynamicFetcher as D;"
              "p=D.fetch(sys.argv[1],headless=True,network_idle=True,wait=3000,timeout=60000,real_chrome=True);"
              "b=p.body if isinstance(p.body,(bytes,bytearray)) else str(p.body).encode('utf-8');"
              "print('STATUS',p.status);print(base64.b64encode(b).decode())")
    r = subprocess.run([str(NAVEGADOR_PY), "-c", codigo, url], capture_output=True, text=True, timeout=180)
    linhas = [l for l in r.stdout.splitlines() if l.strip()]
    st = next((l for l in linhas if l.startswith("STATUS")), "STATUS ?")
    if r.returncode or st != "STATUS 200" or not linhas:
        raise RuntimeError(f"navegador automático não leu {url} ({st}; {r.stderr.strip()[-200:]})")
    return base64.b64decode(linhas[-1])


def item(titulo, link, quando: dt.datetime, resumo="", texto="", lang="pt-br") -> dict:
    return {"titulo": titulo, "link": link, "quando": quando.isoformat(timespec="minutes"),
            "data": quando.strftime("%d/%m/%Y"), "resumo": resumo, "texto": texto, "lang": lang}


# ------------------------------------------------------------------ leitores
def ler_rss(raw: bytes, origem: str, data_br: bool) -> list:
    itens = []
    for it in ET.fromstring(raw).iter("item"):
        titulo, link = limpo(it.findtext("title")), (it.findtext("link") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        if data_br:  # STJ: "Sáb, out 3 2026 17:01:00" (horário de Brasília)
            m = re.search(r"(\w{3})\w*\s+(\d{1,2})\s+(\d{4})\s+(\d{1,2}):(\d{2})", pub.split(",", 1)[-1])
            if not m or m.group(1).lower() not in MESES:
                continue
            q = dt.datetime(int(m.group(3)), MESES[m.group(1).lower()], int(m.group(2)), int(m.group(4)), int(m.group(5)))
        else:        # STF (WordPress): "Sun, 04 Oct 2026 16:12:28 +0000"
            try:
                q = email.utils.parsedate_to_datetime(pub).astimezone(BRASILIA).replace(tzinfo=None)
            except (TypeError, ValueError):
                continue
        if not titulo or not link.startswith(origem):
            continue
        texto = limpo(it.findtext(CONTEUDO))
        if not texto:  # STJ declara o módulo com https
            texto = limpo(it.findtext("{https://purl.org/rss/1.0/modules/content/}encoded"))
        itens.append(item(titulo, link, q, limpo(it.findtext("description")), texto))
    return itens


def ler_stj() -> list:
    return ler_rss(baixar("https://res.stj.jus.br/hrestp-c-portalp/RSS.xml"), "https://www.stj.jus.br/", True)


def baixar_stf(url: str) -> bytes:
    """O STF ora aceita a requisição simples (Mac, 07/10/2026), ora barra (Windows): tenta a simples,
    e só abre o navegador automático se ela falhar ou vier sem notícia."""
    try:
        raw = baixar(url)
        if b"<item>" in raw:
            return raw
    except Exception:
        pass
    return baixar_navegador(url)


def ler_stf() -> list:
    base = "https://noticias.stf.jus.br/feed/?post_type=postsnoticias"
    itens = ler_rss(baixar_stf(base), "https://noticias.stf.jus.br/", False)
    try:
        itens += ler_rss(baixar_stf(base + "&paged=2"), "https://noticias.stf.jus.br/", False)
    except Exception:
        pass  # a segunda página é só reforço
    vistos, unicos = set(), []
    for i in itens:
        if i["link"] not in vistos:
            vistos.add(i["link"]); unicos.append(i)
    return unicos


_EN = re.compile(r"\b(the|of|on|and|in|for|with|court|beginning)\b", re.I)
_ES = re.compile(r"\b(la|las|los|del|el|sobre la|en materia|y)\b", re.I)
_PT = re.compile(r"(ção|ções|ão\b|\bdo\b|\bda\b|\bdos\b|\bdas\b|\bnão\b|\bé\b)", re.I)


def idioma(texto: str, padrao: str = "pt-br") -> str:
    """Idioma do título: português, espanhol ou inglês (contagem de palavras típicas)."""
    pt, es, en = len(_PT.findall(texto)), len(_ES.findall(texto)), len(_EN.findall(texto))
    if en > max(pt, es):
        return "en"
    if es > pt:
        return "es"
    return "pt-br" if pt else padrao


def ler_corteidh() -> list:
    raiz = "https://www.corteidh.or.cr/"
    s = baixar(raiz + "comunicados_prensa.cfm?lang=pt").decode("utf-8", "replace")
    partes = re.split(r'<h4 class="text-justify">', s)[1:]
    itens = []
    for p in partes:
        p = p.split("<h4", 1)[0]
        titulo = limpo(p.split("</h4>", 1)[0])
        corpo = p.split("</h4>", 1)[-1]
        pdfs = re.findall(r'href="(docs/comunicados/cp_\d+_\d{4}(?:_ENG|_POR)?\.pdf)"', corpo)
        por = next((x for x in pdfs if x.endswith("_POR.pdf")), None)
        esp = next((x for x in pdfs if not x.endswith(("_POR.pdf", "_ENG.pdf"))), None)
        texto = limpo(corpo)
        m = re.search(r"(\d{1,2})º?\s+de\s+([a-zçA-Z]+)\s+(?:de\s+)?(\d)\s*(\d)\s*(\d)\s*(\d)", texto)
        if not titulo or not (por or esp) or not m or m.group(2).lower() not in MESES:
            continue
        q = dt.datetime(int("".join(m.group(3, 4, 5, 6))), MESES[m.group(2).lower()], int(m.group(1)), 12, 0)
        resumo = texto[m.end():].lstrip(" .-").split(" Espanhol versión")[0].strip()
        # o título vem em português quando há versão em português; senão, em espanhol
        itens.append(item(titulo, raiz + (por or esp), q, resumo, resumo, idioma(titulo, "pt-br" if por else "es")))
    return itens


FONTES = {"stj": ("STJ", ler_stj), "stf": ("STF", ler_stf), "corteidh": ("CORTEIDH", ler_corteidh)}


# ------------------------------------------------------------------ estado de cada fonte
def pasta(fonte: str) -> Path:
    p = AQUI / fonte
    p.mkdir(exist_ok=True)
    return p


def carregar(p: Path, padrao):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else padrao


def gravar(p: Path, dados):
    p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def ler(fonte: str) -> list:
    itens = FONTES[fonte][1]()
    itens.sort(key=lambda i: i["quando"], reverse=True)
    return itens


def candidatos(fonte: str, dias: int) -> dict:
    vistas = set(carregar(pasta(fonte) / "avaliadas.json", []))
    limite = (dt.datetime.now() - dt.timedelta(days=dias)).isoformat(timespec="minutes")
    trad = carregar(pasta(fonte) / "traducoes.json", {})
    todos = ler(fonte)
    novos = [{k: i[k] for k in ("link", "titulo", "data", "resumo", "texto", "lang")}
             for i in todos if i["link"] not in vistas and i["quando"] >= limite]
    sem = [{"link": i["link"], "lang": i["lang"], "titulo": i["titulo"], "resumo": i["resumo"]}
           for i in todos[:ULTIMAS] if i.get("lang", "pt-br") != "pt-br" and i["link"] not in trad]
    return {"ok": True, "fonte": fonte, "candidatos": novos, "traduzir": sem}


def registrar(fonte: str, arquivo: str) -> dict:
    pedido = json.loads(Path(arquivo).read_text(encoding="utf-8-sig"))
    d = pasta(fonte)
    feed = {i["link"]: i for i in ler(fonte)}
    vistas, ocultas = carregar(d / "avaliadas.json", []), carregar(d / "ocultas.json", [])
    atuais = carregar(d / "destaques_penal.json", [])
    ja = {x["link"] for x in atuais}
    aceitos, recusados = [], []
    for link in pedido.get("avaliadas", []) + pedido.get("ocultar", []):
        if link in feed and link not in vistas:
            vistas.append(link)
    for link in pedido.get("ocultar", []):
        if link in feed and link not in ocultas:
            ocultas.append(link)
    for x in pedido.get("destaques", []):
        i = feed.get(x.get("link", ""))
        motivo = " ".join(str(x.get("motivo", "")).split())[:400]
        if not i or not motivo:
            recusados.append(x.get("link", "")); continue
        if i["link"] in ja:
            continue
        atuais.append({**{k: i[k] for k in ("link", "titulo", "quando", "data", "resumo", "lang")}, "motivo": motivo,
                       "escolhido_em": dt.datetime.now().isoformat(timespec="minutes")})
        if i["link"] not in vistas:
            vistas.append(i["link"])
        aceitos.append(i["titulo"])
    atuais.sort(key=lambda x: x["quando"], reverse=True)
    # classificação por matéria (página de área), decidida pela rotina
    materias = carregar(d / "materias.json", [])
    por_link = {x["link"]: x for x in materias}
    classificadas = []
    for link, areas in (pedido.get("materias") or {}).items():
        i = feed.get(link)
        areas = [a for a in (areas or []) if a in AREAS]
        if not i or not areas:
            recusados.append(link); continue
        por_link[link] = {**{k: i[k] for k in ("link", "titulo", "quando", "data", "resumo", "lang")}, "areas": areas,
                          "classificado_em": dt.datetime.now().isoformat(timespec="minutes")}
        classificadas.append(i["titulo"])
    trad = carregar(d / "traducoes.json", {})
    traduzidas = []
    for link, t in (pedido.get("traducoes") or {}).items():
        titulo = " ".join(str((t or {}).get("titulo", "")).split())
        if link not in feed or not titulo:
            recusados.append(link); continue
        trad[link] = {"titulo": titulo, "resumo": " ".join(str(t.get("resumo", "")).split()),
                      "original": feed[link]["titulo"], "lang": feed[link].get("lang"),
                      "traduzido_em": dt.datetime.now().isoformat(timespec="minutes")}
        traduzidas.append(titulo)
    gravar(d / "traducoes.json", trad)
    materias = sorted(por_link.values(), key=lambda x: x["quando"], reverse=True)[:300]
    gravar(d / "materias.json", materias)
    gravar(d / "destaques_penal.json", atuais)
    gravar(d / "avaliadas.json", vistas[-1000:])
    gravar(d / "ocultas.json", ocultas[-500:])
    return {"ok": True, "fonte": fonte, "destaques_novos": aceitos, "classificadas_por_materia": classificadas,
            "traduzidas": traduzidas,
            "recusados_link_fora_da_fonte_ou_sem_motivo": recusados, "ocultas": len(ocultas)}


# ------------------------------------------------------------------ home
def _lang(i):
    return f' lang="{i["lang"]}"' if i.get("lang") in ("es", "en") else ""


_TRAD = {}


def traducao(i: dict) -> dict:
    """Tradução gravada pela rotina para item em espanhol ou inglês ({} se não houver ou se já for português)."""
    if i.get("lang", "pt-br") == "pt-br":
        return {}
    if not _TRAD:
        for f in FONTES:
            _TRAD.update(carregar(pasta(f) / "traducoes.json", {}))
    return _TRAD.get(i["link"], {})


def _trad_html(texto: str) -> str:
    return f'<span class="traducao" lang="pt-br"><span class="traducao-rotulo">Tradução</span> {html.escape(texto)}</span>'



def li_ultimas(itens: list, sigla: str) -> str:
    """Itens de uma coluna da home (data em cima, título com link)."""
    return "\n".join(
        f'<li role="listitem"><time datetime="{i["quando"][:10]}">{i["data"]}</time>'
        f'<a href="{html.escape(i["link"], quote=True)}" target="_blank" rel="noopener"{_lang(i)}>{html.escape(i["titulo"])}'
        f'<span class="so-leitor"> (abre em nova aba, no site {"da" if sigla.startswith("Corte") else "do"} {sigla})</span></a>'
        + (_trad_html(traducao(i)["titulo"]) if traducao(i) else "") + '</li>'
        for i in itens)


def li_destaques(itens: list, sigla: str) -> str:
    """Mantido para compatibilidade: a home não tem mais quadro de destaques (vão para as áreas)."""
    return li_area([{**i, "_fonte": sigla} for i in itens])


def li_area(itens: list) -> str:
    """Decisões e notícias de uma matéria (página de área): data, tribunal, título com link e resumo oficial."""
    if not itens:
        return ('<li class="decisao-vazia"><p>Ainda não há decisões ou notícias recentes classificadas nesta matéria. '
                'As fontes oficiais de jurisprudência estão na seção seguinte.</p></li>')
    out = []
    for i in itens:
        nome = NOME_TRIBUNAL.get(i.get("_fonte"), i.get("_fonte", ""))
        resumo = (f'\n<p{_lang(i)}>{html.escape(i["resumo"])}</p>' if i.get("resumo") and i["resumo"] != i["titulo"] else "")
        t = traducao(i)
        if t:
            resumo = f'\n<p class="traducao-titulo">{_trad_html(t["titulo"])}</p>' + resumo + (
                f'\n<p>{_trad_html(t["resumo"])}</p>' if t.get("resumo") and resumo else "")
        out.append(f'<li>\n<p class="decisao-meta"><time datetime="{i["quando"][:10]}">{i["data"]}</time> <span>{nome}</span></p>\n'
                   f'<h3><a href="{html.escape(i["link"], quote=True)}" target="_blank" rel="noopener"{_lang(i)}>{html.escape(i["titulo"])}'
                   f'<span class="so-leitor"> (abre em nova aba, no site do tribunal)</span></a></h3>{resumo}\n</li>')
    return "\n".join(out)


def itens_por_area() -> dict:
    """Junta, por matéria, os destaques (penal) e as notícias classificadas pela rotina, dos três tribunais."""
    por = {k: {} for k in AREAS}
    for fonte in FONTES:
        d = pasta(fonte)
        for x in carregar(d / "destaques_penal.json", []):
            for area in x.get("areas") or ["direito-penal"]:
                if area in por:
                    por[area][x["link"]] = {**x, "_fonte": fonte}
        for x in carregar(d / "materias.json", []):
            for area in x.get("areas", []):
                if area in por:
                    por[area].setdefault(x["link"], {**x, "_fonte": fonte})
    return {k: sorted(v.values(), key=lambda i: i["quando"], reverse=True)[:MAX_AREA] for k, v in por.items()}


def atualizar_areas() -> list:
    """Reescreve o bloco NOTICIAS-AREA de cada página de área. Devolve as páginas que mudaram."""
    mudaram = []
    for area, itens in itens_por_area().items():
        pag = PUBLIC / AREAS[area]
        if not pag.exists():
            continue
        s = pag.read_text(encoding="utf-8")
        if "<!-- NOTICIAS-AREA-INICIO" not in s:
            continue
        novo = trocar(s, "NOTICIAS-AREA", li_area(itens))
        if novo != s:
            pag.write_text(novo, encoding="utf-8", newline="\n")
            mudaram.append(pag)
    return mudaram


def trocar(s: str, marca: str, miolo: str) -> str:
    ini, fim = f"<!-- {marca}-INICIO", f"<!-- {marca}-FIM -->"
    if ini not in s or fim not in s:
        raise RuntimeError(f"marcadores {marca} não encontrados na home")
    a = s.index("\n", s.index(ini)) + 1
    return s[:a] + (miolo + "\n" if miolo else "") + s[s.index(fim):]


def git(*args):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)} falhou: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def atualizar(push: bool) -> dict:
    s = HOME.read_text(encoding="utf-8")
    novo, relato, erros = s, {}, {}
    sigla_site = {"stj": "STJ", "stf": "STF", "corteidh": "Corte IDH"}
    for fonte, (marca, _) in FONTES.items():
        try:
            d = pasta(fonte)
            ocultas = set(carregar(d / "ocultas.json", []))
            itens = [i for i in ler(fonte) if i["link"] not in ocultas]
            if len(itens) < 3:
                raise RuntimeError(f"a fonte trouxe só {len(itens)} notícia(s) válida(s)")
            dest = carregar(d / "destaques_penal.json", [])[:MAX_DESTAQUES]
            novo = trocar(novo, f"NOTICIAS-{marca}", li_ultimas(itens[:ULTIMAS], sigla_site[fonte]))
            if f"<!-- DESTAQUES-{marca}-INICIO" in novo:          # home antiga (antes de 06/10/2026)
                novo = trocar(novo, f"DESTAQUES-{marca}", li_destaques(dest, sigla_site[fonte]))
            relato[fonte] = {"ultimas": [f"{i['data']} {i['titulo']}" for i in itens[:ULTIMAS]],
                             "destaques": [f"{x['data']} {x['titulo']}" for x in dest]}
        except Exception as e:  # uma fonte fora do ar não derruba as outras
            erros[fonte] = str(e)[:200]
    if relato and "<!-- ATUALIZADO-INICIO" in novo:
        agora = dt.datetime.now(BRASILIA)
        novo = trocar(novo, "ATUALIZADO", f'<time datetime="{agora.isoformat(timespec="minutes")}">{agora.strftime("%d/%m/%Y, às %Hh%M")}</time>')
    mudou = novo != s
    if mudou:
        HOME.write_text(novo, encoding="utf-8", newline="\n")
    areas_mudadas = atualizar_areas()
    no_ar = False
    estado = [str(p) for p in AQUI.glob("*/*.json")]
    if push and (mudou or areas_mudadas or git("status", "--porcelain", "--", *estado)):
        git("add", "--", str(HOME), *[str(x) for x in areas_mudadas], *estado)
        git("commit", "-m", f"Notícias dos tribunais na home ({dt.date.today().strftime('%d/%m/%Y')})")
        git("push", "origin", "main")
        no_ar = True
    return {"ok": not erros or bool(relato), "mudou": mudou, "areas": [x.name for x in areas_mudadas],
            "no_ar": no_ar, "fontes": relato, "erros": erros}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", choices=["candidatos", "registrar", "atualizar"])
    ap.add_argument("arquivo", nargs="?")
    ap.add_argument("--fonte", choices=list(FONTES))
    ap.add_argument("--dias", type=int, default=7)
    ap.add_argument("--push", action="store_true", help="registra e envia ao GitHub (põe no ar)")
    a = ap.parse_args()
    try:
        if a.acao in ("candidatos", "registrar") and not a.fonte:
            raise RuntimeError("informe --fonte stj, stf ou corteidh")
        if a.acao == "atualizar" and a.push:
            # só os arquivos de estado das notícias podem estar alterados (registro feito nesta rodada)
            sujos = [l for l in git("status", "--porcelain", "--untracked-files=no").splitlines()
                     if "/tools/noticias/" not in l.replace("\\", "/") or not l.strip().endswith(".json")]
            if sujos:
                raise RuntimeError("a cópia do site tem alterações não registradas; nada foi feito")
            git("checkout", "main")
            git("pull", "--ff-only", "--autostash", "origin", "main")
        if a.acao == "candidatos":
            r = candidatos(a.fonte, a.dias)
        elif a.acao == "registrar":
            if not a.arquivo:
                raise RuntimeError("informe o arquivo JSON com as avaliações")
            r = registrar(a.fonte, a.arquivo)
        else:
            r = atualizar(a.push)
        print(json.dumps(r, ensure_ascii=False))
        if not r.get("ok"):
            sys.exit(1)
    except Exception as e:  # rede, fonte ou git: relata e não mexe em mais nada
        print(json.dumps({"ok": False, "erro": str(e)[:300]}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
