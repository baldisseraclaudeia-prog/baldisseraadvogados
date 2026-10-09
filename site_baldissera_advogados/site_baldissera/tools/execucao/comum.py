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
