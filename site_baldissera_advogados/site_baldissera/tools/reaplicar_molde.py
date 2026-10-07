"""
Reaplica o molde (tools/molde.py) às páginas já moldadas, sem tocar no conteúdo.

Quando o cabeçalho, a barra de contatos ou o rodapé mudam em molde.py, este script
reconstrói cada página de public/ que já usa o molde: preserva o <head> técnico, o <main>
inteiro e os scripts próprios da página (o que vem depois de site.js), e troca só a moldura.
404.html fica de fora (tem gerador próprio, gerar_404.py, com endereços absolutos).

Uso:  python tools/reaplicar_molde.py            # todas as páginas moldadas
      python tools/reaplicar_molde.py public/sobre.html [...]
Conferir depois:  python tools/conferir_texto.py public/<pagina>.html
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import molde  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[1] / "public"
MARCA_MAIN = '<main id="conteudo" tabindex="-1">\n'


def reaplicar(caminho: Path) -> bool:
    h = caminho.read_text(encoding="utf-8")
    if 'class="barra-topo"' not in h or caminho.name == "404.html":
        return False
    head = molde.separar_head(h)
    i = h.index(MARCA_MAIN) + len(MARCA_MAIN)
    j = h.rindex("\n</main>")
    corpo = h[i:j]
    m = re.search(r'<li><a href="[^"]+" aria-current="page">([^<]+)</a></li>', h)
    atual = m.group(1) if m else ""
    m = re.search(r'<script src="assets/js/site\.js\?v=[^"]+"></script>\n(.*?)</body>', h, re.S)
    depois = m.group(1) if m else ""
    novo = molde.pagina(head, corpo, atual, depois)
    if novo != h:
        caminho.write_text(novo, encoding="utf-8", newline="\n")
        return True
    return False


if __name__ == "__main__":
    alvos = [Path(a) for a in sys.argv[1:]] or sorted(PUBLIC.glob("*.html"))
    feitas = [p.name for p in alvos if reaplicar(p)]
    print(f"{len(feitas)} página(s) reconstruída(s): " + ", ".join(feitas))
