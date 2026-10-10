"""
Partes comuns às páginas do portal de execução penal (ordem do Dr. Luiz, 09/10/2026):
"Execução penal em linguagem simples" (gerar_explicada.py) e "Revisão da execução penal, por fases"
(tools/gerar_revisao_execucao.py). Aqui ficam o aviso do Provimento 205, a biografia do responsável
técnico, a frase de atendimento e o bloco do autor, para as duas páginas dizerem a mesma coisa.
"""
import html
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit("use ~/.local/bin/python3.12 (o Python 3.9 do sistema não roda as ferramentas do site)")

RAIZ = Path(__file__).resolve().parents[2]      # .../site_baldissera (tools/execucao/ → tools/ → raiz)
PUBLIC = RAIZ / "public"
BASE = "https://www.baldisseraadvogados.com.br"

# contato ao fim das páginas de execução penal: "A" = com botão "Agendar atendimento";
# "B" = sem botão (recomendação do conselho de redação, 08/10/2026). Decisão do Dr. Luiz pendente (GATE 5).
CONTATO_PADRAO = "B"

AVISO = ("Conteúdo informativo, nos termos do Provimento CFOAB 205/2021. Os exemplos são fictícios e não se referem a casos do "
         "escritório. O resultado de cada execução depende dos documentos e das circunstâncias do caso. Julgados citados com "
         "tribunal, número, relator, data e endereço oficial; a data da conferência consta em cada um.")
CONTATO_FRASE = "Atendimento virtual em todo o Brasil e atendimento presencial nas unidades de Cascavel, Porto Alegre, Foz do Iguaçu e Porto Belo, mediante agendamento prévio."
BIO = "Defesa criminal, habeas corpus e recursos perante o STJ e o STF, execução penal e sistema penitenciário federal."
AUTOR = "Luiz Henrique Baldissera"
CARGO = "Advogado criminalista · OAB/PR 55.717 · OAB/SC 78.938-A"
FOTO = "assets/images/luiz-henrique-baldissera.jpg"
INSTAGRAM = [("luizhbaldissera", "https://www.instagram.com/luizhbaldissera/"),
             ("baldisseraadvocacia", "https://www.instagram.com/baldisseraadvocacia/")]
WHATSAPP_ESCRITORIO = "https://wa.me/5545991029806"


# "Das palavras usadas nesta página" — glossário único das duas páginas do portal (termo → explicação curta).
# Veio de gerar_explicada.py em 09/10/2026; os quatro últimos entraram para a Revisão por fases na mesma data.
PALAVRAS = [
    ("Atestado de pena", "Documento que o juízo da execução deve entregar todo ano, com a pena total, o que já foi cumprido e as datas previstas de cada benefício; previsão não equivale à concessão."),
    ("Detração", "Desconto, na pena, do tempo de prisão ou de recolhimento já cumprido antes da condenação."),
    ("Progressão de regime", "Passagem para regime menos rigoroso, por decisão judicial, após o cumprimento do tempo exigido e dos demais requisitos aplicáveis ao caso."),
    ("Remição", "Reconhecimento de tempo como pena cumprida por trabalho, estudo ou leitura, conforme as regras aplicáveis."),
    ("Data-base", "Dia a partir do qual se conta o tempo para o próximo benefício."),
    ("Falta grave", "Infração disciplinar prevista na Lei de Execução Penal que pode reiniciar a contagem da progressão e custar parte dos dias remidos."),
    ("Livramento condicional", "Liberdade antecipada, com condições, depois de cumprida parte da pena."),
    ("Tese repetitiva", "Resposta fixada pelo STJ num tema repetitivo, obrigatória para os demais juízes."),
    ("Comutação", "Redução da pena por decreto presidencial, também chamada de indulto parcial, quando o juiz reconhece o cumprimento dos requisitos do decreto."),
    ("Indulto", "Perdão concedido por decreto presidencial que extingue a pena alcançada pelo benefício, quando o juiz reconhece o cumprimento dos requisitos do decreto."),
    ("SEEU", "Sistema Eletrônico de Execução Unificado, do Conselho Nacional de Justiça (CNJ), usado por tribunais para acompanhar processos de execução penal, registrar decisões e calcular a pena."),
    ("Trânsito em julgado", "Momento em que a decisão não admite mais recurso e passa a valer definitivamente."),
]


def palavras_html(termos=None) -> str:
    """Lista de definições no padrão da linguagem simples (`dl.ex-palavras`); `termos` filtra e ordena."""
    sel = [(t, d) for t, d in PALAVRAS if termos is None or t in termos]
    if termos:
        sel.sort(key=lambda x: termos.index(x[0]))
    return '<dl class="ex-palavras">\n' + "\n".join(f"  <dt>{esc(t)}</dt><dd>{esc(d)}</dd>" for t, d in sel) + "\n</dl>"


def esc(t: str) -> str:
    return html.escape(t or "", quote=False)


def autor_html(rotulo: str = "Responsável técnico") -> str:
    return f'''<section class="autor-bloco" aria-label="{esc(rotulo)}">
  <img src="{FOTO}" alt="" width="520" height="650" loading="lazy" decoding="async">
  <div>
    <p class="rotulo">{esc(rotulo)}</p>
    <h2>{esc(AUTOR)}</h2>
    <p class="cargo">{esc(CARGO)}</p>
    <p class="bio">{esc(BIO)}</p>
    <p><a class="remissao" href="perfil-luiz.html">Ver perfil</a></p>
  </div>
</section>'''


def redes_html() -> str:
    return " · ".join(f'<a href="{u}" target="_blank" rel="noopener">@{n}</a>' for n, u in INSTAGRAM)


def contato_html(modo: str = None) -> str:
    modo = modo or CONTATO_PADRAO
    botao = ' <a class="botao" href="agendar.html">Agendar atendimento</a>' if modo == "A" else ""
    return f'<p class="rv-contato">{esc(CONTATO_FRASE)}{botao}</p>'


def aviso_html() -> str:
    return f'<p class="rv-aviso">{esc(AVISO)}</p>'


def publicacoes_html(numeral: str) -> str:
    """Seção "Das publicações sobre execução penal" ao fim das páginas do portal (ordem do Dr. Luiz, 09/10/2026).
    O miolo fica entre os marcadores PUBLICACOES-AREA e é reescrito pelo publicador a cada nova publicação
    (tools/publicador/vitrines.py, PAGINAS_AREA), como na página da área."""
    sys.path.insert(0, str(RAIZ / "tools" / "publicador"))
    import vitrines
    miolo = vitrines.bloco_area([x for x in vitrines.cartoes(PUBLIC) if x["area"] == "execucao-penal"])
    return f'''<section class="secao" id="pub-area" aria-labelledby="t-pub-area">
    <header>
      <span class="numeral" aria-hidden="true">{numeral}</span>
      <h2 id="t-pub-area">Das publicações sobre execução penal</h2>
      <p class="nota-secao">Atualizada a cada nova publicação desta matéria.</p>
    </header>
    <ul class="pub-grade">
<!-- PUBLICACOES-AREA-INICIO -->
{miolo}
<!-- PUBLICACOES-AREA-FIM -->
    </ul>
  </section>'''


def compartilhar_html(titulo: str, url: str, rotulo: str = "Compartilhar esta análise") -> str:
    """Bloco de compartilhar (09/10/2026, aprovado pelo Dr. Luiz): WhatsApp e e-mail levam só o título e o link;
    sem resumo e sem o WhatsApp do escritório na mensagem; "Copiar link" via site.js ([data-copiar])."""
    from urllib.parse import quote
    import molde
    msg = f"{titulo}\n{url}"
    wa = "https://wa.me/?text=" + quote(msg, safe="")
    mail = "mailto:?subject=" + quote(titulo, safe="") + "&body=" + quote(msg, safe="")
    return (f'''<aside class="compartilhar" aria-label="Compartilhar">
  <p class="rotulo">{esc(rotulo)}</p>
  <div class="acoes">
    <a class="botao" href="{esc(wa)}" target="_blank" rel="noopener">{molde.ICO_WHATS}WhatsApp</a>
    <a class="botao botao-claro" href="{esc(mail)}">E-mail</a>
    <button type="button" class="botao botao-claro" data-copiar="{esc(url)}">Copiar link</button>
  </div>
  <p class="nota" data-copiado hidden>Link copiado.</p>
  <p class="redes">{redes_html()}</p>
</aside>''')
