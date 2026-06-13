#!/bin/bash
set -euo pipefail

# Hook de SessionStart para Claude Code na web.
# Instala ferramentas de validacao para um site estatico (HTML + CSS):
#   - html-validate : validacao de marcacao HTML
#   - stylelint     : lint do CSS (assets/css/style.css)
#   - linkinator    : checagem de links quebrados nas paginas
#
# Roda apenas no ambiente remoto. Em maquina local nao faz nada.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Instalacao global e idempotente. O estado do container e cacheado apos o
# hook, entao a instalacao global persiste entre invocacoes da sessao.
npm install -g --no-fund --no-audit \
  html-validate@9 \
  stylelint@16 \
  stylelint-config-standard@36 \
  linkinator@6

# Permite que stylelint resolva o preset global (stylelint-config-standard)
# e que os binarios fiquem acessiveis durante toda a sessao.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export NODE_PATH=\"$(npm root -g)\"" >> "$CLAUDE_ENV_FILE"
fi

SITE_DIR="site_baldissera_advogados/site_baldissera/public"
echo "Ferramentas de validacao instaladas: html-validate, stylelint, linkinator"
echo "Comandos de validacao do site:"
echo "  html-validate \"$SITE_DIR/**/*.html\""
echo "  stylelint \"$SITE_DIR/assets/css/style.css\""
echo "  linkinator \"$SITE_DIR\" --config linkinator.config.json"
