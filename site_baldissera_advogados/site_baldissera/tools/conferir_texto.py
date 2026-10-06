"""
Confere que o redesenho (06/10/2026) não mudou o texto de uma página.

Compara o texto visível do CONTEÚDO da página na última versão gravada no git (HEAD) com o
arquivo atual. Fica de fora o que é moldura (cabeçalho, menu, barra de contato, rodapé, botões
flutuantes, scripts), que mudou de propósito. Imprime cada trecho removido, acrescentado ou
trocado; quem revisa decide se a diferença é só moldura (aceitável) ou texto (não aceitável).

Uso:
  python conferir_texto.py public/advogados.html [public/contato.html ...]
Saída 0 = texto idêntico; 1 = há diferenças (listadas).
"""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

RAIZ_GIT = Path(__file__).resolve().parents[3]          # .../site-baldissera
SITE = Path(__file__).resolve().parents[1]              # .../site_baldissera


def conteudo_antigo(h: str) -> str:
    h = re.sub(r'(?is)<div class="contact-bar".*?(?=<header)', " ", h)     # barra de contato: até o cabeçalho
    h = re.sub(r"(?is)<(script|style|head|header|footer|noscript)\b[^>]*>.*?</\1>", " ", h)
    h = re.sub(r'(?is)<a[^>]*class="wa-float[^"]*".*?</a>', " ", h)
    return h


def conteudo_novo(h: str) -> str:
    m = re.search(r"(?is)<main[^>]*>(.*)</main>", h)
    h = m.group(1) if m else h
    return re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)


def palavras(h: str) -> list:
    h = re.sub(r"<br\s*/?>", " ", h)
    return html.unescape(re.sub(r"<[^>]+>", " ", h)).split()


def comparar(arq: Path) -> int:
    rel = arq.resolve().relative_to(RAIZ_GIT)
    r = subprocess.run(["git", "-C", str(RAIZ_GIT), "show", f"HEAD:{rel.as_posix()}"], capture_output=True)
    if r.returncode:
        print(f"• {arq.name}: página nova (não existe na versão gravada)"); return 0
    antes = palavras(conteudo_antigo(r.stdout.decode("utf-8")))
    depois = palavras(conteudo_novo(arq.read_text(encoding="utf-8")))
    ops = [o for o in difflib.SequenceMatcher(a=antes, b=depois, autojunk=False).get_opcodes() if o[0] != "equal"]
    if not ops:
        print(f"✓ {arq.name}: texto idêntico ({len(antes)} palavras)"); return 0
    print(f"△ {arq.name}: {len(ops)} diferença(s) — {len(antes)} palavras antes, {len(depois)} depois")
    for op, a1, a2, b1, b2 in ops:
        print(f"   {op}: «{' '.join(antes[a1:a2])[:300]}» → «{' '.join(depois[b1:b2])[:300]}»")
    return 1


if __name__ == "__main__":
    codigo = 0
    for a in sys.argv[1:]:
        p = Path(a)
        if not p.is_absolute():
            p = (SITE / a) if (SITE / a).exists() else Path.cwd() / a
        codigo |= comparar(p)
    sys.exit(codigo)
