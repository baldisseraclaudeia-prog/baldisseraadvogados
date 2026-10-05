"""Fichas técnicas (dados estruturados schema.org) das páginas institucionais — SEO de 04/10/2026.

Fonte única dos dados das unidades e dos advogados que vão nas fichas:
  - index.html   -> o escritório (LegalService, @id #escritorio), com a sede e as unidades;
  - contato.html -> uma ficha por unidade, com endereço completo e CEP;
  - perfil-*.html -> uma ficha "Pessoa" por advogado, com OAB, áreas e unidade.
As publicações apontam para estas fichas (publicar.py: ESCRITORIO_ID e pessoa_ref).

Mudou endereço, CEP, telefone ou unidade? Corrija aqui e no texto visível de contato.html,
e rode de novo. Idempotente: troca a ficha existente, nunca duplica.
Uso:  python fichas_site.py [--so-conferir]
"""
import argparse, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI / "publicador"))
import publicar as P

BASE, PUB = P.BASE, P.PUB
TELEFONE = "+55-45-99102-9806"
EMAIL = "contato@baldisseraadvogados.com.br"
IMAGEM = f"{BASE}/assets/images/og-default.png"
INSTAGRAM_ESCRITORIO = "https://www.instagram.com/baldisseraadvocacia/"

# CEPs conferidos na base pública dos Correios (ViaCEP) e decididos pelo Dr. Luiz em 04/10/2026;
# os mesmos do timbrado (LOGO\MODELO_PETICAO_BALDISSERA.docx) e do Perfil da Empresa no Google.
# Cascavel: 85807-435 (nº 1.631, lado ímpar, Recanto Tropical; o antigo 85805-002 era o lado par).
# Porto Belo: 88211-002 (a avenida no Perequê; o antigo 88210-000 era o CEP geral da cidade).
UNIDADES = {
    "cascavel": dict(rua="Av. Pres. Juscelino Kubitschek, 1.631", bairro="Recanto Tropical",
                     cidade="Cascavel", uf="PR", cep="85807-435"),
    "porto-alegre": dict(rua="Rua Mostardeiro, 366, sala 501", bairro="Moinhos de Vento",
                         cidade="Porto Alegre", uf="RS", cep="90430-000"),
    "foz-do-iguacu": dict(rua="Av. Pedro Basso, 744", bairro="Polo Centro",
                          cidade="Foz do Iguaçu", uf="PR", cep="85863-756"),
    "porto-belo": dict(rua="Av. Senador Atílio Fontana, 2.085, sala 02", bairro="Perequê",
                       cidade="Porto Belo", uf="SC", cep="88211-002"),
}
SEDE = "cascavel"

# Advogados com página própria: áreas = a lista "Principais frentes de trabalho" do perfil.
PERFIS = {
    "luiz": dict(arquivo="perfil-luiz.html", unidade="cascavel",
                 foto="assets/images/luiz-henrique-baldissera.jpg",
                 sameAs=["https://www.instagram.com/luizhbaldissera/"],
                 areas=["Direito Penal", "Recursos aos Tribunais Superiores", "Execução Penal",
                        "Sistema Penitenciário Federal", "Prova Digital", "Investigação Defensiva"]),
    "charys": dict(arquivo="perfil-charys.html", unidade="cascavel",
                   foto="assets/images/charys-baldissera.jpg", sameAs=[],
                   areas=["Família", "Direito Empresarial", "Sucessões", "Planejamento Sucessório",
                          "Direito Imobiliário", "Usucapião", "Inventário e Partilha"]),
    "karla": dict(arquivo="perfil-karla.html", unidade="porto-alegre",
                  foto="assets/images/karla-sampaio.jpg", sameAs=[],
                  areas=["Direito Penal", "Tribunal do Júri", "Direito Penal Econômico",
                         "Direito Penal Empresarial", "Prerrogativas da Advocacia"]),
}
AREAS_ESCRITORIO = ["Direito Penal", "Recursos aos Tribunais Superiores", "Execução Penal",
                    "Direito Imobiliário", "Direito Civil", "Direito de Família e Sucessões",
                    "Direito Ambiental", "Assessoria em Leilões"]

RE_FICHA = re.compile(r'<script type="application/ld\+json">.*?</script>\n', re.S)


def unidade_id(chave):
    return f"{BASE}/contato#{chave}"


def endereco(u):
    return {"@type": "PostalAddress", "streetAddress": f"{u['rua']}, {u['bairro']}",
            "addressLocality": u["cidade"], "addressRegion": u["uf"], "postalCode": u["cep"],
            "addressCountry": "BR"}


def escritorio():
    return {"@context": "https://schema.org", "@type": "LegalService", "@id": P.ESCRITORIO_ID,
            "name": "Baldissera Advogados", "url": BASE, "logo": P.LOGO, "image": IMAGEM,
            "telephone": TELEFONE, "email": EMAIL, "sameAs": [INSTAGRAM_ESCRITORIO],
            "address": endereco(UNIDADES[SEDE]),
            "founder": {"@id": f"{BASE}/perfil-luiz#pessoa"},
            "department": [{"@id": unidade_id(k)} for k in UNIDADES],
            "areaServed": "BR", "serviceType": AREAS_ESCRITORIO}


def unidades():
    nos = [{"@type": "LegalService", "@id": P.ESCRITORIO_ID, "name": "Baldissera Advogados", "url": BASE}]
    for k, u in UNIDADES.items():
        nos.append({"@type": "LegalService", "@id": unidade_id(k), "name": "Baldissera Advogados",
                    "url": f"{BASE}/contato", "image": IMAGEM, "telephone": TELEFONE, "email": EMAIL,
                    "address": endereco(u), "parentOrganization": {"@id": P.ESCRITORIO_ID},
                    "areaServed": "BR"})
    return {"@context": "https://schema.org", "@graph": nos}


def pessoa(chave, descricao):
    cfg, a = PERFIS[chave], P.AUTORES[chave]
    p = {"@context": "https://schema.org", **P.pessoa_ref(chave)}
    p.update({"description": descricao, "image": f"{BASE}/{cfg['foto']}", "knowsAbout": cfg["areas"],
              "workLocation": {"@id": unidade_id(cfg["unidade"])}})
    if cfg["sameAs"]:
        p["sameAs"] = cfg["sameAs"]
    assert a["perfil"] == cfg["arquivo"], f"perfil de {chave} diverge de publicar.py: AUTORES"
    return p


def gravar(arquivo, dados, conferir):
    arq = PUB / arquivo
    s = antes = arq.read_text(encoding="utf-8")
    ficha = P.json_ld(dados) + "\n"
    s = RE_FICHA.sub("", s)
    s = s.replace('<script defer src="/_vercel/insights/script.js"></script>', ficha + '<script defer src="/_vercel/insights/script.js"></script>', 1)
    if ficha not in s:
        raise SystemExit(f"{arquivo}: não achei onde pôr a ficha")
    if s != antes and not conferir:
        arq.write_text(s, encoding="utf-8", newline="\n")
    print(f"{'(conferência) ' if conferir else ''}{arquivo}: {'ficha gravada' if s != antes else 'já estava em dia'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-conferir", action="store_true")
    c = ap.parse_args().so_conferir
    gravar("index.html", escritorio(), c)
    gravar("contato.html", unidades(), c)
    for chave, cfg in PERFIS.items():
        s = (PUB / cfg["arquivo"]).read_text(encoding="utf-8")
        descricao = P.html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
        gravar(cfg["arquivo"], pessoa(chave, descricao), c)


if __name__ == "__main__":
    main()
