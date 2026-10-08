"""
Molde comum do site (visual "liturgia", 06/10/2026).

Fonte única do cabeçalho, do rodapé e dos recursos de <head> de TODAS as páginas: o publicador,
o gerador da página de erro e os scripts de revestimento importam daqui. Antes, cada gerador
copiava o cabeçalho de index.html e as cópias divergiam (cinco versões em 35 páginas).

O <head> técnico de cada página (título, descrição, og:*, canonical, dados estruturados) não é
gerado aqui: quem monta a página o preserva. Aqui só se trocam as folhas de estilo e as fontes.
"""
import re

FONTES = ("https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500"
          "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap")
VERSAO = "20261008d"   # muda quando liturgia.css ou site.js mudam, para o navegador não usar cópia velha

RECURSOS = f"""<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTES}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="stylesheet" href="assets/css/liturgia.css?v={VERSAO}">"""

WHATSAPP = "https://wa.me/5545991029806"
# Instagram do escritório (barra do topo e rodapé de TODAS as páginas; o pessoal do Dr. Luiz vai nas publicações e no perfil)
INSTAGRAM = ("baldisseraadvocacia", "https://www.instagram.com/baldisseraadvocacia/")
EMAIL = "contato@baldisseraadvogados.com.br"
TELEFONE = ("+5545991029806", "+55 45 99102-9806")

# Símbolos dos canais de contato (07/10/2026: "deixe tudo em harmonia") — fonte única para TODAS as páginas.
ICO_EMAIL = ('<svg class="ico-linha" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>')
ICO_TEL = ('<svg class="ico-linha" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
           '19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 '
           '12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 '
           '2.81.7A2 2 0 0 1 22 16.92z"/></svg>')
ICO_WHATS = '''<svg class="ico-whats" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'''


def ico_insta(gid: str) -> str:
    """Símbolo do Instagram no degradê da marca. `gid` = id único do degradê na página."""
    u = f"url(#{gid})"
    return (f'<svg class="ico-insta ico-insta-cor" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="2" y1="22" x2="22" y2="2">'
            '<stop offset="0" stop-color="#FEDA75"/><stop offset=".25" stop-color="#FA7E1E"/><stop offset=".5" stop-color="#D62976"/>'
            '<stop offset=".75" stop-color="#962FBF"/><stop offset="1" stop-color="#4F5BD5"/></linearGradient></defs>'
            f'<rect x="2" y="2" width="20" height="20" rx="5" ry="5" stroke="{u}"/>'
            f'<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" stroke="{u}"/>'
            f'<line x1="17.5" y1="6.5" x2="17.51" y2="6.5" stroke="{u}"/></svg>')


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
      <a href="mailto:{EMAIL}">{ICO_EMAIL}{EMAIL}</a>
      <a href="tel:{TELEFONE[0]}">{ICO_TEL}{TELEFONE[1]}</a>
      <a href="{WHATSAPP}" target="_blank" rel="noopener">{ICO_WHATS}WhatsApp</a>
      <a href="{INSTAGRAM[1]}" target="_blank" rel="noopener">{ico_insta("ig-topo")}Instagram</a>
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
        <p class="fecho-contato"><a href="mailto:{EMAIL}">{ICO_EMAIL}{EMAIL}</a><br><a href="tel:{TELEFONE[0]}">{ICO_TEL}{TELEFONE[1]}</a><br><a href="{WHATSAPP}" target="_blank" rel="noopener">{ICO_WHATS}WhatsApp</a><br><a href="{INSTAGRAM[1]}" target="_blank" rel="noopener">{ico_insta("ig-fecho")}@{INSTAGRAM[0]}</a></p>
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
