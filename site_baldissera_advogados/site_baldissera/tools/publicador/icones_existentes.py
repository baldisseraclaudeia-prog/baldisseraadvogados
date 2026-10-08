"""
Símbolos de contato nas publicações já no ar (07/10/2026, "deixe tudo em harmonia").

Troca, em cada public/publicacao-*.html, só duas linhas do bloco de compartilhar, pelo mesmo
HTML que o publicador gera hoje: o botão "Compartilhar no WhatsApp" ganha o símbolo e a linha
"No Instagram" ganha o símbolo da marca em cada perfil. Nada mais na página muda.
Uso: python icones_existentes.py
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent))
import molde  # noqa: E402
import publicar as P  # noqa: E402

PUB = AQUI.parents[1] / "public"
feitas = []
for f in sorted(PUB.glob("publicacao-*.html")):
    s = f.read_text(encoding="utf-8")
    n = re.sub(r'(<a class="botao" href="[^"]*" target="_blank" rel="noopener">)(?:<svg class="ico-whats".*?</svg>)?Compartilhar no WhatsApp</a>',
               lambda m: m.group(1) + molde.ICO_WHATS + "Compartilhar no WhatsApp</a>", s, count=1, flags=re.S)
    n = re.sub(r'<p class="redes">No Instagram: .*?</p>', lambda m: f'<p class="redes">No Instagram: {P.redes_html()}</p>', n, count=1, flags=re.S)
    if n != s:
        f.write_text(n, encoding="utf-8", newline="\n"); feitas.append(f.name)
print(f"{len(feitas)} publicação(ões) com símbolos: " + ", ".join(feitas))
