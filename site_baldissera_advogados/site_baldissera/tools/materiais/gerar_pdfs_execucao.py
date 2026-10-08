"""
Gera os dois PDFs da página "Revisão completa da execução penal" (08/10/2026):
  public/assets/docs/guia-revisao-execucao-penal.pdf   — versão objetiva, para enviar a quem pergunta
  public/assets/docs/estudo-revisao-execucao-penal.pdf — versão aprofundada

Conteúdo comum vem de tools/gerar_revisao_execucao.py (mesma fonte da página); o catálogo de 41 erros, as histórias e o
glossário vêm de CATALOGO (JSON público, fora do git) e só levam a base legal que consta de BASES_JSON
(artigos e súmulas conferidos no portal oficial — ficha E). Nunca editar o PDF: corrige-se aqui e gera-se de novo.

Uso: python tools/materiais/gerar_pdfs_execucao.py   (precisa do Google Chrome; usa a internet para as fontes)
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import gerar_revisao_execucao as P  # noqa: E402

PUBLIC = AQUI.parents[1] / "public"
MARCA = PUBLIC / "assets" / "images" / "marca"
PESQUISA = Path.home() / ".claude" / "plans" / "site-execucao-penal" / "pesquisa"
CATALOGO = PESQUISA / "F-catalogo-publico.json"
BASES_JSON = PESQUISA / "E-bases-conferidas.json"   # lista das bases conferidas (ficha E)
COPIA_ONEDRIVE = (Path.home() / "Library/CloudStorage/OneDrive-Pessoal/Área de Trabalho/SITE BALDISSERA ADVOGADOS"
                  / "MATERIAIS" / "execucao-penal")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DATA = "Outubro de 2026"
RODAPE = "Cascavel/PR · Porto Alegre/RS · Foz do Iguaçu/PR · www.baldisseraadvogados.com.br"

esc = P.esc


def svg(nome: str, classe: str) -> str:
    s = (MARCA / nome).read_text(encoding="utf-8")
    s = s[s.index("<svg"):]
    return s.replace("<svg ", f'<svg class="{classe}" role="img" aria-label="Baldissera Advogados" ', 1)


CSS = """
@import url('""" + P.molde.FONTES + """');
:root { --toga:#0F172A; --papel:#F7F3EA; --papel-2:#EEE7D7; --ouro:#9B7B3A; --ouro-texto:#806328; --tinta:#1E222B; --tinta-2:#4A4F5A; --linha:#D6CCB6; }
@page { size: A4; margin: 20mm 19mm 22mm;
  @bottom-left { content: '""" + RODAPE + """'; font: 7.5pt 'Source Serif 4', Georgia, serif; color: #4A4F5A; }
  @bottom-right { content: counter(page); font: 8pt 'Source Serif 4', Georgia, serif; color: #806328; }
  @top-right { content: '__CABECALHO__'; font: 7.5pt 'Source Serif 4', Georgia, serif; color: #806328; font-variant-caps: all-small-caps; letter-spacing: .08em; }
}
@page capa { margin: 0; @bottom-left { content: none } @bottom-right { content: none } @top-right { content: none } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 10.2pt/1.55 'Source Serif 4', Georgia, serif; color: var(--tinta); font-variant-numeric: lining-nums; hyphens: auto; }
h1, h2, h3, h4 { font-family: 'EB Garamond', Garamond, serif; color: var(--toga); font-weight: 500; break-after: avoid; }
p { margin: 0 0 .55em; text-align: justify; orphans: 3; widows: 3; }
strong { font-weight: 600; color: var(--toga); }
a { color: inherit; text-decoration-color: var(--ouro); }

.capa { page: capa; height: 297mm; width: 210mm; background: var(--toga); color: #F5F1E8; position: relative; padding: 30mm 24mm; break-after: page; }
.capa::before { content: ""; position: absolute; left: 24mm; right: 24mm; top: 18mm; border-top: 4px double #9B7B3A; }
.capa::after { content: ""; position: absolute; left: 24mm; right: 24mm; bottom: 18mm; border-top: 4px double #9B7B3A; }
.capa .marca { width: 92mm; height: auto; display: block; margin: 6mm 0 0 -3mm; }
.capa .sobre { margin-top: 52mm; font-size: 10pt; color: #C9B98A; font-variant-caps: all-small-caps; letter-spacing: .14em; }
.capa h1 { font-size: 40pt; line-height: 1.04; color: #F5F1E8; margin: 4mm 0 0; max-width: 140mm; }
.capa .sub { font: italic 15pt/1.4 'EB Garamond', serif; color: #E7E1D2; margin-top: 8mm; max-width: 135mm; text-align: left; }
.capa .rodape { position: absolute; left: 24mm; right: 24mm; bottom: 26mm; font-size: 9pt; color: #C9C3B4; display: flex; justify-content: space-between; }

.cab { display: flex; align-items: flex-end; justify-content: space-between; border-bottom: 4px double var(--ouro); padding-bottom: 3mm; margin-bottom: 7mm; }
.cab .marca { width: 46mm; height: auto; }
.cab span { font-size: 8pt; color: var(--ouro-texto); font-variant-caps: all-small-caps; letter-spacing: .1em; }

h2.cap { font-size: 22pt; line-height: 1.1; margin: 0 0 4mm; padding-top: 2mm; }
h2.cap .num { display: block; font-size: 13pt; color: var(--ouro); margin-bottom: 1mm; }
h3 { font-size: 13.5pt; line-height: 1.2; margin: 5mm 0 1.5mm; }
.nova { break-before: page; }
.lead { font: italic 12.5pt/1.45 'EB Garamond', serif; color: var(--toga); border-left: 2px solid var(--ouro); padding-left: 4mm; margin: 0 0 5mm; text-align: left; }
.recuo p { text-indent: 1.27cm; }
.recuo p.abre { text-indent: 0; }

.numeros { display: grid; grid-template-columns: repeat(3, 1fr); border-top: 4px double var(--ouro); border-bottom: 1px solid var(--linha); margin: 5mm 0; break-inside: avoid; }
.numeros div { padding: 4mm 3mm; border-left: 1px solid var(--linha); text-align: center; }
.numeros div:first-child { border-left: 0; }
.numeros b { display: block; font: 500 24pt/1 'EB Garamond', serif; color: var(--toga); }
.numeros span { display: block; font-size: 8.4pt; line-height: 1.4; margin-top: 2mm; }
.numeros small { display: block; font-size: 7pt; color: var(--tinta-2); margin-top: 1.5mm; line-height: 1.35; }

.caixa { background: var(--papel-2); border-left: 3px solid var(--ouro); padding: 3.5mm 4.5mm; margin: 4mm 0; break-inside: avoid; }
.caixa .rot { font-size: 8pt; color: var(--ouro-texto); font-variant-caps: all-small-caps; letter-spacing: .1em; margin: 0 0 1mm; }
.caixa h3 { margin-top: 0; }
.caixa p { font-size: 9.6pt; }

ol.passos { list-style: none; counter-reset: p; padding: 0; margin: 3mm 0; }
ol.passos li { counter-increment: p; position: relative; padding: 0 0 2.5mm 11mm; break-inside: avoid; }
ol.passos li::before { content: counter(p, upper-roman); position: absolute; left: 0; top: 0; width: 7mm; height: 7mm; background: var(--toga); color: #F5F1E8; font: 500 9pt/7mm 'EB Garamond', serif; text-align: center; }
ol.passos h4 { font-size: 11.5pt; margin: 0 0 .5mm; }
ol.passos p { font-size: 9.4pt; margin: 0; color: var(--tinta-2); }

table { width: 100%; border-collapse: collapse; font-size: 9pt; margin: 3mm 0 4mm; break-inside: auto; }
th, td { text-align: left; vertical-align: top; padding: 1.8mm 2mm; border-bottom: 1px solid var(--linha); }
thead th { border-bottom: 1.5px solid var(--toga); color: var(--toga); font-weight: 600; }
tr { break-inside: avoid; }
td.n { white-space: nowrap; font-weight: 600; color: var(--toga); }
caption { caption-side: top; text-align: left; font-size: 8pt; color: var(--ouro-texto); font-variant-caps: all-small-caps; letter-spacing: .1em; padding-bottom: 1.5mm; }
.nota { font-size: 8pt; color: var(--tinta-2); }

.erro { border-top: 1px solid var(--linha); padding: 3mm 0 2mm; break-inside: avoid; }
.erro h4 { font-size: 12pt; margin: 0 0 1mm; }
.erro h4 .id { color: var(--ouro); margin-right: 2mm; }
.erro p { font-size: 9.3pt; margin: 0 0 1mm; }
.erro .r { font-variant-caps: all-small-caps; letter-spacing: .08em; color: var(--ouro-texto); margin-right: 1mm; }
.erro .base { font-size: 8.2pt; color: var(--tinta-2); }

.check { columns: 2; column-gap: 8mm; list-style: none; padding: 0; margin: 3mm 0; }
.check li { break-inside: avoid; padding: 1.4mm 0 1.4mm 6mm; position: relative; font-size: 9.4pt; border-bottom: 1px solid var(--linha); }
.check li::before { content: ""; position: absolute; left: 0; top: 2.6mm; width: 3mm; height: 3mm; border: 1px solid var(--toga); }

.julgado { margin: 4mm 0 6mm; }
.julgado .trib { font-size: 8pt; color: var(--ouro-texto); font-variant-caps: all-small-caps; letter-spacing: .1em; margin: 0; }
.julgado h3 { margin-top: 1mm; }
.julgado blockquote { margin: 2mm 0; padding: 3mm 4mm; background: var(--papel-2); border-left: 3px solid var(--ouro); font-style: italic; font-size: 9.2pt; line-height: 1.5; text-align: justify; }
.julgado blockquote strong { font-style: italic; }
.julgado .ref { display: block; font-style: normal; font-size: 8pt; color: var(--tinta-2); margin-top: 2mm; }

dl.glos { margin: 0; }
dl.glos dt { font: 600 10.5pt 'EB Garamond', serif; color: var(--toga); margin-top: 2mm; break-after: avoid; }
dl.glos dd { margin: 0 0 1mm; font-size: 9.3pt; }

.fecho { border-top: 4px double var(--ouro); margin-top: 8mm; padding-top: 4mm; font-size: 8.6pt; color: var(--tinta-2); break-inside: avoid; }
.fecho p { text-align: left; }
.assina { margin: 3mm 0; }
.assina b { font: 600 12pt 'EB Garamond', serif; color: var(--toga); display: block; }
.sumario-pdf { list-style: none; padding: 0; margin: 4mm 0; }
.sumario-pdf li { display: flex; gap: 3mm; padding: 1.6mm 0; border-bottom: 1px dotted var(--linha); font-size: 10.5pt; }
.sumario-pdf li span:first-child { color: var(--ouro); min-width: 10mm; font-family: 'EB Garamond', serif; }
svg.rv-grafico { width: 100%; height: auto; margin: 2mm 0; }
.rv-grafico .g-fio { stroke: #D6CCB6; stroke-width: 1; }
.rv-grafico .g-oficial { fill: #B9AE95; } .rv-grafico .g-revisto { fill: #0F172A; } .rv-grafico .g-ganho { fill: #9B7B3A; }
.rv-grafico text { font-family: 'Source Serif 4', serif; font-size: 13px; fill: #1E222B; }
.rv-grafico .g-rotulo { font-size: 12px; fill: #4A4F5A; } .rv-grafico .g-titulo { font-family: 'EB Garamond', serif; font-size: 16px; fill: #0F172A; }
"""


def documento(titulo_aba: str, cabecalho: str, corpo: str) -> str:
    css = CSS.replace("__CABECALHO__", cabecalho)
    return (f'<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><title>{esc(titulo_aba)}</title>'
            f"<style>{css}</style></head><body>{corpo}</body></html>")


def capa(sobre: str, titulo: str, sub: str) -> str:
    return f'''<section class="capa">
  {svg("baldissera-advogados-escuro.svg", "marca")}
  <p class="sobre">{esc(sobre)}</p>
  <h1>{esc(titulo)}</h1>
  <p class="sub">{esc(sub)}</p>
  <div class="rodape"><span>Baldissera Advogados · Sociedade de Advogados · OAB/PR 4.545</span><span>{DATA}</span></div>
</section>'''


def cab(rotulo: str) -> str:
    return f'<div class="cab">{svg("baldissera-advogados-principal.svg", "marca")}<span>{esc(rotulo)}</span></div>'


def numeros() -> str:
    return '<div class="numeros">' + "".join(
        f"<div><b>{n}</b><span>{esc(r)}</span><small>{esc(f)}</small></div>" for n, r, f, _u in P.NUMEROS) + "</div>"


def quadro() -> str:
    linhas = "".join(f"<tr><td>{esc(n)}</td><td>{r}</td><td>{l}</td><td class='n'>8 meses</td></tr>" for n, r, l in P.QUADRO)
    return (f"<table><caption>Exemplo hipotético · frações ilustrativas</caption><thead><tr><th>Etapa</th><th>Data revista</th>"
            f"<th>Data lançada</th><th>Atraso</th></tr></thead><tbody>{linhas}</tbody></table>"
            "<p class='nota'>Pena de 8 anos; prisão preventiva iniciada em maio de 2021 e lançada como janeiro de 2022. Um sexto para "
            "cada progressão (a segunda sobre o saldo) e um terço para o livramento, frações usadas apenas para ilustrar. Em caso real, "
            "a fração depende da data do fato, da natureza do crime e da reincidência.</p>")


def fecho() -> str:
    return f'''<div class="fecho">
  <div class="assina"><b>Luiz Henrique Baldissera</b>Advogado criminalista · OAB/PR 55.717 · OAB/SC 78.938-A · Responsável técnico</div>
  <p>Baldissera Advogados · Sociedade de Advogados · OAB/PR 4.545 · CNPJ 24.129.499/0001-08<br>
  {RODAPE}<br>contato@baldisseraadvogados.com.br · +55 45 99102-9806</p>
  <p>Material informativo, nos termos do Provimento CFOAB 205/2021 e do Código de Ética e Disciplina da OAB. Os exemplos são hipotéticos,
  com frações ilustrativas, e não se referem a casos do escritório. O resultado de cada execução depende dos documentos e das
  circunstâncias do caso. Dados oficiais com fonte e página indicadas, consultados em 8 de outubro de 2026.</p>
</div>'''


# ------------------------------------------------------------------ GUIA (objetivo)
def guia() -> str:
    c = [capa("Guia objetivo", "Revisão da execução penal",
              "O que é, por que importa, o que se confere e como começar.")]
    c.append(cab("Revisão da execução penal · guia objetivo"))
    c.append('<h2 class="cap"><span class="num">I</span>Em uma página</h2>')
    c.append('<p class="lead">Na execução penal, um erro raramente é um só: uma data errada hoje é o atraso de cada benefício que vem depois.</p>')
    c.append('<div class="recuo">'
             '<p class="abre">A pena fixada na sentença atravessa anos de cálculos, lançamentos e decisões. Passa da sentença para a guia de '
             'recolhimento, da guia para o sistema eletrônico, e é atualizada a cada remição, falta, decreto ou nova condenação. Cada '
             'passagem é um ponto em que um número pode ser digitado errado, uma decisão pode não chegar ao cálculo, um período pode ficar de fora.</p>'
             '<p>A revisão completa refaz a execução desde o início: lê todas as folhas, monta a linha do tempo, recalcula cada benefício '
             'com a conta exposta e confronta o resultado com o cálculo oficial. Quando há divergência, ela é demonstrada com o documento que a '
             'sustenta e levada ao juízo da execução na forma e na ordem adequadas.</p></div>')
    c.append(numeros())
    c.append('<p class="nota">O próprio Conselho Nacional de Justiça ressalva que parte dos casos de benefício vencido corresponde a atraso de '
             'lançamento no sistema, e não à perda de um direito. Em ambas as situações, é a conferência que distingue uma da outra.</p>')
    c.append('<h2 class="cap nova"><span class="num">II</span>Por que os erros acontecem</h2>')
    c.append('<ol class="passos">'
             '<li><h4>Muitas mãos</h4><p>Sentença, guia, cartório, sistema eletrônico, unidade prisional e juízo: cada um alimenta uma parte da conta.</p></li>'
             '<li><h4>A lei muda</h4><p>As frações para a progressão foram reescritas mais de uma vez nos últimos anos, e cada condenação segue a lei da data do fato.</p></li>'
             '<li><h4>Juntar não é lançar</h4><p>O sistema calcula o que recebe. A decisão juntada aos autos só produz efeito quando o dado é lançado no campo certo.</p></li>'
             '<li><h4>Os benefícios são encadeados</h4><p>Cada etapa é contada a partir da anterior. Por isso o erro se propaga.</p></li></ol>')
    c.append('<h3>O efeito cascata, em um exemplo</h3>')
    c.append(P.grafico_svg())
    c.append(quadro())
    c.append('<h2 class="cap nova"><span class="num">III</span>Os doze erros mais frequentes</h2>')
    c.append("<table><thead><tr><th>Erro</th><th>Efeito</th></tr></thead><tbody>" + "".join(
        f"<tr><td><strong>{esc(t)}</strong></td><td>{esc(e[0].upper() + e[1:])}</td></tr>" for t, _c, e, _b in P.ERROS) + "</tbody></table>")
    c.append('<h2 class="cap nova"><span class="num">IV</span>O que a revisão confere</h2>')
    c.append("<table><thead><tr><th>Capítulo</th><th>Em resumo</th></tr></thead><tbody>" + "".join(
        f"<tr><td class='n'>{i}. {esc(t)}</td><td>{esc(intro)}</td></tr>" for i, (t, intro, _x) in enumerate(P.CAPITULOS, 1)) + "</tbody></table>")
    c.append('<h3>Como o trabalho é feito</h3><ol class="passos">' + "".join(
        f"<li><h4>{esc(t)}</h4><p>{esc(p)}</p></li>" for t, p in P.METODO) + "</ol>")
    c.append('<h2 class="cap"><span class="num">V</span>O que o cliente recebe</h2>')
    c.append('<ul class="check">' + "".join(f"<li><strong>{esc(a)}</strong>: {esc(b)}</li>" for a, b in P.ENTREGA) + "</ul>")
    c.append('<h3>Documentos para começar</h3><ul class="check">' + "".join(
        f"<li><strong>{esc(a)}</strong>, {esc(b)}</li>" for a, b in P.DOCUMENTOS) + "</ul>")
    c.append('<p class="nota">Não é preciso reunir tudo de início: com a procuração, o advogado tem acesso aos autos eletrônicos da execução; '
             'os documentos da família servem para completar o que não estiver lá.</p>')
    c.append('<h3>Perguntas frequentes</h3>' + "".join(f"<p><strong>{esc(q)}</strong> {esc(r)}</p>" for q, r in P.FAQ[:4]))
    c.append('<p class="nota">O estudo completo, com o catálogo de mais de quarenta erros, os exemplos com a conta e os precedentes, está em '
             'www.baldisseraadvogados.com.br/execucao-penal-revisao-completa.</p>')
    c.append(fecho())
    return documento("Guia — Revisão da execução penal", "Guia objetivo", "\n".join(c))


# ------------------------------------------------------------------ ESTUDO (aprofundado)
JULG_PDF_EXTRA = [
    {"trib": "STJ · Tema Repetitivo 1.084",
     "tese": "Reincidente apenas genérico em crime hediondo progride com a fração do primário",
     "ponte": "A lei de 2019 não previu fração para quem cometeu crime hediondo sem ser reincidente em crime da mesma natureza. "
              "Vedada a analogia contra o réu, aplica-se a fração do primário. O erro aparece quando o cadastro marca apenas "
              "\"reincidente\", sem distinguir a espécie. As frações do art. 112 foram novamente alteradas em 2026; a conta segue a "
              "lei de cada fato.",
     "integral_html": "RECURSO ESPECIAL REPRESENTATIVO DE CONTROVÉRSIA. EXECUÇÃO PENAL. PROGRESSÃO DE REGIME. ALTERAÇÕES PROMOVIDAS PELA LEI "
                      "N. 13.964/2019 (PACOTE ANTICRIME). DIFERENCIAÇÃO ENTRE REINCIDÊNCIA GENÉRICA E ESPECÍFICA. AUSÊNCIA DE PREVISÃO DOS "
                      "LAPSOS RELATIVOS AOS REINCIDENTES GENÉRICOS. LACUNA LEGAL. INTEGRAÇÃO DA NORMA. APLICAÇÃO DOS PATAMARES PREVISTOS PARA "
                      "OS APENADOS PRIMÁRIOS. RETROATIVIDADE DA LEI PENAL MAIS BENÉFICA. PATAMAR HODIERNO INFERIOR À FRAÇÃO ANTERIORMENTE "
                      "EXIGIDA AOS REINCIDENTES GENÉRICOS. RECURSO NÃO PROVIDO. 1. A Lei n. 13.964/2019, intitulada Pacote Anticrime, "
                      "promoveu profundas alterações no marco normativo referente aos lapsos exigidos para o alcance da progressão a regime "
                      "menos gravoso, tendo sido expressamente revogadas as disposições do art. 2º, § 2º, da Lei n. 8.072/1990 e "
                      "estabelecidos patamares calcados não apenas na natureza do delito, mas também no caráter da reincidência, seja ela "
                      "genérica ou específica. 2. Evidenciada a ausência de previsão dos parâmetros relativos aos apenados condenados por "
                      "crime hediondo ou equiparado, mas reincidentes genéricos, impõe-se ao Juízo da execução penal a integração da norma "
                      "sob análise, de modo que, <strong>dado o óbice à analogia in malam partem, é imperiosa a aplicação aos reincidentes "
                      "genéricos dos lapsos de progressão referentes aos sentenciados primários</strong>. 3. Ainda que provavelmente não "
                      "tenha sido essa a intenção do legislador, é irrefutável que de lege lata, a incidência retroativa do art. 112, V, da "
                      "Lei n. 7.210/1984, quanto à hipótese da lacuna legal relativa aos apenados condenados por crime hediondo ou "
                      "equiparado e reincidentes genéricos, instituiu conjuntura mais favorável que o anterior lapso de 3/5, a permitir, "
                      "então, a retroatividade da lei penal mais benigna. 4. Dadas as ponderações acima, a hipótese em análise trata da "
                      "incidência de lei penal mais benéfica ao apenado, condenado por estupro, porém reincidente genérico, de forma que é "
                      "mister o reconhecimento de sua retroatividade, dado que o percentual por ela estabelecido – qual seja, de "
                      "cumprimento de 40% das reprimendas impostas –, é inferior à fração de 3/5, anteriormente exigida para a progressão "
                      "de condenados por crimes hediondos, fossem reincidentes genéricos ou específicos. 5. Recurso especial "
                      "representativo da controvérsia não provido, assentando-se a seguinte tese: <strong>É reconhecida a retroatividade "
                      "do patamar estabelecido no art. 112, V, da Lei n. 13.964/2019, àqueles apenados que, embora tenham cometido crime "
                      "hediondo ou equiparado sem resultado morte, não sejam reincidentes em delito de natureza semelhante.</strong>",
     "ref": "(REsp n. 1.910.240/MG, relator Ministro Rogerio Schietti Cruz, Terceira Seção, julgado em 26/5/2021, DJe de 31/5/2021.)"},
    {"trib": "STF · Súmula Vinculante 56",
     "tese": "A falta de vaga não autoriza manter o condenado em regime mais grave",
     "ponte": "Concedida a progressão, a ausência de vaga no regime adequado não justifica a permanência no regime anterior. "
              "O Superior Tribunal de Justiça acrescenta que a prisão domiciliar não é automática: antes dela vêm as providências "
              "fixadas pelo Supremo para o déficit de vagas.",
     "integral_html": "<strong>A falta de estabelecimento penal adequado não autoriza a manutenção do condenado em regime prisional mais "
                      "gravoso</strong>, devendo-se observar, nessa hipótese, os parâmetros fixados no RE 641.320/RS.",
     "ref": "(Súmula Vinculante 56, Supremo Tribunal Federal, aprovada na sessão plenária de 29/6/2016. Enunciado conferido no portal do STF.)"},
    {"trib": "STJ · Jurisprudência em Teses, edições 7, 144 e 145",
     "tese": "Falta grave prescrita, antiga ou apurada sem defesa técnica não pode travar a execução",
     "ponte": "A falta grave produz efeitos fortes, e por isso a sua validade é a primeira coisa a conferir. A jurisprudência do STJ "
              "fixou prazo para a apuração, impede que faltas antigas e reabilitadas sirvam de fundamento para negar a progressão "
              "e reconhece a nulidade do procedimento sem advogado na oitiva de testemunhas. Em sentido limitador, o Supremo admite "
              "que a audiência de justificação com defensor e Ministério Público supra o procedimento disciplinar (Tema 941, adiante).",
     "integral_html": "Edição 7, tese 3: <strong>Diante da inexistência de legislação específica quanto ao prazo prescricional para apuração "
                      "de falta grave, deve ser adotado o menor lapso prescricional previsto no art. 109 do CP, ou seja, o de 3 anos.</strong><br>"
                      "Edição 144, tese 1: <strong>Faltas graves cometidas em período longínquo e já reabilitadas não configuram fundamento "
                      "idôneo para indeferir o pedido de progressão de regime</strong>, para que os princípios da razoabilidade e da "
                      "ressocialização da pena e o direito ao esquecimento sejam respeitados.<br>"
                      "Edição 145, tese 2: A decisão que reconhece a prática de falta grave disciplinar deverá ser desconstituída diante das "
                      "hipóteses de arquivamento de inquérito policial ou de posterior absolvição na esfera penal, por inexistência do fato "
                      "ou negativa de autoria, tendo em vista a atipicidade da conduta.<br>"
                      "Edição 145, tese 5: No processo administrativo disciplinar instaurado para apuração de falta grave supostamente "
                      "praticada no curso da execução penal, <strong>a inexistência de defesa técnica por advogado na oitiva de testemunhas "
                      "viola os princípios do contraditório e da ampla defesa e configura causa de nulidade do PAD</strong>.",
     "ref": "(STJ, Jurisprudência em Teses n. 7, Falta Grave em Execução Penal, tese 3; n. 144, Falta Grave em Execução Penal II, tese 1; n. 145, Falta Grave em Execução Penal III, teses 2 e 5.)"},
    {"trib": "STJ · Jurisprudência em Teses, edição 139",
     "tese": "Indulto e comutação: decisão declaratória e data-base preservada",
     "ponte": "Preenchidos os requisitos do decreto, o juiz apenas declara o direito, e nova condenação não altera a data-base desses "
              "benefícios. Por isso decretos antigos continuam aplicáveis e precisam ser examinados um a um.",
     "integral_html": "Tese 2: <strong>A sentença que concede o indulto ou a comutação de pena tem natureza declaratória</strong>, não havendo "
                      "como impedir a concessão dos benefícios ao sentenciado, se cumpridos todos os requisitos exigidos no decreto presidencial.<br>"
                      "Tese 5: <strong>A superveniência de condenação, seja por fato anterior ou posterior ao início do cumprimento da pena, "
                      "não altera a data-base para a concessão da comutação de pena e do indulto.</strong><br>"
                      "Tese 7: Para a concessão de indulto, deve ser considerada a pena originalmente imposta, não sendo levada em conta, "
                      "portanto, a pena remanescente em decorrência de comutações anteriores.",
     "ref": "(STJ, Jurisprudência em Teses n. 139, Do Indulto e da Comutação de Pena, teses 2, 5 e 7.)"},
]

CONTRA = [
    ("STJ · Súmula 534", "A falta grave interrompe a contagem para a progressão",
     "A prática de falta grave interrompe a contagem do prazo para a progressão de regime de cumprimento de pena, o qual se reinicia "
     "a partir do cometimento dessa infração.",
     "(Súmula 534, Terceira Seção, julgada em 10/6/2015, DJe de 15/6/2015.)",
     "A regra pesa contra o condenado, mas fixa a data certa: a do cometimento, não a da homologação. É justamente aí que aparece um dos erros mais comuns."),
    ("STJ · Tema Repetitivo 1.161", "O comportamento para o livramento considera todo o histórico",
     "A valoração do requisito subjetivo para concessão do livramento condicional - bom comportamento durante da execução da pena "
     "(art. 83, inciso III, alínea \"a\", do Código Penal) - deve considerar todo o histórico prisional, não se limitando ao período "
     "de 12 meses referido na alínea \"b\" do mesmo inciso III do art. 83 do Código Penal.",
     "(STJ, Tema Repetitivo 1.161, Terceira Seção, tese firmada conforme o portal de precedentes qualificados.)",
     "A falta grave não reinicia o prazo do livramento, mas continua pesando na avaliação do comportamento."),
    ("STF · Tema 941 de repercussão geral", "A audiência de justificação pode suprir o procedimento disciplinar",
     "A oitiva do condenado pelo Juízo da Execução Penal, em audiência de justificação realizada na presença do defensor e do Ministério "
     "Público, afasta a necessidade de prévio Procedimento Administrativo Disciplinar (PAD), assim como supre eventual ausência ou "
     "insuficiência de defesa técnica no PAD instaurado para apurar a prática de falta grave durante o cumprimento da pena.",
     "(RE n. 972.598/RS, relator Ministro Roberto Barroso, Tribunal Pleno, julgado em 4/5/2020, DJe de 6/8/2020, Tema 941.)",
     "Limita a alegação de nulidade do procedimento disciplinar quando houve audiência judicial com defesa."),
    ("STF · Súmula 715", "O limite de cumprimento não é base para os benefícios",
     "A pena unificada para atender ao limite de trinta anos de cumprimento, determinado pelo art. 75 do Código Penal, não é "
     "considerada para a concessão de outros benefícios, como o livramento condicional ou regime mais favorável de execução.",
     "(Súmula 715, Supremo Tribunal Federal, sessão plenária de 24/9/2003.)",
     "Os benefícios são calculados sobre a pena total, não sobre o limite máximo de cumprimento."),
]

EP102 = {
    "trib": "STF · Tribunal Pleno · EP 102 AgR-segundo",
    "tese": "Em sentido diverso do Tema 1.354: fração mais grave sobre a pena unificada",
    "ponte": "Em execução penal originária, o Plenário do Supremo decidiu, por maioria, que a condenação simultânea por crime comum e por "
             "crime com violência atrai a fração mais grave sobre toda a pena unificada. O caso não tratou da sucessão de leis no tempo, "
             "objeto do Tema 1.354 do STJ, mas a divergência entre as cortes existe e precisa ser considerada em cada cálculo.",
    "integral_html": "Ementa: Direito processual penal. Segundo agravo regimental na execução penal. PROGRESSÃO DE REGIME. UNIFICAÇÃO DE PENAS. "
                     "CONCURSO DE CRIMES COM E SEM VIOLÊNCIA À PESSOA. CÁLCULO DO REQUISITO OBJETIVO. APLICAÇÃO DO PERCENTUAL MAIS GRAVOSO "
                     "SOBRE A TOTALIDADE DA PENA. AGRAVO REGIMENTAL A QUE SE NEGA PROVIMENTO. I. Caso em exame 1. Trata-se de agravo regimental "
                     "interposto contra decisão monocrática que, em sede de execução penal, determinou a retificação do cálculo de pena para "
                     "aplicar o percentual de 25% (vinte e cinco por cento) para fins de progressão de regime, com base no artigo 112, inciso "
                     "III, da Lei de Execução Penal, sobre a totalidade da pena unificada. O agravante, condenado por múltiplos crimes, sustenta "
                     "que o percentual mais gravoso deveria incidir apenas sobre a pena do crime cometido com violência à pessoa, aplicando-se "
                     "o percentual de 16% (dezesseis por cento) aos demais delitos. II. Questão em discussão 2. A controvérsia central consiste "
                     "em definir se, no caso de concurso de crimes e consequente unificação das penas, o requisito objetivo para a progressão "
                     "de regime deve ser calculado de forma isolada para cada delito ou se deve prevalecer o percentual mais rigoroso sobre o "
                     "total da pena unificada, quando uma das condenações for por crime cometido com violência ou grave ameaça à pessoa. "
                     "III. Razões de decidir 3. Em matéria de execução penal, as penas impostas em razão do concurso de crimes são unificadas, "
                     "formando um montante único sobre o qual incidirão as regras para a concessão de benefícios, como a progressão de regime. "
                     "4. A existência de condenação por crime praticado com violência ou grave ameaça à pessoa, conforme previsto no artigo "
                     "112, inciso III, da Lei de Execução Penal, impõe a aplicação do percentual de 25% (vinte e cinco por cento) para a "
                     "progressão. Este requisito mais gravoso se estende sobre a totalidade da pena unificada, sendo inviável a fragmentação "
                     "do cálculo para aplicar percentuais distintos a cada crime. 5. A execução da pena é una e indivisível. A adoção de "
                     "critério diverso, além de não encontrar amparo legal, criaria um sistema de execução complexo e impraticável, "
                     "desvirtuando a finalidade da unificação das penas. IV. Dispositivo e tese 6. Agravo regimental a que se nega provimento. "
                     "Tese de julgamento: \"1. Havendo concurso de crimes, a unificação das penas para fins de execução penal impõe que o "
                     "cálculo do requisito objetivo para a progressão de regime seja realizado sobre a <strong>totalidade da pena "
                     "remanescente</strong>, observando-se o percentual mais gravoso previsto em lei. 2. A condenação simultânea por crimes "
                     "comuns e por crime cometido com violência ou grave ameaça à pessoa (art. 112, III, da Lei de Execução Penal) atrai a "
                     "incidência do percentual de 25% sobre a integralidade da pena unificada, não sendo cabível a aplicação de frações "
                     "distintas para cada delito.\" Dispositivos relevantes citados: Lei nº 7.210/1984 (Lei de Execução Penal), art. 112, III. "
                     "Jurisprudência relevante citada: STF, HC nº 231.110 ED-AgR, Relator Ministro Gilmar Mendes, Segunda Turma, DJe 25/10/2023.",
    "ref": "(EP 102 AgR-segundo, relator Ministro Alexandre de Moraes, Tribunal Pleno, julgado em 14/4/2026, DJe de 8/5/2026.)"}

DADOS_TEXTO = [
    ("2025 · CNJ, I Mutirão Processual Penal — Pena Justa",
     "Foram levantados 107.755 processos de execução penal com incidentes vencidos. Dos 86.398 fora de São Paulo, 24,6% foram analisados "
     "e 75,4% ainda dependiam de análise judicial; entre os analisados, houve concessão de progressões, livramentos, extinções de pena e "
     "outros benefícios em 14.027 processos e resposta negativa em 3.105. O relatório registra que, algumas vezes, o direito já estava "
     "implementado mas não lançado no sistema e, outras vezes, a própria análise estava atrasada.",
     "Relatório final, p. 15, 28, 29 e 30 · cnj.jus.br/wp-content/uploads/2025/11/relatorio-final-mutirao-2025-v5.pdf"),
    ("2024 · CNJ, Mutirão Processual Penal",
     "No tema do sistema eletrônico de execução, foram saneados 50.926 processos: 25.918 de término de pena, 16.979 de progressão de regime "
     "com incidente vencido e 8.056 de livramento condicional com incidente vencido. O CNJ ressalvou que os dados não permitem separar "
     "os casos de simples saneamento do sistema daqueles em que um direito adquirido foi garantido pela intervenção.",
     "Relatório final, p. 22 · cnj.jus.br/relatorio-mutirao-processual-2024/"),
    ("2023 · CNJ, Mutirão Processual Penal",
     "Os tribunais informaram 22.276 pessoas em cumprimento de pena em estabelecimentos de regime fechado embora sentenciadas a regime "
     "menos gravoso; o CNJ leu os dados como indicativo de possível violação sistemática de súmula vinculante. No conjunto do mutirão, "
     "que abrangeu presos provisórios e condenados, 27.010 pessoas tiveram a situação de aprisionamento modificada e 21.866 saíram de "
     "unidades prisionais.",
     "Relatório, p. 15, 29 e 30 · cnj.jus.br/wp-content/uploads/2023/09/relatorio-mutirao-processual-penal.pdf"),
    ("2º semestre de 2025 · SENAPPEN, Relatório de Informações Penais",
     "Em 31/12/2025, 10.224 presos em regime fechado já haviam obtido a progressão e aguardavam transferência. O número é mínimo: 673 "
     "estabelecimentos declararam não controlar esse dado.",
     "RELIPEN, p. 36 · gov.br/senappen/pt-br/servicos/sisdepen/relatorios"),
    ("2023 · STF, ADPF 347",
     "Ao reconhecer o estado de coisas inconstitucional do sistema prisional, o Supremo determinou a elaboração de plano com diretrizes "
     "para reduzir, entre outros pontos, a permanência em regime mais severo ou por tempo superior ao da pena.",
     "Notícia oficial do STF de 04/10/2023 · portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=515220"),
]

CADEIAS = [
    ("Data-base fixada na data da decisão, e não na da falta",
     "O intervalo entre a falta e a decisão que a homologa vira tempo perdido, e o atraso se repete em toda a sequência de "
     "progressões. Se o mesmo lançamento desloca a data do livramento, que não deveria mudar, o erro dobra. E, se a falta "
     "não foi validamente reconhecida, a própria interrupção não deveria existir."),
    ("Detração não computada",
     "Um período de prisão que não entrou no cálculo não aparece como erro: simplesmente desaparece. Todas as datas correm "
     "sobre uma base menor do que a devida. O caso mais oculto é a prisão em outro processo encerrado sem condenação."),
    ("Fração errada na classificação de uma condenação",
     "Crime comum lançado como hediondo, ou primário tratado como reincidente, recebe fração maior. A primeira progressão "
     "atrasa; a segunda, calculada sobre o saldo, herda a distorção; o livramento também se afasta."),
    ("Pena total errada na origem",
     "Guia duplicada, soma onde cabia unificação, pena do acórdão não lançada: a pena total é a base de tudo. Corrigida, "
     "mudam a fração atingida em cada benefício, o fim da pena e o tempo exigido pelos decretos, que podem ser reexaminados."),
    ("Falta grave sem base mantendo três efeitos",
     "Nova data-base, regressão e perda de dias remidos nascem juntas. Se a falta cai, os três caem juntos, e por isso a "
     "conferência da falta vem antes da conferência das datas."),
    ("Remição esquecida ou lançada na data errada",
     "Dias trabalhados sem homologação, saldo que não fecha a proporção e é esquecido, remição lançada na data da decisão: "
     "o tempo cumprido fica menor, e a data da remição pode alterar o regime em que uma falta posterior é considerada."),
    ("Extinção de uma pena que apaga a primeira prisão",
     "Ao declarar extinta uma das condenações, o lançamento pode retirar da linha do tempo o processo da primeira prisão. "
     "O livramento, que se conta a partir dela, passa a ser contado de uma prisão posterior."),
    ("O descarte circular",
     "Um benefício é dado como inútil porque cairia depois do fim da pena, mas essa data foi calculada com o próprio erro "
     "que se pretende corrigir. Refeita a conta no cenário corrigido, o benefício pode caber muito antes."),
]


def julgado_html(j: dict) -> str:
    return (f'<div class="julgado"><p class="trib">{esc(j["trib"])}</p><h3>{esc(j["tese"])}</h3><p>{esc(j["ponte"])}</p>'
            f'<blockquote>{j["integral_html"]}<span class="ref">{esc(j["ref"])}</span></blockquote></div>')


def carregar_catalogo():
    if not CATALOGO.exists():
        return None
    cat = json.loads(CATALOGO.read_text(encoding="utf-8"))
    bases_ok = set(json.loads(BASES_JSON.read_text(encoding="utf-8"))) if BASES_JSON.exists() else set()
    for capx in cat["capitulos"]:
        for e in capx["erros"]:
            e["base"] = [b for b in e.get("base", []) if b in bases_ok]
    return cat


def estudo() -> str:
    cat = carregar_catalogo()
    c = [capa("Estudo completo", "Revisão completa da execução penal",
              "Como os erros nascem, como se propagam pela pena e o que uma análise completa pode encontrar.")]
    c.append(cab("Revisão completa da execução penal · estudo"))
    secoes = ["Apresentação", "A execução como cálculo encadeado", "O que dizem os dados oficiais", "O efeito cascata",
              "Catálogo de erros", "Histórias-exemplo", "O que a revisão confere", "O que dizem os tribunais",
              "O que pesa contra", "Método e entrega", "Documentos para começar", "Glossário"]
    c.append('<h2 class="cap">Sumário</h2><ol class="sumario-pdf">' + "".join(
        f"<li><span>{i}</span><span>{esc(s)}</span></li>" for i, s in enumerate(secoes, 1)) + "</ol>")
    c.append('<div class="caixa"><p class="rot">Como ler</p><p>Este estudo é informativo. Os exemplos são hipotéticos e as frações, '
             'ilustrativas: em caso real, cada fração depende da data do fato, da natureza do crime e da reincidência, e as frações do '
             'art. 112 da Lei de Execução Penal foram reescritas mais de uma vez, a última em 2026, com a nova redação questionada no '
             'Supremo Tribunal Federal. Os precedentes são reproduzidos na íntegra do texto oficial (tese, enunciado ou ementa), com a '
             'referência completa. Os dados oficiais trazem a fonte e a página.</p></div>')
    c.append('<h2 class="cap nova"><span class="num">1</span>Apresentação</h2><div class="recuo">'
             '<p class="abre">A execução penal é a fase em que a pena fixada na condenação é efetivamente cumprida. É também a fase em que '
             'essa pena deixa de ser um número fixo: ela é reduzida por remição e detração, interrompida por faltas, somada a novas '
             'condenações, alcançada por decretos de indulto e comutação, e recalculada a cada um desses eventos. Ao longo de anos, '
             'muitas pessoas e sistemas tocam a mesma conta.</p>'
             '<p>Este estudo descreve, em linguagem acessível, onde essa conta costuma falhar, por que uma falha raramente fica '
             'isolada e o que uma revisão completa confere, capítulo a capítulo. Não substitui a análise do caso concreto: cada execução '
             'depende dos seus documentos.</p></div>')
    c.append('<h2 class="cap"><span class="num">2</span>A execução como cálculo encadeado</h2><div class="recuo">'
             '<p class="abre">Três dados governam quase todos os benefícios: a pena total, a fração exigida pela lei e a data a partir da '
             'qual se conta o prazo, a data-base. A progressão de regime, o livramento condicional, o indulto e a comutação dependem de '
             'combinações desses três dados.</p>'
             '<p>Cada um deles nasce em um documento diferente. A pena vem da sentença e do acórdão, transportados pela guia de '
             'recolhimento; a fração vem da lei vigente na data de cada fato; a data-base vem dos registros de prisão, soltura, fuga, '
             'recaptura e falta. Os dados são lançados no sistema eletrônico de execução, que faz o cálculo a partir do que recebe. '
             'Uma decisão juntada aos autos e não lançada não existe para o cálculo.</p>'
             '<p>Daí a regra que orienta toda revisão: o cálculo pode estar aritmeticamente correto e, ainda assim, errado, porque '
             'partiu de um dado errado. A conferência não se limita a refazer a conta; ela volta a cada documento de origem.</p></div>')
    c.append('<h2 class="cap nova"><span class="num">3</span>O que dizem os dados oficiais</h2>')
    c.append(numeros())
    for t, txt, f in DADOS_TEXTO:
        c.append(f'<div class="caixa"><p class="rot">{esc(t)}</p><p>{esc(txt)}</p><p class="nota">{esc(f)}</p></div>')
    c.append('<p class="nota">Processos revisados, processos com alteração, pessoas soltas e benefícios concedidos medem coisas diferentes '
             'e não se somam. Os números acima são reproduzidos com a grandeza que a fonte oficial indica.</p>')
    c.append('<h2 class="cap nova"><span class="num">4</span>O efeito cascata</h2>')
    c.append('<p>Na execução, os benefícios são encadeados: cada um é contado a partir de uma pena e de uma data-base que dependem das '
             'etapas anteriores. Por isso o erro se propaga. Abaixo, as cadeias mais frequentes.</p>')
    c.append('<ol class="passos">' + "".join(f"<li><h4>{esc(t)}</h4><p>{esc(p)}</p></li>" for t, p in CADEIAS) + "</ol>")
    c.append('<h3>Um exemplo com a conta</h3>')
    c.append(P.grafico_svg())
    c.append(quadro())
    c.append('<h2 class="cap nova"><span class="num">5</span>Catálogo de erros</h2>')
    if cat:
        c.append('<p>Os erros a seguir são descritos de forma genérica, com exemplos hipotéticos e a base legal conferida no texto '
                 'oficial. Nem todo erro aparece em toda execução; muitos aparecem combinados.</p>')
        for capx in cat["capitulos"]:
            c.append(f'<h3>{esc(capx["titulo"])}</h3><p>{esc(capx.get("intro", ""))}</p>')
            for e in capx["erros"]:
                base = f'<p class="base">{esc("; ".join(e["base"]))}.</p>' if e.get("base") else ""
                c.append(f'<div class="erro"><h4><span class="id">{esc(e["id"].replace("E-", ""))}</span>{esc(e["titulo"])}</h4>'
                         f'<p>{esc(e["como"])}</p><p><span class="r">Onde aparece</span>{esc(e["onde"])}</p>'
                         f'<p><span class="r">Efeito</span>{esc(e["efeito"])}</p>{base}</div>')
    else:
        for t, cx, ef, b in P.ERROS:
            c.append(f'<div class="erro"><h4>{esc(t)}</h4><p>{esc(cx)}</p><p><span class="r">Efeito</span>{esc(ef)}</p><p class="base">{esc(b)}</p></div>')
    c.append('<h2 class="cap nova"><span class="num">6</span>Histórias-exemplo</h2>')
    c.append('<p class="nota">Pessoas e números fictícios, criados para explicar. Não são casos do escritório. Frações ilustrativas.</p>')
    if cat:
        for h in cat["historias"]:
            c.append(f'<div class="caixa"><p class="rot">Exemplo hipotético</p><h3>{esc(h["titulo"])}</h3><p>{esc(h["cena"])}</p>'
                     f'<p><strong>Antes.</strong> {esc(h["antes"])}</p><p><strong>Depois.</strong> {esc(h["depois"])}</p>'
                     f'<p><strong>A conta.</strong> {esc(h["conta"])}</p></div>')
    else:
        for t, cena, sol, _conta in P.EXEMPLOS:
            c.append(f'<div class="caixa"><p class="rot">Exemplo hipotético</p><h3>{esc(t)}</h3><p>{esc(cena)}</p><p>{esc(sol)}</p></div>')
    c.append('<h2 class="cap nova"><span class="num">7</span>O que a revisão confere</h2>')
    for i, (t, intro, itens) in enumerate(P.CAPITULOS, 1):
        c.append(f'<h3>{i}. {esc(t)}</h3><p>{esc(intro)}</p><ul class="check">' + "".join(
            f"<li><strong>{esc(a)}</strong>: {esc(b)}</li>" for a, b in itens) + "</ul>")
    c.append('<h2 class="cap nova"><span class="num">8</span>O que dizem os tribunais</h2>')
    c.append('<p>Precedentes conferidos na fonte oficial, reproduzidos na íntegra do texto oficial, com o trecho decisivo em negrito.</p>')
    for j in P.JULGADOS + JULG_PDF_EXTRA:
        c.append(julgado_html(j))
    c.append('<h2 class="cap nova"><span class="num">9</span>O que pesa contra</h2>')
    c.append('<p>Uma revisão séria mostra também o que limita as teses favoráveis. Os enunciados abaixo são aplicados pelos tribunais e '
             'precisam ser considerados em cada cálculo.</p>')
    for trib, tese, txt, ref, nota in CONTRA:
        c.append(f'<div class="julgado"><p class="trib">{esc(trib)}</p><h3>{esc(tese)}</h3><p>{esc(nota)}</p>'
                 f'<blockquote>{esc(txt)}<span class="ref">{esc(ref)}</span></blockquote></div>')
    c.append(julgado_html(EP102))
    c.append('<h2 class="cap nova"><span class="num">10</span>Método e entrega</h2>')
    c.append('<ol class="passos">' + "".join(f"<li><h4>{esc(t)}</h4><p>{esc(p)}</p></li>" for t, p in P.METODO) + "</ol>")
    c.append('<h3>O que o cliente recebe</h3><ul class="check">' + "".join(
        f"<li><strong>{esc(a)}</strong>: {esc(b)}</li>" for a, b in P.ENTREGA) + "</ul>")
    c.append('<h3>Perguntas frequentes</h3>' + "".join(f"<p><strong>{esc(q)}</strong> {esc(r)}</p>" for q, r in P.FAQ))
    c.append('<h2 class="cap"><span class="num">11</span>Documentos para começar</h2><ul class="check">' + "".join(
        f"<li><strong>{esc(a)}</strong>, {esc(b)}</li>" for a, b in P.DOCUMENTOS) + "</ul>")
    if cat and cat.get("glossario"):
        c.append('<h2 class="cap nova"><span class="num">12</span>Glossário</h2><dl class="glos">' + "".join(
            f"<dt>{esc(g['termo'])}</dt><dd>{esc(g['definicao'])}</dd>" for g in cat["glossario"]) + "</dl>")
    c.append(fecho())
    return documento("Estudo — Revisão completa da execução penal", "Estudo completo", "\n".join(c))


def imprimir(html: str, destino: Path) -> None:
    """Chrome sem interface grava o PDF; às vezes não fecha sozinho: espera o arquivo estabilizar e encerra."""
    import time
    with tempfile.TemporaryDirectory() as d:
        fonte = Path(d) / "doc.html"
        fonte.write_text(html, encoding="utf-8")
        if destino.exists():
            destino.unlink()
        proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
                                 "--virtual-time-budget=15000", "--disk-cache-size=1", f"--user-data-dir={d}/perfil",
                                 f"--print-to-pdf={destino}", fonte.as_uri()],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tamanho, estavel = -1, 0
        for _ in range(240):
            time.sleep(1)
            if proc.poll() is not None and destino.exists():
                break
            atual = destino.stat().st_size if destino.exists() else -1
            estavel = estavel + 1 if atual > 0 and atual == tamanho else 0
            tamanho = atual
            if estavel >= 4:
                break
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        if not destino.exists() or destino.stat().st_size == 0:
            raise RuntimeError(f"PDF não gerado: {destino}")


def main() -> None:
    docs = PUBLIC / "assets" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    so = sys.argv[1] if len(sys.argv) > 1 else ""
    saidas = []
    if so in ("", "guia"):
        saidas.append((guia(), docs / Path(P.PDF_GUIA).name))
    if so in ("", "estudo"):
        saidas.append((estudo(), docs / Path(P.PDF_ESTUDO).name))
    for html, destino in saidas:
        imprimir(html, destino)
        print(destino)
    if COPIA_ONEDRIVE.parents[1].exists():
        COPIA_ONEDRIVE.mkdir(parents=True, exist_ok=True)
        for _h, destino in saidas:
            shutil.copy2(destino, COPIA_ONEDRIVE / destino.name)
        print(COPIA_ONEDRIVE)


if __name__ == "__main__":
    main()
