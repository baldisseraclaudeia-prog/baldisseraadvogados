"""
Publicações recentes na página inicial — desde 06/10/2026 é um atalho para vitrines.py, que
atualiza a manchete e o "Você sabia?" da home, as publicações de cada página de área e o índice
da busca. Mantido com este nome porque rotinas e o publicador antigo o chamam.

    python home_recentes.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vitrines  # noqa: E402

PUB = vitrines.PUB


def atualizar(pub: Path = PUB) -> bool:
    """Atualiza todas as vitrines. Devolve True se algum arquivo mudou."""
    return bool(vitrines.atualizar_tudo(pub))


if __name__ == "__main__":
    mudou = atualizar()
    print("vitrines atualizadas" if mudou else "vitrines já estavam em dia (ou sem marcadores)")
    sys.exit(0)
