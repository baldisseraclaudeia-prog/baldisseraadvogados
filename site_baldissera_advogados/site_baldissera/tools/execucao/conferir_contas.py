"""
Conferência independente das contas e da paridade do conteúdo da página "Revisão da execução penal, por fases"
(v3, 09/10/2026). Os produtos da v2 (guia, estudo e Word) saíram do site; se voltarem, são conferidos também.

Duas verificações, separadas da aprovação jurídica (que é do especialista):
  1. ARITMÉTICA: cada exemplo é recalculado aqui a partir das premissas declaradas, sem ler o texto,
     e o resultado esperado tem de aparecer no texto renderizado de cada produto onde o exemplo está.
  2. PARIDADE: frases-núcleo (tese, premissas do exemplo, limites do serviço, aviso) têm de ser idênticas
     em todos os produtos que as contêm.

Uso: ~/.local/bin/python3.12 tools/execucao/conferir_contas.py    (sai com código 1 se qualquer item falhar)
Convenção didática: meses de 30 dias para frações de ano; datas contadas em meses inteiros a partir do dia 1.
"""
import re
import sys
import zipfile
from fractions import Fraction as F
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PUBLIC = AQUI.parents[1] / "public"
PAGINA = PUBLIC / "execucao-penal-revisao-por-fases.html"
GUIA = PUBLIC / "assets" / "docs" / "guia-revisao-execucao-penal.pdf"
ESTUDO = PUBLIC / "assets" / "docs" / "estudo-revisao-execucao-penal.pdf"
WORD = PUBLIC / "assets" / "docs" / "estudo-revisao-execucao-penal.docx"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
NOMES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


# ------------------------------------------------------------------ utilitários de conta
def anos_para_amd(anos: F) -> tuple:
    """Fração de anos → (anos, meses, dias) com mês de 30 dias (convenção didática declarada)."""
    meses_tot = anos * 12
    a, m = divmod(int(meses_tot), 12)
    dias = (meses_tot - int(meses_tot)) * 30
    assert dias.denominator == 1, f"dias não inteiros: {dias}"
    return a, m, int(dias)


def amd_txt(a: int, m: int, d: int) -> str:
    partes = []
    if a:
        partes.append(f"{a} ano" + ("s" if a > 1 else ""))
    if m:
        partes.append(f"{m} " + ("mês" if m == 1 else "meses"))
    if d:
        partes.append(f"{d} dia" + ("s" if d > 1 else ""))
    return partes[0] if len(partes) == 1 else (", ".join(partes[:-1]) + " e " + partes[-1])


def soma_meses(mes: int, ano: int, n: int) -> tuple:
    t = ano * 12 + (mes - 1) + n
    return t % 12 + 1, t // 12


def abrev(mes: int, ano: int) -> str:
    return f"{MESES[mes - 1]}/{ano}"


def extenso(mes: int, ano: int) -> str:
    return f"{NOMES[mes - 1]} de {ano}"


# ------------------------------------------------------------------ casos (premissas → esperado)
def casos():
    c = []
    # Cascata da página/guia/estudo: pena 96 meses; início real mai/2021; lançado jan/2022; 1/6, 1/6 sobre saldo, 1/3.
    p1 = F(96, 6)                      # 16 meses
    p2 = F(96 - 16, 6)                 # 13 meses e 10 dias
    lv = F(96, 3)                      # 32 meses
    assert p1 == 16 and lv == 32 and p2 == F(40, 3)
    real, lanc = (5, 2021), (1, 2022)
    def etapa(inicio, meses_int):
        return abrev(*soma_meses(inicio[0], inicio[1], meses_int))
    r1, l1 = etapa(real, 16), etapa(lanc, 16)
    r2 = abrev(*soma_meses(*soma_meses(real[0], real[1], 16), 13))   # +13 meses (+10 dias no mesmo mês)
    l2 = abrev(*soma_meses(*soma_meses(lanc[0], lanc[1], 16), 13))
    rl, ll = etapa(real, 32), etapa(lanc, 32)
    rf, lf = etapa(real, 96), etapa(lanc, 96)
    c.append(("cascata", ["pagina", "guia", "estudo", "word"],
              [r1, l1, r2, l2, rl, ll, rf, lf, "8 meses"]))
    assert (r1, l1, r2, l2, rl, ll, rf, lf) == ("set/2022", "mai/2023", "out/2023", "jun/2024", "jan/2024", "set/2024", "mai/2029", "jan/2030")

    est = ["estudo", "word"]
    c.append(("E-02", est, ["2 meses", "4 meses"]))
    assert F(1, 6) * 12 == 2 and F(1, 3) * 12 == 4
    c.append(("E-04", est, [amd_txt(*anos_para_amd(F(5, 6))), amd_txt(*anos_para_amd(F(5, 3))),
                            amd_txt(*anos_para_amd(F(2) - F(5, 6))), amd_txt(*anos_para_amd(F(10, 3) - F(5, 3)))]))
    c.append(("E-05", est, ["maio de 2021", "maio de 2023", "janeiro de 2028", "janeiro de 2030"]))
    assert extenso(*soma_meses(1, 2020, 16)) == "maio de 2021" and extenso(*soma_meses(1, 2022, 16)) == "maio de 2023"
    c.append(("E-06", est, [extenso(*soma_meses(1, 2020, 32)), extenso(*soma_meses(1, 2022, 24)), "1 ano e 4 meses"]))
    c.append(("E-11", est, [amd_txt(*anos_para_amd(F(6) * F(20, 100))), amd_txt(*anos_para_amd(F(6) * F(20, 100) - 1))]))
    c.append(("E-12", est, [amd_txt(*anos_para_amd(F(8) * F(40, 100))),
                            amd_txt(*anos_para_amd(F(8) * F(40, 100) - F(8, 6))), amd_txt(*anos_para_amd(F(16, 3)))]))
    unif = F(2) * F(6, 5)
    c.append(("E-13", est, [amd_txt(*anos_para_amd(unif)), amd_txt(*anos_para_amd(6 - unif))]))
    c.append(("E-14", est, [extenso(*soma_meses(1, 2022, 18)), extenso(*soma_meses(1, 2023, 16)), "10 meses"]))
    c.append(("E-16", est, [str(54 - 8) + " meses", "3.600 horas", "150 dias"]))
    assert 300 * 12 == 3600 and 3600 // 24 == 150
    c.append(("E-17", est, ["4 dias", "120 dias"]))
    c.append(("E-19", est, [amd_txt(*anos_para_amd(F(10, 6))), "4 meses"]))
    c.append(("E-20", est, [extenso(*soma_meses(1, 2022, 36)), amd_txt(*anos_para_amd(F(7, 3))),
                            extenso(*soma_meses(1, 2024, 28)), "1 ano e 4 meses"]))
    c.append(("E-22", est, ["40 dias", "12 dias", "28 dias"]))
    c.append(("E-26", est, [amd_txt(*anos_para_amd(F(4) * F(4, 3)))]))
    c.append(("E-40", est, [amd_txt(*anos_para_amd(F(2) * F(4, 3)))]))
    c.append(("H-5", est, [extenso(*soma_meses(1, 2023, 16)), extenso(*soma_meses(1, 2022, 18)), "10 meses"]))
    c.append(("H-6", est, [amd_txt(*anos_para_amd(unif)), amd_txt(*anos_para_amd(6 - unif))]))
    return c


# ------------------------------------------------------------------ paridade (frases-núcleo)
PARIDADE = [
    ("tese", ["pagina", "guia", "estudo", "word"], "Um erro no cálculo da pena pode repercutir em outros marcos da execução"),
    ("premissa-cascata", ["pagina", "guia", "estudo", "word"], "lançada no cálculo como janeiro de 2022"),
    ("limite-servico", ["pagina", "guia", "estudo", "word"], "Pode concluir que o cálculo está correto ou que não há providência cabível"),
    ("ressalva-cnj", ["pagina"], "em parte dos casos, o direito já estava implementado e apenas não fora lançado no sistema"),
    ("cascata-dias", ["pagina"], "cada data fica oito meses adiante. São efeitos do mesmo período não computado"),
    ("fases-limite", ["pagina"], "Pedidos e recursos são atuação distinta, que não integra as fases"),
]


# ------------------------------------------------------------------ leitura dos produtos
def texto_pdf(p: Path) -> str:
    import fitz
    return "\n".join(pg.get_text() for pg in fitz.open(p))


def texto_html(p: Path) -> str:
    import html
    h = p.read_text(encoding="utf-8")
    h = h[h.find("<main"):h.find("</main>")]
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    return html.unescape(re.sub(r"<[^>]+>", " ", h))


def texto_docx(p: Path) -> str:
    with zipfile.ZipFile(p) as z:
        x = z.read("word/document.xml").decode("utf-8")
    x = re.sub(r"</w:p>", "\n", x)
    return re.sub(r"<[^>]+>", "", x)


def normal(t: str) -> str:
    t = t.replace("­", "").replace(" ", " ")
    t = re.sub(r"-\n", "", t)            # hifenização de fim de linha no PDF
    return re.sub(r"\s+", " ", t)


def main() -> int:
    fontes = {"pagina": (PAGINA, texto_html), "guia": (GUIA, texto_pdf), "estudo": (ESTUDO, texto_pdf), "word": (WORD, texto_docx)}
    textos = {k: normal(f(p)) for k, (p, f) in fontes.items() if p.exists()}
    faltam = [k for k in fontes if k not in textos]
    if "pagina" not in textos:
        print(f"FALHA: página não encontrada ({PAGINA.name}); gere antes com tools/gerar_revisao_execucao.py")
        return 1
    falhas = 0
    for nome, onde, esperados in casos():
        for prod in onde:
            if prod not in textos:
                continue
            for e in esperados:
                if e not in textos[prod]:
                    print(f"FALHA conta {nome} · {prod}: não encontrado «{e}»")
                    falhas += 1
    for nome, onde, frase in PARIDADE:
        for prod in onde:
            if prod in textos and frase not in textos[prod]:
                print(f"FALHA paridade {nome} · {prod}: ausente «{frase}»")
                falhas += 1
    proibidas = ["mais comum", "mais comuns", "mais frequente", "mais frequentes", "nunca seja surpreendida", "revisão séria",
                 "modo de cômputo", "se repete a cada etapa", "garantimos", "garantia de"]
    for prod, t in textos.items():
        for p in proibidas:
            if p in t.lower():
                print(f"FALHA vedada · {prod}: «{p}»")
                falhas += 1
    print(f"produtos lidos: {', '.join(textos)}" + (f" · ausentes: {', '.join(faltam)}" if faltam else ""))
    print("OK — contas, paridade e vedações conferidas" if not falhas else f"{falhas} falha(s)")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
