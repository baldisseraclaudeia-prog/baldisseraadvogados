"""Gera as capas das publicações já no ar e aponta a imagem de compartilhamento delas para a capa.
Lê título, área e autor da própria página; não altera o texto de nenhuma publicação."""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import publicar as P
import capa

NOMES = {v["nome"]: k for k, v in P.AUTORES.items()}


def dados(f: Path) -> dict:
    s = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
    titulo = re.sub(r"\s+", " ", s.find("h1").get_text(" ", strip=True))
    meta = s.select_one(".post-meta")
    if meta:                                   # modelo das publicações Nº 3 a 7
        area = meta.find("span").get_text(strip=True)
    else:                                      # modelo "PUBLICAÇÃO · ÁREA · MÊS"
        kick = s.find(string=re.compile(r"PUBLICAÇÃO\s*·"))
        area = kick.split("·")[1].strip()
    area = area.title() if area.isupper() else area
    texto = s.get_text(" ", strip=True)
    autor = next((k for nome, k in NOMES.items() if nome in texto), "luiz")
    # o primeiro nome de advogado que aparece depois do título é o autor
    pos = {k: texto.find(nome, texto.find(titulo[:30])) for nome, k in NOMES.items()}
    pos = {k: v for k, v in pos.items() if v >= 0}
    if pos:
        autor = min(pos, key=pos.get)
    return {"titulo": titulo, "area": area, "autor": autor, "corpo": [{"tipo": "paragrafo", "texto": "x"}],
            "subtitulo": "x", "resumo": "x", "slug": f.stem, "sobrescrever": True}


def main():
    destino = P.PUB / "assets" / "images" / "capas"
    for f in sorted(P.PUB.glob("publicacao-*.html")):
        p = P.preparar(dados(f))
        if not (destino / f"{p['_slug']}-og.png").exists():
            capa.gerar(p, ["og", "quadrado", "vertical"], destino)
        s = f.read_text(encoding="utf-8")
        nova = f"{P.BASE}/assets/images/capas/{p['_slug']}-og.png"
        s2 = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', rf"\g<1>{nova}\g<2>", s)
        if s2 != s:
            f.write_text(s2, encoding="utf-8", newline="\n")
        print(json.dumps({"pagina": f.name, "titulo": p["titulo"][:70], "area": p["area"], "autor": p["autor"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
