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
        arquivo: {"avaliadas":[links], "destaques":[{"link","motivo"}], "ocultar":[links]}
    python noticias.py atualizar [--push]      # reescreve os quadros dos três; --push põe no ar

A última linha da saída é sempre um JSON {"ok": ...}. Fonte fora do ar = o quadro dela fica como estava.
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
NAVEGADOR_PY = Path(r"C:\Users\LuizH\scrapling-mcp\.venv\Scripts\python.exe")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36 (site Baldissera Advogados; noticias.py)"}
ULTIMAS, MAX_DESTAQUES = 5, 4
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


def ler_stf() -> list:
    base = "https://noticias.stf.jus.br/feed/?post_type=postsnoticias"
    itens = ler_rss(baixar_navegador(base), "https://noticias.stf.jus.br/", False)
    try:
        itens += ler_rss(baixar_navegador(base + "&paged=2"), "https://noticias.stf.jus.br/", False)
    except Exception:
        pass  # a segunda página é só reforço
    vistos, unicos = set(), []
    for i in itens:
        if i["link"] not in vistos:
            vistos.add(i["link"]); unicos.append(i)
    return unicos


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
        itens.append(item(titulo, raiz + (por or esp), q, resumo, resumo, "pt-br" if por else "es"))
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
    novos = [{k: i[k] for k in ("link", "titulo", "data", "resumo", "texto")}
             for i in ler(fonte) if i["link"] not in vistas and i["quando"] >= limite]
    return {"ok": True, "fonte": fonte, "candidatos": novos}


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
    gravar(d / "destaques_penal.json", atuais)
    gravar(d / "avaliadas.json", vistas[-1000:])
    gravar(d / "ocultas.json", ocultas[-500:])
    return {"ok": True, "fonte": fonte, "destaques_novos": aceitos,
            "recusados_link_fora_da_fonte_ou_sem_motivo": recusados, "ocultas": len(ocultas)}


# ------------------------------------------------------------------ home
def _lang(i):
    return ' lang="es"' if i.get("lang") == "es" else ""


def li_ultimas(itens: list, sigla: str) -> str:
    return "\n".join(
        f'<li><a href="{html.escape(i["link"], quote=True)}" target="_blank" rel="noopener">'
        f'<time datetime="{i["quando"][:10]}">{i["data"]}</time>'
        f'<span class="noticia-titulo"{_lang(i)}>{html.escape(i["titulo"])}</span>'
        f'<span class="sr-only"> (abre em nova aba, no site do {sigla})</span></a></li>'
        for i in itens)


def li_destaques(itens: list, sigla: str) -> str:
    return "\n".join(
        f'<li><a href="{html.escape(i["link"], quote=True)}" target="_blank" rel="noopener">'
        f'<time datetime="{i["quando"][:10]}">{i["data"]}</time>'
        f'<span class="destaque-titulo"{_lang(i)}>{html.escape(i["titulo"])}</span>'
        # a fonte repete o título quando a notícia não tem resumo: aí o resumo não aparece
        + (f'<span class="destaque-resumo"{_lang(i)}>{html.escape(i["resumo"])}</span>'
           if i["resumo"] and i["resumo"] != i["titulo"] else "") +
        f'<span class="sr-only"> (abre em nova aba, no site do {sigla})</span></a></li>'
        for i in itens)


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
            novo = trocar(novo, f"DESTAQUES-{marca}", li_destaques(dest, sigla_site[fonte]))
            relato[fonte] = {"ultimas": [f"{i['data']} {i['titulo']}" for i in itens[:ULTIMAS]],
                             "destaques": [f"{x['data']} {x['titulo']}" for x in dest]}
        except Exception as e:  # uma fonte fora do ar não derruba as outras
            erros[fonte] = str(e)[:200]
    mudou = novo != s
    if mudou:
        HOME.write_text(novo, encoding="utf-8", newline="\n")
    no_ar = False
    estado = [str(p) for p in AQUI.glob("*/*.json")]
    if push and (mudou or git("status", "--porcelain", "--", *estado)):
        git("add", "--", str(HOME), *estado)
        git("commit", "-m", f"Notícias dos tribunais na home ({dt.date.today().strftime('%d/%m/%Y')})")
        git("push", "origin", "main")
        no_ar = True
    return {"ok": not erros or bool(relato), "mudou": mudou, "no_ar": no_ar, "fontes": relato, "erros": erros}


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
