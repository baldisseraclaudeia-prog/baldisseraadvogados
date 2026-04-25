# Contexto para assistentes de IA — Baldissera Advogados

> Este arquivo orienta assistentes de IA (Claude Code, Cursor, Cowork, etc.) sobre o projeto. **Sempre leia primeiro `site_baldissera_advogados/site_baldissera/docs/BRIEFING.md` para o panorama completo.**

## Stack

Site estático puro (HTML + CSS, sem framework, sem build). Servido pela Vercel a partir do diretório `site_baldissera_advogados/site_baldissera/public/` (Root Directory configurada no painel Vercel).

## Domínio em produção

`https://www.baldisseraadvogados.com.br/` (apex redireciona 307 → www).

## Workflow de edição

- Editar HTMLs em `site_baldissera_advogados/site_baldissera/public/`.
- CSS único em `site_baldissera_advogados/site_baldissera/public/assets/css/style.css`.
- Imagens em `site_baldissera_advogados/site_baldissera/public/assets/images/`.
- Push para `main` aciona deploy automático da Vercel (~60-90s).

## Convenções editoriais

- **Idioma:** português do Brasil.
- **Tom:** sóbrio, técnico, sem auto-elogio mercadológico.
- **Sem emojis** em conteúdo do site.
- **Conformidade Provimento OAB 205/2021:** evitar superlativos, comparações nominais, promessas de resultado, menção a casos concretos ou clientes.

## Documentos de referência neste repo

- `site_baldissera_advogados/site_baldissera/docs/BRIEFING.md` — **comece por aqui**. Panorama completo: identidade, stack, arquitetura, equipe, histórico, pendências, convenções.
- `site_baldissera_advogados/site_baldissera/docs/PENDENCIAS.md` — itens em aberto, com seção atualizada do que já foi resolvido.
- `site_baldissera_advogados/site_baldissera/docs/DEPLOY.md` — guia histórico de deploy (parcialmente desatualizado; site já está no ar).
- `site_baldissera_advogados/site_baldissera/docs/README.md` — inventário de arquivos.


## Módulo editorial — geração de publicações

Para gerar uma nova publicação para a aba `/publicacoes` (a partir de julgado, ensaio dogmático ou tema livre), seguir o protocolo em `site_baldissera_advogados/site_baldissera/docs/editorial/`:

- `PADRAO-EDITORIAL.md` — anatomia visual, tom, vedações Provimento 205, convenções de citação.
- `TEMPLATE.html` — template HTML pronto com marcadores `{{...}}`.
- `INSTRUCOES.md` — workflow operacional passo a passo, princípios invioláveis e exemplos.

Espelho de referência: `site_baldissera_advogados/site_baldissera/public/publicacao-cadeia-de-custodia.html`.

## Convenção de manutenção crítica

Ao editar arquivos da pasta sincronizada com OneDrive (`C:\Users\LuizH\OneDrive\...`), **trabalhar primeiro em clone do sandbox** e sincronizar com `cp` em batch. Edição direta na pasta OneDrive durante sync ativa pode truncar arquivos (já aconteceu uma vez nesta base de código).
