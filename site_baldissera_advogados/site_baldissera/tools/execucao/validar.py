"""
Valida os julgados explicados (tools/execucao/julgados/*.json) antes de gerar a página.
Sai com 1 e lista os erros; a geração em modo "publicar" para se houver erro.

Regras: formato em FORMATO-JULGADO.md; régua ética do Provimento 205 e da casa (PADRAO-EDITORIAL §5,
§13.9): nada dirigido a quem precisa de advogado, nada de captação, nada de promessa, nada de
superlativo, nada de marcador de lacuna em texto que vai ao ar.

Uso:  python3.12 tools/execucao/validar.py            # todos
      python3.12 tools/execucao/validar.py tema-1155   # um
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit("use ~/.local/bin/python3.12")

AQUI = Path(__file__).resolve().parent
JULGADOS = AQUI / "julgados"
PUBLIC = AQUI.parents[1] / "public"   # AQUI = tools/execucao → tools → raiz

MATERIAS = ("progressao", "remicao", "detracao", "livramento", "indulto", "falta-grave", "federal", "condicoes", "multa")
SITUACOES = ("rascunho", "aguarda-selagem", "publicar")
SITUACOES_PUBLICAS = ("em vigor", "afetado", "repercussão geral reconhecida", "aguardando publicação", "pendente (ADI)",
                      "sobrestado", "superado")
DOMINIOS = ("stj.jus.br", "portal.stf.jus.br", "jurisprudencia.stf.jus.br", "planalto.gov.br", "legis.senado.leg.br")
OBRIGATORIOS = ("id", "materia", "ordem", "situacao", "pendente", "titulo", "alcance", "parabola", "exemplo", "decidiu",
                "limites", "documento", "selagem", "relacionados", "audio")
SELAGEM_OBRIGATORIA = ("tribunal", "orgao", "classe", "tese_verbatim", "url_oficial", "situacao_publica", "verificado_em",
                       "verificado_por")
MARCADORES = re.compile(r"\[(CONFIRMAR|COMPLETAR|SECUNDÁRIA|data\])")
# vedações da régua (§5 do plano): segunda pessoa, captação, autoelogio, gancho emocional, frequência sem prova
VEDADOS = [(re.compile(r"\bvoc[êe]s?\b", re.I), "segunda pessoa (\"você\")"),
           (re.compile(r"\bseu familiar|\bsua fam[íi]lia", re.I), "dirigido à família"),
           (re.compile(r"procure (um|o) advogado|fale conosco|entre em contato|agende|podemos revisar", re.I), "verbo de captação"),
           (re.compile(r"\bespecializad[oa]s?\b|refer[êe]ncia em|o melhor|o maior|l[íi]der em", re.I), "autoqualificação"),
           (re.compile(r"\besperan[çc]a\b", re.I), "\"esperança\" como gancho"),
           (re.compile(r"\bcostumam?\b|na maioria dos casos|quase sempre", re.I), "frequência sem demonstração"),
           (re.compile(r"n[ãa]o perca|cada dia conta|urgente", re.I), "urgência"),
           (re.compile(r"preso federal|pres[íi]dio federal para", re.I), "léxico vedado da casa"),
           (re.compile(r"\btem direito\b(?![^.]*\bpode\b)", re.I), "\"tem direito\" sem condição (usar \"pode\")")]


def textos_publicos(j: dict):
    yield "titulo", j.get("titulo", "")
    yield "alcance", j.get("alcance", "")
    yield "parabola", j.get("parabola", "")
    ex = j.get("exemplo") or {}
    for k in ("premissas", "conta", "texto"):
        yield f"exemplo.{k}", ex.get(k, "") or ""
    yield "decidiu", j.get("decidiu", "")
    for i, l in enumerate(j.get("limites") or []):
        yield f"limites[{i}]", l
    yield "documento", j.get("documento", "")
    for k in ("em_jogo", "ate_la"):
        if j.get(k):
            yield k, j[k]
    yield "selagem.nota_situacao", (j.get("selagem") or {}).get("nota_situacao", "") or ""
    yield "audio.roteiro", (j.get("audio") or {}).get("roteiro", "") or ""


def validar(caminho: Path) -> list:
    erros = []
    try:
        j = json.loads(caminho.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"{caminho.name}: JSON inválido ({e})"]
    e = lambda m: erros.append(f"{caminho.name}: {m}")
    for k in OBRIGATORIOS:
        if k not in j:
            e(f"falta o campo \"{k}\"")
    if erros:
        return erros
    if j["id"] != caminho.stem:
        e(f"id \"{j['id']}\" diferente do nome do arquivo")
    if j["materia"] not in MATERIAS:
        e(f"materia \"{j['materia']}\" fora de {MATERIAS}")
    if j["situacao"] not in SITUACOES:
        e(f"situacao \"{j['situacao']}\" fora de {SITUACOES}")
    publicar = j["situacao"] == "publicar"
    pendente = bool(j.get("pendente"))
    for k in ("titulo", "alcance", "parabola", "decidiu", "documento"):
        if not (j.get(k) or "").strip():
            e(f"\"{k}\" vazio")
    if len(j["titulo"]) > 140:
        e(f"título com {len(j['titulo'])} caracteres (máximo 140)")
    if not j["parabola"].lstrip().startswith("Imagine"):
        e("parábola não abre com \"Imagine\"")
    np = len(j["parabola"].split())
    if not 60 <= np <= 150:
        e(f"parábola com {np} palavras (80–130 esperadas)")
    if not pendente:
        ex = j.get("exemplo") or {}
        if not (ex.get("premissas") and ex.get("conta") and ex.get("texto")):
            e("exemplo precisa de premissas, conta e texto")
    if len(j.get("limites") or []) < 1:
        e("limites: ao menos um item (o que prejudica)")
    s = j["selagem"]
    for k in SELAGEM_OBRIGATORIA:
        if not (s.get(k) or "").strip():
            e(f"selagem.{k} vazio")
    if s.get("url_oficial") and not (s["url_oficial"].startswith("https://") and any(d in s["url_oficial"] for d in DOMINIOS)):
        e(f"selagem.url_oficial fora dos domínios oficiais: {s.get('url_oficial')}")
    if s.get("tese_verbatim") and len(s["tese_verbatim"]) < 40:
        e("selagem.tese_verbatim curta demais")
    if s.get("situacao_publica") not in SITUACOES_PUBLICAS:
        e(f"selagem.situacao_publica \"{s.get('situacao_publica')}\" fora de {SITUACOES_PUBLICAS}")
    try:
        if date.fromisoformat(s.get("verificado_em", "")) > date.today():
            e("selagem.verificado_em no futuro")
    except ValueError:
        e("selagem.verificado_em não é data ISO (AAAA-MM-DD)")
    rel = j.get("relacionados") or {}
    if rel.get("publicacao") and not (PUBLIC / rel["publicacao"]).exists():
        e(f"relacionados.publicacao não existe em public/: {rel['publicacao']}")
    rot = (j.get("audio") or {}).get("roteiro") or ""
    if len(rot) > 1600:
        e(f"audio.roteiro com {len(rot)} caracteres (máximo 1.600)")
    nar = ((j.get("audio") or {}).get("narracao") or {})
    if nar.get("arquivo") and (PUBLIC / nar["arquivo"]).exists() and (PUBLIC / nar["arquivo"]).stat().st_size > 3_000_000:
        e("áudio da narração maior que 3 MB")
    # régua ética e marcadores só travam o que vai ao ar
    for campo, texto in textos_publicos(j):
        if not texto:
            continue
        m = MARCADORES.search(texto)
        if m and publicar:
            e(f"{campo}: marcador de lacuna \"{m.group(0)}\" em texto que vai ao ar")
        for rx, motivo in VEDADOS:
            if rx.search(texto):
                (e if publicar else lambda m: erros.append(f"{caminho.name}: (aviso) {m}"))(f"{campo}: {motivo}: \"{rx.search(texto).group(0)}\"")
    return erros


def todos(so: str = None) -> list:
    arqs = sorted(JULGADOS.glob("*.json")) if not so else [JULGADOS / f"{so}.json"]
    erros = []
    for a in arqs:
        erros += validar(a)
    return erros


if __name__ == "__main__":
    errs = todos(sys.argv[1] if len(sys.argv) > 1 else None)
    graves = [x for x in errs if "(aviso)" not in x]
    for x in errs:
        print(x)
    print(f"{len(graves)} erro(s), {len(errs) - len(graves)} aviso(s)")
    sys.exit(1 if graves else 0)
