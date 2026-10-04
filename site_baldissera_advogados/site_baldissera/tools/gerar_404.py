"""Página de erro própria (404.html) — SEO de 04/10/2026.

A Vercel mostra public/404.html a quem abre um endereço que não existe. O menu e o rodapé
são copiados de index.html; os endereços viram absolutos ("/assets/...", "/publicacoes"),
porque a página pode aparecer em qualquer caminho (ex.: /a/b/c). Marcada para não ir ao Google.
Rodar de novo quando o menu ou o rodapé da página inicial mudar.
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
    idx = (PUB / "index.html").read_text(encoding="utf-8")
    contato = idx[idx.index('<div class="contact-bar">'):idx.index('<header class="b-header">')]
    cabecalho = idx[idx.index('<header class="b-header">'):idx.index("</header>") + 9].replace(' class="active"', "")
    rodape = idx[idx.index('<footer class="b-footer">'):idx.index("</body>")]
    links = [("/publicacoes", "Publicações", "análises de julgados e temas jurídicos"),
             ("/areas-de-atuacao", "Áreas de atuação", "as sete frentes do escritório"),
             ("/advogados", "Advogados", "a equipe e as inscrições na OAB"),
             ("/contato", "Contato", "endereços das unidades"),
             ("/", "Página inicial", "o escritório")]
    cartoes = "\n".join(
        f'<a href="{u}" style="display:block;background:var(--ivory);border:0.5px solid var(--gold-light);border-radius:8px;padding:20px 24px;text-decoration:none;">'
        f'<span style="display:block;font-family:var(--serif);font-weight:500;font-size:20px;color:var(--navy);margin:0 0 4px;">{t}</span>'
        f'<span style="font-size:13px;color:var(--text-muted);">{d}</span></a>' for u, t, d in links)
    pagina = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Página não encontrada · Baldissera Advogados</title>
<meta name="robots" content="noindex">
<meta name="description" content="O endereço procurado não existe ou mudou. As publicações e as páginas do escritório Baldissera Advogados seguem disponíveis.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&display=swap">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/css/style.css">
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>

{absolutos(contato)}{absolutos(cabecalho)}

<section style="padding:80px 40px 50px;background:var(--ivory-bg);text-align:center;border-bottom:0.5px solid var(--border-soft);">
<p style="font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);font-weight:500;margin-bottom:20px;">ERRO 404</p>
<h1 style="font-family:var(--serif);font-weight:500;font-size:48px;line-height:1.15;letter-spacing:.01em;color:var(--navy);margin:0 auto 22px;max-width:760px;">Página não encontrada.</h1>
<p style="font-size:15px;line-height:1.85;color:var(--text-soft);margin:0 auto 24px;max-width:620px;">O endereço procurado não existe ou mudou de lugar. O conteúdo do escritório continua disponível pelos caminhos abaixo.</p>
<div class="hd-orn"><div class="line"></div><div class="d"></div><div class="line"></div></div>
</section>

<section style="padding:50px 40px 80px;background:var(--ivory-bg);">
<div style="max-width:620px;margin:0 auto;display:grid;grid-template-columns:1fr;gap:12px;">
{cartoes}
</div>
</section>

{absolutos(rodape)}</body>
</html>
"""
    (PUB / "404.html").write_text(pagina, encoding="utf-8", newline="\n")
    print("404.html gravada")


if __name__ == "__main__":
    main()
