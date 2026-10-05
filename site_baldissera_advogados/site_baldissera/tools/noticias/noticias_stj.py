"""
Notícias do STJ na página inicial (04/10/2026, decisões do Dr. Luiz):
- "Últimas do STJ": todas as notícias, as 5 mais recentes, atualização automática diária;
- "Destaques em matéria penal": notícia criminal com decisão favorável à defesa, em quadro
  separado. QUEM ESCOLHE é a rotina diária (lê o texto inteiro da notícia no feed); este
  programa só recebe os LINKS escolhidos e tira título, data e resumo do próprio feed do STJ —
  nada é redigitado.

Fonte: feed oficial https://res.stj.jus.br/hrestp-c-portalp/RSS.xml (indicado na página
"Conteúdos por feed (RSS)" do portal do STJ). Só entram links que começam com
https://www.stj.jus.br/. Sem texto nosso no site.

    python noticias_stj.py candidatos [--dias 7]     # JSON das notícias ainda não avaliadas (com o texto)
    python noticias_stj.py registrar <arquivo.json>  # {"avaliadas":[links], "destaques":[{"link","motivo"}], "ocultar":[links]}
    python noticias_stj.py atualizar [--push]        # reescreve os dois quadros da home; --push põe no ar

A última linha da saída é sempre um JSON {"ok": ...}. Feed fora do ar = nada muda.
"""
import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED = "https://res.stj.jus.br/hrestp-c-portalp/RSS.xml"
ORIGEM_OK = "https://www.stj.jus.br/"
AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[3]
HOME = REPO / "site_baldissera_advogados" / "site_baldissera" / "public" / "index.html"
AVALIADAS = AQUI / "avaliadas.json"        # links já examinados pela rotina (não reexaminar)
DESTAQUES = AQUI / "destaques_penal.json"  # destaques escolhidos, com o motivo (registro interno)
OCULTAS = AQUI / "ocultas.json"            # notícias com nome de parte: não aparecem em "Últimas" (regra da casa)
ULTIMAS, MAX_DESTAQUES = 5, 4
MARCAS = {"ultimas": ("<!-- NOTICIAS-STJ-INICIO", "<!-- NOTICIAS-STJ-FIM -->"),
          "destaques": ("<!-- DESTAQUES-PENAL-INICIO", "<!-- DESTAQUES-PENAL-FIM -->")}
MESES = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
         "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}
# formato do feed em 04/10/2026: "Sáb, out 3 2026 17:01:00"
DATA = re.compile(r"(\w{3})\w*\s+(\d{1,2})\s+(\d{4})\s+(\d{1,2}):(\d{2})")
CONTEUDO = "{https://purl.org/rss/1.0/modules/content/}encoded"


def limpo(t: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", t or "")).replace("​", "").split())


def ler_feed() -> list:
    req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (site Baldissera Advogados; noticias_stj.py)"})
    raw = urllib.request.urlopen(req, timeout=40).read()
    itens = []
    for it in ET.fromstring(raw).iter("item"):
        titulo = limpo(it.findtext("title"))
        link = (it.findtext("link") or "").strip()
        m = DATA.search((it.findtext("pubDate") or "").split(",", 1)[-1])
        if not titulo or not link.startswith(ORIGEM_OK) or not m or m.group(1).lower() not in MESES:
            continue
        q = dt.datetime(int(m.group(3)), MESES[m.group(1).lower()], int(m.group(2)), int(m.group(4)), int(m.group(5)))
        itens.append({"titulo": titulo, "link": link, "quando": q.isoformat(timespec="minutes"),
                      "data": q.strftime("%d/%m/%Y"), "resumo": limpo(it.findtext("description")),
                      "texto": limpo(it.findtext(CONTEUDO))})
    itens.sort(key=lambda i: i["quando"], reverse=True)
    return itens


def carregar(p: Path, padrao):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else padrao


def gravar(p: Path, dados):
    p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def li_ultimas(itens: list) -> str:
    return "\n".join(
        f'<li><a href="{html.escape(i["link"], quote=True)}" target="_blank" rel="noopener">'
        f'<time datetime="{i["quando"][:10]}">{i["data"]}</time>'
        f'<span class="noticia-titulo">{html.escape(i["titulo"])}</span>'
        f'<span class="sr-only"> (abre em nova aba, no site do STJ)</span></a></li>'
        for i in itens)


def li_destaques(itens: list) -> str:
    return "\n".join(
        f'<li><a href="{html.escape(i["link"], quote=True)}" target="_blank" rel="noopener">'
        f'<time datetime="{i["quando"][:10]}">{i["data"]}</time>'
        f'<span class="destaque-titulo">{html.escape(i["titulo"])}</span>'
        # o feed repete o título quando a notícia não tem resumo: aí o resumo não aparece
        + (f'<span class="destaque-resumo">{html.escape(i["resumo"])}</span>' if i["resumo"] and i["resumo"] != i["titulo"] else "") +
        f'<span class="sr-only"> (abre em nova aba, no site do STJ)</span></a></li>'
        for i in itens)


def trocar(s: str, chave: str, miolo: str) -> str:
    ini, fim = MARCAS[chave]
    if ini not in s or fim not in s:
        raise RuntimeError(f"marcadores {chave} não encontrados na home")
    a = s.index("\n", s.index(ini)) + 1
    return s[:a] + (miolo + "\n" if miolo else "") + s[s.index(fim):]


def git(*args):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)} falhou: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def candidatos(dias: int) -> dict:
    vistas = set(carregar(AVALIADAS, []))
    limite = (dt.datetime.now() - dt.timedelta(days=dias)).isoformat(timespec="minutes")
    novos = [{k: i[k] for k in ("link", "titulo", "data", "resumo", "texto")}
             for i in ler_feed() if i["link"] not in vistas and i["quando"] >= limite]
    return {"ok": True, "candidatos": novos}


def registrar(arquivo: str) -> dict:
    pedido = json.loads(Path(arquivo).read_text(encoding="utf-8"))
    feed = {i["link"]: i for i in ler_feed()}
    vistas = carregar(AVALIADAS, [])
    for link in pedido.get("avaliadas", []):
        if link in feed and link not in vistas:
            vistas.append(link)
    atuais = carregar(DESTAQUES, [])
    ja = {d["link"] for d in atuais}
    aceitos, recusados = [], []
    for d in pedido.get("destaques", []):
        i = feed.get(d.get("link", ""))
        motivo = " ".join(str(d.get("motivo", "")).split())[:400]
        if not i or not motivo:
            recusados.append(d.get("link", "")); continue
        if i["link"] in ja:
            continue
        atuais.append({**{k: i[k] for k in ("link", "titulo", "quando", "data", "resumo")}, "motivo": motivo,
                       "escolhido_em": dt.datetime.now().isoformat(timespec="minutes")})
        if i["link"] not in vistas:
            vistas.append(i["link"])
        aceitos.append(i["titulo"])
    ocultas = carregar(OCULTAS, [])
    for link in pedido.get("ocultar", []):
        if link in feed and link not in ocultas:
            ocultas.append(link)
            if link not in vistas:
                vistas.append(link)
    atuais.sort(key=lambda x: x["quando"], reverse=True)
    gravar(DESTAQUES, atuais)
    gravar(AVALIADAS, vistas[-1000:])
    gravar(OCULTAS, ocultas[-500:])
    return {"ok": True, "destaques_novos": aceitos, "recusados_link_fora_do_feed_ou_sem_motivo": recusados,
            "ocultas": len(ocultas)}


def atualizar(push: bool) -> dict:
    ocultas = set(carregar(OCULTAS, []))
    itens = [i for i in ler_feed() if i["link"] not in ocultas]
    if len(itens) < 3:
        raise RuntimeError(f"o feed do STJ trouxe só {len(itens)} notícia(s) válida(s); a home ficou como estava")
    destaques = carregar(DESTAQUES, [])[:MAX_DESTAQUES]
    s = HOME.read_text(encoding="utf-8")
    novo = trocar(trocar(s, "ultimas", li_ultimas(itens[:ULTIMAS])), "destaques", li_destaques(destaques))
    mudou = novo != s
    if mudou:
        HOME.write_text(novo, encoding="utf-8", newline="\n")
    no_ar = False
    if push and (mudou or git("status", "--porcelain", "--", str(AVALIADAS), str(DESTAQUES), str(OCULTAS))):
        git("add", "--", str(HOME), str(AVALIADAS), str(DESTAQUES), str(OCULTAS))
        git("commit", "-m", f"Notícias do STJ na home ({itens[0]['data']})")
        git("push", "origin", "main")
        no_ar = True
    return {"ok": True, "mudou": mudou, "no_ar": no_ar,
            "ultimas": [f"{i['data']} {i['titulo']}" for i in itens[:ULTIMAS]],
            "destaques": [f"{d['data']} {d['titulo']}" for d in destaques]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", choices=["candidatos", "registrar", "atualizar"])
    ap.add_argument("arquivo", nargs="?")
    ap.add_argument("--dias", type=int, default=7)
    ap.add_argument("--push", action="store_true", help="registra e envia ao GitHub (põe no ar)")
    a = ap.parse_args()
    try:
        if a.acao == "atualizar" and a.push:
            # só os arquivos das notícias podem estar alterados (registro feito antes nesta rodada)
            sujos = [l for l in git("status", "--porcelain", "--untracked-files=no").splitlines()
                     if not l.strip().endswith(("avaliadas.json", "destaques_penal.json", "ocultas.json"))]
            if sujos:
                raise RuntimeError("a cópia do site tem alterações não registradas; nada foi feito")
            git("checkout", "main")
            git("pull", "--ff-only", "--autostash", "origin", "main")
        if a.acao == "candidatos":
            r = candidatos(a.dias)
        elif a.acao == "registrar":
            if not a.arquivo:
                raise RuntimeError("informe o arquivo JSON com as avaliações")
            r = registrar(a.arquivo)
        else:
            r = atualizar(a.push)
        print(json.dumps(r, ensure_ascii=False))
    except Exception as e:  # rede, feed ou git: relata e não mexe em mais nada
        print(json.dumps({"ok": False, "erro": str(e)[:300]}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
