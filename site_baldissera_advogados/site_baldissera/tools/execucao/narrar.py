"""
Gera a narração (voz sintética, ElevenLabs) de cada julgado explicado a partir do roteiro aprovado em
julgados/<id>.json (campo audio.roteiro), com a voz, o modelo e a velocidade de narracao.json
(escolha do Dr. Luiz, 09/10/2026). Grava o mp3 em public/<audio.narracao.arquivo> e preenche no JSON
hash, voz, modelo, data, duração e caracteres. Depois, rodar gerar_explicada.py para o tocador aparecer.

Só gera o que ainda não tem áudio ou cujo roteiro mudou (o hash do roteiro fica em narracao.roteiro_hash).
A chave fica fora do repositório, em ~/.config/baldissera/elevenlabs.key.

Uso:  python3.12 tools/execucao/narrar.py [id ...] [--forcar]
"""
import hashlib
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import comum  # noqa: E402

CONFIG = json.loads((AQUI / "narracao.json").read_text(encoding="utf-8"))
CHAVE = Path.home() / ".config" / "baldissera" / "elevenlabs.key"
KBPS = int(re.search(r"_(\d+)$", CONFIG["output_format"]).group(1))   # mp3_44100_64 → 64 kbps constantes


def sintetizar(texto: str) -> bytes:
    corpo = json.dumps({"text": texto, "model_id": CONFIG["modelo"], "voice_settings": CONFIG["voice_settings"]}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{CONFIG['voz_id']}?output_format={CONFIG['output_format']}",
        data=corpo, method="POST",
        headers={"xi-api-key": CHAVE.read_text().strip(), "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def narrar(arq: Path, forcar: bool) -> str:
    texto = arq.read_text(encoding="utf-8")
    j = json.loads(texto)
    a = j["audio"]
    roteiro, nar = a["roteiro"].strip(), a["narracao"]
    h_rot = hashlib.sha256(roteiro.encode()).hexdigest()[:16]
    destino = comum.PUBLIC / nar["arquivo"]
    if destino.exists() and nar.get("roteiro_hash") == h_rot and not forcar:
        return f"{j['id']}: já narrado, roteiro sem mudança"
    mp3 = sintetizar(roteiro)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(mp3)
    novo = {"arquivo": nar["arquivo"], "hash": hashlib.sha256(mp3).hexdigest(), "roteiro_hash": h_rot,
            "voz_id": CONFIG["voz_id"], "modelo": CONFIG["modelo"], "velocidade": CONFIG["voice_settings"]["speed"],
            "gerado_em": date.today().isoformat(), "duracao_s": round(len(mp3) * 8 / (KBPS * 1000)),
            "caracteres": len(roteiro)}
    linha = re.compile(r'^(\s*)"narracao": \{.*\},?$', re.M)
    m = linha.search(texto)
    assert m, f"{arq.name}: linha da narração não encontrada"
    fim = "," if m.group(0).rstrip().endswith(",") else ""
    texto = texto[:m.start()] + f'{m.group(1)}"narracao": {json.dumps(novo, ensure_ascii=False)}{fim}' + texto[m.end():]
    json.loads(texto)
    arq.write_text(texto, encoding="utf-8")
    return f"{j['id']}: {novo['duracao_s']} s, {novo['caracteres']} caracteres → {nar['arquivo']}"


if __name__ == "__main__":
    args = sys.argv[1:]
    forcar = "--forcar" in args
    ids = [x for x in args if not x.startswith("--")]
    for arq in sorted((AQUI / "julgados").glob("*.json")):
        if ids and arq.stem not in ids:
            continue
        print(narrar(arq, forcar))
