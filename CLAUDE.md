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

## Publicação (desde 25/09/2026)

- **Sem numeração** de publicação. A lista em `public/publicacoes.html` recebe cada nova publicação logo abaixo do marcador `<!-- NOVAS-PUBLICACOES ... -->` (a mais nova no topo).
- **Lista por área (27/09/2026)**: as 7 pílulas de `publicacoes.html` são botões que filtram os cartões (`class="pub-card" data-area data-superior data-data`); "Tribunais Superiores" mostra as análises de julgado STF/STJ agrupadas por matéria; a ordem é por data. `area` do JSON tem de ser uma das 7 (`publicar.py: AREAS`); `superior` é detectado pelo conteúdo. Retroativo: `tools/publicador/classificar_existentes.py`.
- **Ilustração (27/09/2026)**: cada publicação tem uma ilustração editorial gerada pelo agente `baldissera-diretor-arte` (Canva; método baoyu-cover-image; checklist Provimento 205) gravada em `PAINEL-PUBLICACAO\IMAGENS\<slug>.png` (fora do git). O publicador a usa como fundo das 3 capas (`capa.py`, marca vetorial em `assets/images/marca/`) e põe a **capa quadrada ao lado do título, estilo blog** (`.pub-hero-grid`, `publicacoes/<slug>-lateral.jpg`). **REGRA do Dr. Luiz (27/09/2026)**: capa lateral + **@luizhbaldissera** e **@baldisseraadvocacia** em toda publicação (bloco de compartilhar e rodapé das capas; `publicar.py: INSTAGRAM`). Retroativo: `tools/publicador/imagens_existentes.py`. Campos `imagem`/`imagem_alt` em `FORMATO.md`. ⚠ `capa.py` (Edge headless) só funciona rodando pelo PowerShell — pelo Bash em sandbox falha em silêncio.
- **Publicador**: `site_baldissera_advogados/site_baldissera/tools/publicador/publicar.py` transforma uma publicação em JSON (`FORMATO.md`, ao lado) em página no padrão do site, encaixa o cartão e o sitemap; com `--push` envia (vai ao ar). Nunca editar à mão o HTML que ele gera: corrige-se o JSON e gera-se de novo.
- **Página "Publicar no site"** (Claude, só advogados convidados como Editor): https://claude.ai/artifact/Bj4RTL3JUVUgESYEPV6MZw — fila `fila`. Fonte: `PAINEL-PUBLICACAO/publicar-no-site.html` (fora do git).
- **Tarefas**: `publicador-site-baldissera` (a cada 30 min, 7h–23h; modo em `PAINEL-PUBLICACAO/MODO.txt`: `TESTE` ou `NO AR`) e `minutas-publicacoes-site` (dia sim, dia não, 6h; põe minuta na fila como "aguardando"). A rotina antiga da nuvem "Publicacoes diarias baldissera" foi pausada.
- **Exceção à revisão do Dr. Luiz, decidida por ele em 25/09/2026, só para o site**: publicação aprovada por um advogado na página vai ao ar sem passar por ele; quem aprova responde pelo conteúdo. Minuta automática e pedido `/publicar` continuam esperando o "publica" do Dr. Luiz.
- **Cópia de trabalho fora do OneDrive**: `C:\Users\LuizH\site-baldissera` (evita arquivo truncado pela sincronização). O publicador faz `pull` na cópia do OneDrive depois de publicar, se ela estiver limpa.
