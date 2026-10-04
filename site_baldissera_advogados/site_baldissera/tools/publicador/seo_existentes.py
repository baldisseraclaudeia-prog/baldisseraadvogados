"""SEO das publicações já no ar (04/10/2026).

Aplica às 12 publicações anteriores ao publicador novo o que ele já faz nas novas:
  1. título curto para o Google nas que passavam de 60 caracteres;
  2. resumo (meta description, og e twitter) de até 160 caracteres, escrito à mão a partir do
     resumo e do texto de cada publicação — nada de fato novo;
  3. data de publicação no código (article:published_time) nas que não tinham;
  4. intertítulos do molde antigo (<div class="post-section-label">) marcados como h2,
     com a mesma aparência (a classe já define fonte, tamanho e margens);
  5. ficha técnica de artigo (schema.org Article, publicar.py: ficha_artigo).

Idempotente: rodar de novo não duplica nada (a ficha antiga é trocada pela nova).
Uso:  python seo_existentes.py [--so-conferir]
"""
import argparse, html, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import publicar as P

# Datas: as do cartão da lista (classificar_existentes.py, aprovadas pelo Dr. Luiz em 27/09/2026),
# que batem com a data visível no topo de cada página. Exceção marcada abaixo.
PUBLICACOES = {
    "publicacao-adpf-347-na-execucao-penal": dict(
        autor="luiz", data="2026-09-27", titulo_google=None,
        resumo="O STF reconheceu o estado de coisas inconstitucional das prisões. Na execução penal, o argumento só rende com prova concreta da unidade e pedido específico."),
    "publicacao-cadeia-de-custodia": dict(
        autor="luiz", data="2026-01-15", titulo_google=None,
        resumo=None),   # o resumo atual já tem 149 caracteres
    "publicacao-colacao-doacao-dissimulada-resp-2171573-ms": dict(
        autor="charys", data="2026-05-06", titulo_google="Doação dissimulada e colação no STJ",
        resumo="REsp 2.171.573/MS: para o STJ, a dispensa de colação exige declaração expressa do doador (art. 2.006 do CC). A doação dissimulada deve ser colacionada."),
    "publicacao-domiciliar-humanitaria-6t-stj": dict(
        autor="luiz", data="2026-05-26", titulo_google="Domiciliar humanitária na Sexta Turma",
        resumo="Quatro precedentes da Sexta Turma do STJ desenham o teste da domiciliar humanitária e o que a defesa precisa provar de plano (art. 318, II e III, do CPP)."),
    "publicacao-impronuncia-aresp-3065825-pe": dict(
        autor="luiz", data="2026-04-27", titulo_google="STJ restabelece impronúncia",
        resumo="AREsp 3.065.825/PE: o STJ restabeleceu a impronúncia porque a pronúncia não pode se apoiar só no inquérito, sem prova confirmada em juízo (art. 155 do CPP)."),
    "publicacao-pena-em-dobro-por-prisao-degradante": dict(
        autor="luiz", data="2026-09-30", titulo_google=None,
        resumo="No RHC 136.961/RJ, a Quinta Turma do STJ mandou contar em dobro todo o tempo de pena cumprido no Instituto Penal Plácido de Sá Carvalho, como fixou a Corte IDH."),
    "publicacao-prova-digital-sem-hash": dict(
        autor="luiz", data="2026-04-25", titulo_google=None,
        resumo="A Sexta Turma do STJ exigiu perícia técnica e relaxou a preventiva fundada em prints de WhatsApp juntados sem extração forense. O que o caso ensina à defesa."),
    "publicacao-re-635659-ed-segundos-cannabis": dict(
        # [CONFIRMAR] a lista tem 2025-02-01, anterior ao próprio julgamento (7 a 14/02/2025);
        # 2026-05-19 é o dia em que a página entrou no site (histórico do git).
        autor="karla", data="2026-05-19", titulo_google="Tema 506 e cannabis: embargos no STF",
        resumo="RE 635.659 ED-Segundos: o STF rejeitou os embargos no Tema 506 e esclareceu cinco pontos sobre porte de cannabis para uso pessoal, ônus da prova e sanções."),
    "publicacao-rif-coaf-re-1537165-sp": dict(
        autor="luiz", data="2026-04-30", titulo_google="RIF do COAF: os requisitos do STF",
        resumo="RE 1.537.165/SP: liminar do STF fixa sete requisitos cumulativos para o COAF fornecer Relatórios de Inteligência Financeira, com eficácia ex nunc."),
    "publicacao-tema-1354-e-a-progressao-por-condenacao": dict(
        autor="luiz", data="2026-10-03", titulo_google="Tema 1354 e a progressão de regime",
        resumo="Tema 1.354 do STJ: com mais de uma condenação na mesma execução, a progressão de regime é calculada pena por pena, com a lei mais favorável a cada uma."),
    "publicacao-tema-1374-e-a-progressao-especial": dict(
        autor="luiz", data="2026-10-03", titulo_google=None,
        resumo="Tema 1.374 do STJ: a gestante, mãe ou responsável por criança ou pessoa com deficiência condenada por associação para o tráfico progride com 1/8 da pena."),
    "publicacao-tema-931-resp-2090454-sp": dict(
        autor="anderson", data="2026-05-06", titulo_google="Tema 931: pobreza e pena de multa",
        resumo="REsp 2.090.454/SP: o STJ revisou o Tema 931. A multa não paga não impede extinguir a punibilidade quando alegada a pobreza, presumida pela autodeclaração."),
}

RE_FICHA = re.compile(r'\n?[ \t]*<script type="application/ld\+json">(?:(?!</script>).)*"@type": "Article"(?:(?!</script>).)*</script>', re.S)
RE_SECAO = re.compile(r'<div class="post-section-label">(.*?)</div>', re.S)


def texto(s: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", s)).split())


def meta(s: str, chave: str, valor: str) -> str:
    """Troca o content de <meta name|property="chave">, mantendo o resto da etiqueta."""
    padrao = re.compile(r'(<meta (?:name|property)="' + re.escape(chave) + r'" content=")[^"]*(")')
    return padrao.sub(lambda m: m.group(1) + valor + m.group(2), s, count=1)


def ajustar(slug: str, cfg: dict) -> tuple:
    arq = P.PUB / f"{slug}.html"
    s = original = arq.read_text(encoding="utf-8")
    feito = []

    if cfg["titulo_google"]:
        titulo = P.attr(cfg["titulo_google"]) + P.SUFIXO_TITULO
        s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{titulo}</title>", s, count=1, flags=re.S)
        feito.append("título")

    if cfg["resumo"]:
        assert len(cfg["resumo"]) <= P.LIMITE_RESUMO, f"{slug}: resumo com {len(cfg['resumo'])}"
        for chave in ("description", "og:description", "twitter:description"):
            s = meta(s, chave, P.attr(cfg["resumo"]))
        feito.append("resumo")
    resumo = texto(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))

    if 'property="article:published_time"' not in s:
        canonical = re.search(r'[ \t]*<link rel="canonical"[^>]*>\n', s)
        s = s[:canonical.end()] + f'<meta property="article:published_time" content="{cfg["data"]}">\n' + s[canonical.end():]
        feito.append("data")

    s, n = RE_SECAO.subn(r'<h2 class="post-section-label">\1</h2>', s)
    if n:
        feito.append(f"{n} intertítulos h2")

    url = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    imagem = re.search(r'<meta property="og:image" content="([^"]+)"', s).group(1)
    titulo_h1 = texto(re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1))
    ficha = P.ficha_artigo(titulo_h1, resumo, url, cfg["data"], cfg["autor"], imagem)
    s = RE_FICHA.sub("", s)
    s = s.replace("</head>", ficha + "\n</head>", 1)
    feito.append("ficha de artigo")

    return arq, original, s, feito


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-conferir", action="store_true", help="mostra o que mudaria, sem gravar")
    a = ap.parse_args()
    existentes = {p.stem for p in P.PUB.glob("publicacao-*.html")}
    faltam = existentes - PUBLICACOES.keys()
    if faltam:
        print("publicações fora da tabela (não mexi):", ", ".join(sorted(faltam)))
    for slug, cfg in PUBLICACOES.items():
        arq, antes, depois, feito = ajustar(slug, cfg)
        if antes != depois and not a.so_conferir:
            arq.write_text(depois, encoding="utf-8", newline="\n")
        print(f"{'(conferência) ' if a.so_conferir else ''}{slug}: {', '.join(feito)}"
              f"{'' if antes != depois else ' — já estava em dia'}")


if __name__ == "__main__":
    main()
