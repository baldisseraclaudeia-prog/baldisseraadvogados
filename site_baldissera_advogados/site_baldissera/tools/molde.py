"""
Molde comum do site (visual "liturgia", 06/10/2026).

Fonte única do cabeçalho, do rodapé e dos recursos de <head> de TODAS as páginas: o publicador,
o gerador da página de erro e os scripts de revestimento importam daqui. Antes, cada gerador
copiava o cabeçalho de index.html e as cópias divergiam (cinco versões em 35 páginas).

O <head> técnico de cada página (título, descrição, og:*, canonical, dados estruturados) não é
gerado aqui: quem monta a página o preserva. Aqui só se trocam as folhas de estilo e as fontes.
"""
import re

FONTES = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500"
          "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap")
VERSAO = "20261006"   # muda quando liturgia.css ou site.js mudam, para o navegador não usar cópia velha

RECURSOS = f"""<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTES}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="stylesheet" href="assets/css/liturgia.css?v={VERSAO}">"""

WHATSAPP = "https://wa.me/5545991029806"
EMAIL = "contato@baldisseraadvogados.com.br"
TELEFONE = ("+5545991029806", "+55 45 99102-9806")

NAV = [("Escritório", "sobre.html"), ("Atuação", "areas-de-atuacao.html"), ("Advogados", "advogados.html"),
       ("Publicações", "publicacoes.html"), ("Contato", "contato.html"), ("Agendar atendimento", "agendar.html")]

UNIDADES = [("Cascavel", "Paraná", "cascavel"), ("Porto Alegre", "Rio Grande do Sul", "porto-alegre"),
            ("Foz do Iguaçu", "Paraná", "foz-do-iguacu"), ("Porto Belo", "Santa Catarina", "porto-belo")]


def trocar_head(head: str) -> str:
    """Tira do <head> as fontes, o style.css antigo, os ícones e os blocos <style> de página;
    põe os recursos do molde logo antes dos dados estruturados (ou no fim do head)."""
    h = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", head)
    h = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*"[^>]*>\s*', "", h)
    h = re.sub(r'<link href="https://fonts\.googleapis\.com[^"]*" rel="stylesheet"[^>]*>\s*', "", h)
    h = re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>\s*', "", h)
    h = re.sub(r'<link rel="stylesheet" href="assets/css/[^"]*"[^>]*>\s*', "", h)
    h = re.sub(r"(?is)<style[^>]*>.*?</style>\s*", "", h)
    i = h.find('<script type="application/ld+json">')
    if i < 0:
        i = h.find('<script defer src="/_vercel/insights')
    if i < 0:
        i = len(h)
    return h[:i] + RECURSOS + "\n" + h[i:]


def cabecalho(atual: str = "") -> str:
    """Barra de contatos e acessibilidade + cabeçalho escuro com busca e menu."""
    itens = "\n".join(
        f'      <li><a href="{u}"{" aria-current=\"page\"" if n == atual else ""}>{n}</a></li>' for n, u in NAV)
    return f'''<a class="pular" href="#conteudo">Pular para o conteúdo</a>

<div class="barra-topo">
  <div class="barra-interna">
    <span class="contatos">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="tel:{TELEFONE[0]}">{TELEFONE[1]}</a>
      <a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a>
    </span>
    <div class="acess" role="group" aria-label="Acessibilidade">
      <button type="button" data-letra="-1" aria-label="Diminuir o tamanho da letra">A−</button>
      <button type="button" data-letra="1" aria-label="Aumentar o tamanho da letra">A+</button>
      <button type="button" data-contraste aria-pressed="false">Alto contraste</button>
    </div>
  </div>
</div>

<header class="cabecalho" id="cabecalho">
  <div class="cab-interno">
    <a class="cab-marca" href="index.html"><img src="assets/images/marca/baldissera-advogados-escuro.svg" alt="Baldissera Advogados, página inicial" width="224" height="75"></a>
    <form class="busca busca-cab" role="search" action="publicacoes.html">
      <label class="so-leitor" for="busca-cab">Buscar no site</label>
      <input id="busca-cab" type="search" placeholder="O que você procura?" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="res-cab">
      <ul id="res-cab" class="busca-resultados" role="listbox" aria-label="Resultados da busca" hidden></ul>
    </form>
    <button class="menu-botao" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  </div>
  <nav class="ordem" id="menu" aria-label="Principal">
    <ul>
{itens}
    </ul>
  </nav>
</header>
'''


def rodape() -> str:
    unidades = "\n".join(
        f'        <li><a href="contato.html#{a}">{c}, {e}</a></li>' for c, e, a in UNIDADES)
    nav = "\n".join(f'        <li><a href="{u}">{n if n != "Atuação" else "Áreas de atuação"}</a></li>' for n, u in NAV)
    return f'''<footer class="fecho">
  <div class="fecho-interno">
    <div>
      <img src="assets/images/marca/baldissera-advogados-escuro.svg" alt="Baldissera Advogados" width="224" height="75">
      <div class="assinatura-casa">
        <p class="nome">Baldissera Advogados</p>
        <p>Sociedade de Advogados · OAB/PR 4.545</p>
        <p>CNPJ 24.129.499/0001-08</p>
        <p class="fecho-contato"><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{TELEFONE[0]}">{TELEFONE[1]}</a></p>
      </div>
    </div>
    <nav aria-label="Rodapé">
      <h2>Navegação</h2>
      <ul>
{nav}
      </ul>
    </nav>
    <div id="unidades">
      <h2>Unidades</h2>
      <ul>
{unidades}
      </ul>
    </div>
  </div>
  <div class="fecho-base">
    <span>© 2026 Baldissera Advogados</span>
    <span><a href="politica-de-privacidade.html">Política de privacidade</a> &nbsp;&nbsp; <a href="aviso-provimento-205.html">Provimento CFOAB 205/2021</a></span>
  </div>
</footer>

<button class="voltar-topo" type="button" hidden>Voltar ao topo</button>
<script src="assets/js/site.js?v={VERSAO}"></script>
'''


def pagina(head: str, corpo: str, atual: str = "", depois: str = "") -> str:
    """Página inteira: <head> preservado (com recursos trocados) + cabeçalho + <main> + rodapé.
    `depois` entra antes de </body> (scripts próprios da página, como o filtro da lista)."""
    head = trocar_head(head)
    return (f"{head}</head>\n<body>\n\n{cabecalho(atual)}\n<main id=\"conteudo\" tabindex=\"-1\">\n{corpo}\n</main>\n\n"
            f"{rodape()}{depois}</body>\n</html>\n")


def separar_head(html_pagina: str) -> str:
    """Devolve tudo até (sem incluir) </head> da página existente."""
    return html_pagina[:html_pagina.index("</head>")]
