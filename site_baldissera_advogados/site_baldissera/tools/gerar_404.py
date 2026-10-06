"""Página de erro própria (404.html) — SEO de 04/10/2026.

A Vercel mostra public/404.html a quem abre um endereço que não existe. O menu e o rodapé
vêm de tools/molde.py (desde 06/10/2026); os endereços viram absolutos ("/assets/...", "/publicacoes"),
porque a página pode aparecer em qualquer caminho (ex.: /a/b/c). Marcada para não ir ao Google.
Rodar de novo quando o molde mudar.
Uso:  python gerar_404.py
"""
import re
from pathlib import Path

PUB = Path(__file__).resolve().parents[1] / "public"


def absolutos(trecho: str) -> str:
    """href="index.html" -> href="/"; href="contato.html" -> href="/contato"; src="assets/x" -> src="/assets/x"."""
    trecho = re.sub(r'(href|src)="index\.html"', r'\1="/"', trecho)
    trecho = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|/|#)([^"]+?)\.html"', r'\1="/\2"', trecho)
    return re.sub(r'(href|src)="(?!https?:|mailto:|tel:|/|#)([^"]+)"', r'\1="/\2"', trecho)


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import molde  # cabeçalho, rodapé e recursos comuns (visual "liturgia", 06/10/2026)
    links = [("/publicacoes", "Publicações", "análises de julgados e temas jurídicos"),
             ("/areas-de-atuacao", "Áreas de atuação", "as oito áreas do escritório"),
             ("/advogados", "Advogados", "a equipe e as inscrições na OAB"),
             ("/contato", "Contato", "endereços das unidades"),
             ("/agendar", "Agendar atendimento", "marcar um horário com um advogado"),
             ("/", "Página inicial", "o escritório")]
    itens = "\n".join(f'<li><a href="{u}"><span class="ref-nome">{t}</span><span class="ref-desc">{d}</span></a></li>'
                      for u, t, d in links)
    head = """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Página não encontrada · Baldissera Advogados</title>
<meta name="robots" content="noindex">
<meta name="description" content="O endereço procurado não existe ou mudou. As publicações e as páginas do escritório Baldissera Advogados seguem disponíveis.">
<script defer src="/_vercel/insights/script.js"></script>
"""
    corpo = f"""<section class="cabeca-pagina">
  <p class="sobretitulo">Erro 404</p>
  <h1>Página não encontrada.</h1>
  <p class="preambulo">O endereço procurado não existe ou mudou de lugar. O conteúdo do escritório continua disponível pelos caminhos abaixo.</p>
</section>
<div class="pagina-texto">
<ul class="diplomas fontes-lista">
{itens}
</ul>
</div>
"""
    pagina = absolutos(molde.pagina(head, corpo))
    (PUB / "404.html").write_text(pagina, encoding="utf-8", newline="\n")
    print("404.html gravada")


if __name__ == "__main__":
    main()
