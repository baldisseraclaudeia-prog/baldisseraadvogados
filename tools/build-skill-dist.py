#!/usr/bin/env python3
"""
Gera a versao de DISTRIBUICAO do agente de pecas academicas a partir da skill
interna, removendo tudo que e especifico do escritorio (nome da casa, nomes e
inscricoes OAB de advogados, referencias a outras skills baldissera-*).

Fonte unica de verdade: .claude/skills/baldissera-civil-academico/
Saida:                  dist/pecas-academicas-civil/ + dist/pecas-academicas-civil.zip

Uso:  python3 tools/build-skill-dist.py
"""
import re
import shutil
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / ".claude" / "skills" / "baldissera-civil-academico"
DESTINO = RAIZ / "dist" / "pecas-academicas-civil"
ZIP = RAIZ / "dist" / "pecas-academicas-civil.zip"

NOME_DIST = "pecas-academicas-civil"

# (padrao, substituicao, obrigatorio) — obrigatorio=True falha o build se nao casar
SUBSTITUICOES = [
    (
        "name: baldissera-civil-academico",
        f"name: {NOME_DIST}",
        True,
    ),
    (
        """- **NÃO usa timbre, OAB ou assinatura do escritório.** Peça de faculdade não
  leva papel timbrado da Baldissera Advogados nem número de inscrição de
  advogado real. Ver `references/formatacao-academica.md`.""",
        """- **NÃO usa timbre de escritório nem OAB real.** Peça de faculdade não leva
  papel timbrado de banca de advocacia existente nem número de inscrição de
  advogado real. Ver `references/formatacao-academica.md`.""",
        True,
    ),
    (
        "### 1. Trava de citação (regra da casa — não negociável)",
        "### 1. Trava de citação (não negociável)",
        True,
    ),
    (
        """1. **Nunca aplicar o timbre da Baldissera Advogados** (cabeçalho "BALDISSERA /
   A D V O G A D O S", rodapé com endereços das unidades e telefone
   institucional) em trabalho acadêmico. O timbre identifica escritório real
   em documento que não é dele.
2. **Nunca usar número de OAB real** — nem o de Luiz Henrique Baldissera
   (OAB/PR 55.717; OAB/SC 78.938-A), nem o de Anderson Spanhol
   (OAB/PR 96.871), nem o de qualquer advogado existente. Assinar peça
   acadêmica com inscrição alheia é problema ético, não detalhe de forma.""",
        """1. **Nunca aplicar timbre de escritório real** — cabeçalho, logotipo, rodapé
   com endereços ou telefone de banca existente — em trabalho acadêmico. O
   timbre identifica escritório real em documento que não é dele.
2. **Nunca usar número de OAB real**, de nenhum advogado existente. Assinar
   peça acadêmica com inscrição alheia é problema ético, não detalhe de forma.""",
        True,
    ),
    (
        """3. Indique o encaminhamento: matéria criminal de homicídio → skill
   `baldissera-homicidio-hc`; demais ramos → dizer francamente que falta agente
   próprio, em vez de improvisar.""",
        """3. Indique o encaminhamento: diga francamente que o caso pede um agente
   próprio daquele ramo, em vez de improvisar.""",
        True,
    ),
    ("(regra fixa da casa)", "(regra fixa)", False),
    ("**Regra de versionamento (regra fixa da casa):**", "**Regra de versionamento:**", False),
]

# Termos que NAO podem sobrar na versao distribuida
PROIBIDOS = [
    r"Baldissera",
    r"baldissera-",
    r"OAB/PR\s*\d",
    r"OAB/SC\s*\d",
    r"Luiz Henrique",
    r"Anderson Spanhol",
    r"regra da casa",
    r"regra fixa da casa",
]


def main() -> None:
    if not ORIGEM.is_dir():
        raise SystemExit(f"origem nao encontrada: {ORIGEM}")

    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    DESTINO.mkdir(parents=True)

    arquivos = sorted(p for p in ORIGEM.rglob("*.md") if p.is_file())
    nao_casadas = []

    for origem in arquivos:
        rel = origem.relative_to(ORIGEM)
        if rel.name == "INSTALACAO.md":
            continue  # substituido pelo LEIA-ME.md proprio da distribuicao
        texto = origem.read_text(encoding="utf-8")
        for alvo, troca, obrigatorio in SUBSTITUICOES:
            if alvo in texto:
                texto = texto.replace(alvo, troca)
            elif obrigatorio:
                nao_casadas.append((rel.as_posix(), alvo.splitlines()[0][:60]))
        destino = DESTINO / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")

    # substituicao obrigatoria precisa casar em ao menos um arquivo
    contagem = {alvo: 0 for alvo, _, obrig in SUBSTITUICOES if obrig}
    for origem in arquivos:
        t = origem.read_text(encoding="utf-8")
        for alvo in contagem:
            if alvo in t:
                contagem[alvo] += 1
    faltando = [a.splitlines()[0][:60] for a, n in contagem.items() if n == 0]
    if faltando:
        raise SystemExit("substituicao obrigatoria nao casou em nenhum arquivo:\n  " + "\n  ".join(faltando))

    # LEIA-ME proprio da distribuicao
    leiame = RAIZ / "tools" / "dist-LEIA-ME.md"
    if not leiame.is_file():
        raise SystemExit(f"falta o LEIA-ME da distribuicao: {leiame}")
    shutil.copy(leiame, DESTINO / "LEIA-ME.md")

    # auditoria: nada especifico do escritorio pode sobrar
    vazamentos = []
    for p in sorted(DESTINO.rglob("*.md")):
        t = p.read_text(encoding="utf-8")
        for padrao in PROIBIDOS:
            for m in re.finditer(padrao, t, re.IGNORECASE):
                linha = t[: m.start()].count("\n") + 1
                vazamentos.append(f"{p.relative_to(DESTINO)}:{linha}: {m.group(0)}")
    if vazamentos:
        raise SystemExit("VAZAMENTO na versao distribuida:\n  " + "\n  ".join(vazamentos))

    # zip
    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DESTINO.rglob("*")):
            if p.is_file():
                z.write(p, Path(NOME_DIST) / p.relative_to(DESTINO))

    gerados = sorted(p.relative_to(DESTINO).as_posix() for p in DESTINO.rglob("*") if p.is_file())
    print(f"OK — {len(gerados)} arquivos em {DESTINO.relative_to(RAIZ)}")
    for g in gerados:
        print("   ", g)
    print(f"zip: {ZIP.relative_to(RAIZ)} ({ZIP.stat().st_size} bytes)")
    print("auditoria: nenhum termo do escritorio na versao distribuida")


if __name__ == "__main__":
    main()
