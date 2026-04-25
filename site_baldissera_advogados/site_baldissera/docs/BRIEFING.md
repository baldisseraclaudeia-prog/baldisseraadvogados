# Briefing — Site Baldissera Advogados

> **Documento de contexto para Claude Projects e ferramentas de IA.**
> Cole o conteúdo deste arquivo (ou anexe o `.md` diretamente) na knowledge base de um Project. Futuras sessões de Claude conhecerão o site, o stack técnico, as convenções editoriais, o histórico recente e as pendências em aberto sem precisar reauditar do zero.
>
> **Última atualização:** 25/04/2026.

---

## 1. Identidade do projeto

- **Cliente / titular:** Luiz Henrique Baldissera — sócio titular da banca **Baldissera Advogados** (OAB/PR 55.717).
- **Domínio em produção:** `https://www.baldisseraadvogados.com.br/` (apex redireciona 307 → www).
- **Domínio de staging Vercel:** `https://baldisseraadvogados.vercel.app/` (continua funcionando em paralelo).
- **Repositório GitHub:** `github.com/baldisseraclaudeia-prog/baldisseraadvogados` (atenção: nome do repo é com `g`, não `c`).
- **Branch de produção:** `main`. Push direto, sem PR. Vercel auto-deploya em ~60-90s.
- **Conta Vercel:** plano Hobby. Scope: `luiz-henrique-baldisseras-projects`. Project: `baldisseraadvogados`.

## 2. Stack técnico

- **Stack:** site estático puro. **HTML + CSS** apenas. Sem framework, sem build step, sem JavaScript de aplicação. Vercel serve o conteúdo de `public/` como arquivos estáticos.
- **Tipografia:** Cormorant Garamond (Google Fonts), via `<link rel="preconnect">` + `<link rel="stylesheet">` no `<head>`.
- **Identidade visual:** paleta navy (`#0F172A`) + dourado (`#9B7B3A`) + ivory (`#F5F1E8` / `#FAFAF7`). Variáveis CSS no `:root` do `style.css`.
- **Formulários:** apontam para `https://formsubmit.co/contato@baldisseraadvogados.com.br` com captcha + honeypot. Não requer cadastro; basta confirmar uma vez o e-mail de ativação enviado pelo formsubmit no primeiro envio.
- **Deployment Protection:** **desabilitada**. Site é público.
- **Analytics:** **Vercel Web Analytics** habilitado (plano Hobby — 50.000 events/mês, 30 dias de histórico, sem cookies, sem banner LGPD necessário).
- **SSL:** automático pela Vercel.

## 3. Estrutura do repo

```
baldisseraadvogados/                                  ← repo root no GitHub
├── CLAUDE.md                                         ← contexto para AI tooling
└── site_baldissera_advogados/
    └── site_baldissera/
        ├── docs/
        │   ├── README.md
        │   ├── DEPLOY.md
        │   ├── PENDENCIAS.md
        │   ├── BRIEFING.md                           ← este arquivo
        │   └── editorial/
        │       ├── PADRAO-EDITORIAL.md               ← guia editorial completo
        │       ├── TEMPLATE.html                     ← template de publicação
        │       └── INSTRUCOES.md                     ← workflow operacional
        └── public/                                   ← Vercel Root Directory
            ├── index.html                            ← home
            ├── sobre.html
            ├── advogados.html
            ├── areas-de-atuacao.html
            ├── publicacoes.html                      ← hub editorial (peer cards)
            ├── publicacao-cadeia-de-custodia.html    ← Pub Nº 1 (jan/2026)
            ├── publicacao-prova-digital-sem-hash.html ← Pub Nº 2 (abr/2026)
            ├── contato.html                          ← form + 4 unidades + 3 cards canais diretos com ícones
            ├── politica-de-privacidade.html
            ├── aviso-provimento-205.html
            ├── area-direito-penal.html
            ├── area-recursos-tribunais-superiores.html
            ├── area-execucao-penal.html
            ├── area-direito-imobiliario.html
            ├── area-direito-civil.html
            ├── area-familia-sucessoes.html
            ├── area-direito-ambiental.html
            ├── perfil-luiz.html
            ├── perfil-charys.html
            ├── perfil-karla.html
            ├── whatsapp.html                         ← redirect com Analytics tracking
            ├── vercel.json                           ← cleanUrls + redirects + headers
            ├── robots.txt
            ├── sitemap.xml
            ├── favicon.svg
            ├── favicon-32x32.png
            ├── apple-touch-icon.png
            └── assets/
                ├── css/
                │   └── style.css                     ← single CSS, ~507 linhas
                └── images/
                    ├── luiz-henrique-baldissera.jpg
                    ├── charys-baldissera.jpg
                    ├── karla-sampaio.jpg
                    ├── anderson-spanhol.jpg
                    └── og-default.png                ← 1200×630 para Open Graph
```

**Nota crítica:** Vercel está configurada com Root Directory = `site_baldissera_advogados/site_baldissera/public/`. Por isso `vercel.json` precisa estar dentro de `public/`. Referências de assets nos HTMLs são relativas (`assets/css/style.css`, sem `../`).

## 4. Configuração do `public/vercel.json`

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "redirects": [
    { "source": "/atuacao", "destination": "/areas-de-atuacao", "permanent": false },
    { "source": "/privacidade", "destination": "/politica-de-privacidade", "permanent": false },
    { "source": "/provimento-205", "destination": "/aviso-provimento-205", "permanent": false }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains" }
      ]
    }
  ]
}
```

## 5. Arquitetura de páginas

| Slug | Função | Notas |
|---|---|---|
| `/` | Home institucional | hero + grid de áreas, sem `<h1>` por escolha editorial |
| `/sobre` | Página sobre o escritório | órfã do nav principal — pendência |
| `/advogados` | Equipe (4 membros) | Anderson sem perfil dedicado ainda |
| `/areas-de-atuacao` | Listagem das 7 áreas | aponta para `area-*.html` |
| `/publicacoes` | Hub editorial | peer cards (Pub Nº 2 + Pub Nº 1), calendário 2026 |
| `/publicacao-cadeia-de-custodia` | Pub Nº 1 — ensaio dogmático | jan/2026 |
| `/publicacao-prova-digital-sem-hash` | Pub Nº 2 — comentário a julgado | abr/2026, com box "Para quem está chegando" |
| `/contato` | 4 unidades + form + 3 cards canais diretos com ícones | RJ "em implantação" |
| `/politica-de-privacidade` | LGPD | conformidade Lei 13.709/2018 |
| `/aviso-provimento-205` | OAB 205 | declarações de conformidade |
| `/area-*` × 7 | Páginas de cada frente | núcleo I-III, conexas IV-VI, transversal VII |
| `/perfil-luiz`, `/perfil-charys`, `/perfil-karla` | Perfis individuais | currículo do Luiz subdimensionado — pendência |
| `/whatsapp` | Página de redirect | tracking de cliques via Analytics |

## 6. Equipe

| Nome | Cargo | OAB | Lotação | Foto | Perfil |
|---|---|---|---|---|---|
| Luiz Henrique Baldissera | Sócio titular | OAB/PR 55.717 | Cascavel | ✓ | ✓ |
| Charys Gabriella Baldissera | Sócia | OAB/PR 69.897 | Cascavel | ✓ | ✓ |
| Karla da Costa Sampaio | Advogada responsável | OAB/RS 66.523 | Porto Alegre | ✓ | ✓ |
| Anderson Spanhol | Sócio | OAB/PR 96.871 | Porto Belo | ✓ | ✗ (currículo em breve) |

## 7. Captura de leads e analytics

### 7.1 — Top bar de contato (presente em todas as páginas)

Barra fina alinhada à direita do topo de todas as 20 páginas, acima do header principal. Três canais diretos:

- **E-mail** (ícone envelope dourado) → `mailto:contato@baldisseraadvogados.com.br`.
- **Telefone** (ícone aparelho dourado + número visível) → `tel:+5545991029806`. Em mobile (<600px), o texto do número esconde e fica só o ícone.
- **WhatsApp** (ícone WhatsApp em verde `#25D366` discreto) → `/whatsapp.html`.

### 7.2 — Botão flutuante WhatsApp (todas as páginas)

Fixed bottom-right, navy + ícone dourado, 58×58px (54×54 em mobile). Ao clicar, abre `/whatsapp.html`.

### 7.3 — Cards "Canais diretos" no /contato

Três cards grandes na seção "Contato institucional." da página `/contato`, com SVG de envelope, telefone e WhatsApp em tamanho 32px. WhatsApp em verde, os outros em dourado da banca. WhatsApp aponta para `/whatsapp.html` (não direto para `wa.me`) para manter o tracking.

### 7.4 — Vercel Web Analytics

Habilitado em Settings → Analytics. Plano Hobby: 50.000 events/mês, 30 dias de histórico, privacy-first (sem cookies, sem banner LGPD necessário). Script injetado em todas as páginas: `<script defer src="/_vercel/insights/script.js"></script>`.

**Como o Luiz consulta os dados:**

1. https://vercel.com/dashboard → clicar no projeto `baldisseraadvogados`.
2. Coluna esquerda → **Analytics**.
3. Painel mostra: **Visitors** (únicos), **Page Views** (total), **Bounce Rate**, **Top Pages**, **Top Referrers**, **Geografia**, **Devices**, **Browsers**.
4. Filtros de período: 24h, 7d, 30d. Filtros de ambiente: Production / Preview / All.

**Como contar cliques no botão WhatsApp** (substituto dos custom events não disponíveis no Hobby):

- Em **Top Pages**, procurar a URL `/whatsapp` (ou `/whatsapp.html`).
- O número de Page Views dessa página = quantas vezes o botão WhatsApp foi clicado no período (somando top bar, botão flutuante e card de canais diretos — todos passam pela mesma página intermediária).

**Como contar engajamento por publicação:**

- Em **Top Pages**, procurar `/publicacao-cadeia-de-custodia` e `/publicacao-prova-digital-sem-hash`.
- Cada uma terá page views próprios. Comparar entre si para entender quais temas atraem mais.

**Cadência recomendada:** olhar 1x por semana ou após cada nova publicação. Não diariamente. Os números úteis começam a partir da terceira semana de coleta.

## 8. Conformidade — Provimento CFOAB 205/2021

Site em **conformidade substancial**. Auditoria feita: não há promessa de resultado, menção a casos concretos da banca, menção a clientes, superlativos mercadológicos comparativos, depoimentos, descontos ou ofertas mercantilizadas. A página `/aviso-provimento-205` é robusta.

Borderlines mantidos por enquanto:
- Em `/areas-de-atuacao` e `/perfil-luiz`, lista nominal das cinco unidades penitenciárias federais (Catanduvas, Campo Grande, Porto Velho, Mossoró, Brasília). Não é menção a casos — é escopo geográfico de prática. Suavizável para "atuação nos cinco estabelecimentos do sistema penitenciário federal" sem nomear, se quiser maximizar zelo.
- Headline "Banca construída sobre especialização técnica" em `/areas-de-atuacao` (versão neutra de "não generalista" — o original foi reformulado).

## 9. Convenções editoriais

- **Idioma:** português do Brasil em todo o site.
- **Tom:** sóbrio, técnico, sem auto-elogio mercadológico.
- **Tipografia:** Cormorant Garamond para serif (títulos, números, callouts); sans-serif system-stack para corpo.
- **Cores:** navy + gold + ivory. Sem outras cores de marca, exceto verde WhatsApp (`#25D366`) usado pontualmente nos ícones de WhatsApp.
- **Pessoa:** terceira pessoa institucional ("a banca", "o escritório") nos institucionais; primeira pessoa só nos perfis individuais quando apropriado.
- **Provimento 205:** evitar "melhor", "maior", "garantia", "êxito", "especialista em X" comercial, depoimentos, comparações nominais, casos concretos da banca.
- **Citações jurisprudenciais:** identificar tribunal, classe processual, número, relator e data quando possível.
- **Sem emojis** em conteúdo do site.

## 10. Convenções de manutenção

### Workflow de edição

Trabalhar **no clone do sandbox primeiro**, depois sincronizar com a pasta local (Desktop). Editar diretamente arquivos na pasta `OneDrive\Área de Trabalho\site_baldissera_advogados` causou truncagem em commit anterior (race condition do OneDrive sync). Usar Edit tool ou Write tool **apenas no sandbox**, depois `cp` para o local.

### Atalhos para validação rápida

```bash
# verificar referências quebradas a assets
grep -rE '\.\./assets' public/

# verificar HTML válido (tags abertas vs fechadas)
for f in public/*.html; do
  echo "$f: html=$(grep -c '<html' $f) /html=$(grep -c '</html>' $f)"
done

# contagem total de palavras/caracteres por página
wc -w public/*.html | sort -n
```

### Push e validação em produção

1. `cd /caminho/para/baldisseraadvogados`
2. `git add -A && git commit -m "..." && git push origin main`
3. Vercel detecta push em ~5s e inicia build em ~30s.
4. Build completa em ~60-90s.
5. Validar em aba anônima (Ctrl+F5) em `https://www.baldisseraadvogados.com.br/`.
6. Conferir DevTools → Network → status 200 em `style.css` e nas imagens.

### Rollback

```bash
git revert HEAD
git push origin main
```

## 11. Pendências em aberto (que precisam de decisão do Luiz)

| # | Item | Decisão necessária |
|---|---|---|
| 1 | **Status do Rio de Janeiro** | Hoje incoerente em 4 lugares (sobre, contato, footer, perfil-luiz, home). Operacional? Em implantação? Omitir? |
| 2 | **Porto Belo** | Adicionar como 5ª unidade formal ou redefinir lotação do Anderson? |
| 3 | **Currículo do Luiz** | Adicionar dois mestrados (Recursos para Tribunais Superiores; Civil e Processo Civil) com instituições e ano. |
| 4 | **Nav vs `/sobre`** | A página `/sobre` é órfã do nav. Remover, renomear "Escritório" ou adicionar item "Sobre"? |
| 5 | **Narrativa "três vetores" × "sete frentes"** | `/sobre` ainda diz "três vetores"; home diz sete. Padronizar. |
| 6 | **Currículo do Anderson Spanhol** | Quando chegar: card no `/advogados` + criar `perfil-anderson.html`. |

### Opcionais (sem urgência)

- **Submissão do sitemap ao Google Search Console** — adicionar propriedade `baldisseraadvogados.com.br` → submeter `https://www.baldisseraadvogados.com.br/sitemap.xml`.
- **Migração do CNAME do www** para o endpoint novo da Vercel (`bfeb0a03dfb72088.vercel-dns-017.com.`) — não bloqueante.
- **Áudio narrado das publicações** — gerar com ElevenLabs ou similar (TTS BR), embutir como `<audio>`. Decisão: pago (~$5-22/mês) ou gravação pessoal do Luiz.

## 12. Acessos e credenciais

- **GitHub:** conta `baldisseraclaudeia-prog`. Push autenticado por PAT (Personal Access Token) com escopo `repo`.
- **Vercel:** conta de Luiz, plano Hobby. Login via Google.
- **Domínio:** registrado em provedor brasileiro (provavelmente Registro.br).
- **E-mail institucional:** `contato@baldisseraadvogados.com.br` — provedor a definir (Google Workspace foi mencionado como próximo passo no runbook original).
- **formsubmit.co:** sem cadastro. Primeiro envio do form dispara confirmação no e-mail destino, basta clicar uma vez.

## 13. Limites operacionais conhecidos

- **OneDrive na pasta de trabalho local:** edições simultâneas em arquivos na pasta `C:\Users\LuizH\OneDrive\Área de Trabalho\site_baldissera_advogados\` durante sync do OneDrive podem truncar arquivos. Trabalhar sempre no sandbox e sincronizar com `cp` em batch.
- **Sandbox Cowork:** sem egress para `vercel.com` ou `api.github.com` (cowork-egress-blocked). Operações no painel da Vercel feitas via Claude in Chrome com a sessão autenticada. Push para GitHub via `github.com` (sem proxy).
- **Claude in Chrome:** ocasionalmente engasga em screenshots/scrolls de páginas pesadas. Fallback: usar `get_page_text` que é mais leve.
- **Vercel Hobby:** sem custom events em Analytics. Workaround: tracking de cliques via páginas intermediárias (ex.: `/whatsapp.html` para contar cliques no botão).

## 14. Histórico recente de commits (últimos relevantes)

| Hash | Tema |
|---|---|
| `ebd326f` | Ícones nos cards de canais diretos do `/contato` |
| `6f73b87` | Top bar de contato (e-mail · telefone · WhatsApp verde) em todas as páginas |
| `9d340d5` | BRIEFING §17 (analytics) + PADRAO §13.8 (acessibility box) |
| `b109728` | Botão flutuante WhatsApp + Vercel Web Analytics + box "Para quem está chegando" na Pub Nº 2 |
| `44370ff` | Reescrita da Pub Nº 2 como narrativa de caso para público misto |
| `d60052b` | Pub Nº 1 e Pub Nº 2 unificadas como peer cards |
| `8b06a84` | Pub Nº 2 publicada (AgRg no HC 1.014.212/ES) |
| `fcc096c` | Sistema editorial criado (PADRAO + TEMPLATE + INSTRUCOES) |
| `e3a23b2` | BRIEFING.md, PENDENCIAS.md atualizados, CLAUDE.md criado |
| `bc49735` | Site review (metas, OG, forms funcionais, SEO infra, favicons) |

## 15. Módulo editorial — produção de publicações

Sistema dedicado em `docs/editorial/`:

| Arquivo | Função |
|---|---|
| `PADRAO-EDITORIAL.md` | Anatomia visual + tom + Provimento 205 + convenções de citação + aprendizados consolidados (seção 13) |
| `TEMPLATE.html` | Template HTML com marcadores `{{...}}` |
| `INSTRUCOES.md` | Workflow operacional para Claude executar a geração |

**Modalidades:** comentário a julgado · ensaio dogmático · análise de tese recursal · roteiro de defesa.

**Como usar em Claude Project:**
1. Anexar `BRIEFING.md` (este arquivo) + os três do `editorial/` como knowledge files.
2. Colar o julgado ou tema com direcionamento curto.
3. Claude entrega: HTML completo + atualização de `publicacoes.html` + linha nova para `sitemap.xml`.
4. Revisar, comitar, pushar — Vercel publica em ~90 segundos.

**Espelhos de referência:**
- `public/publicacao-cadeia-de-custodia.html` (Pub Nº 1 — ensaio dogmático sobre cadeia de custódia, jan/2026).
- `public/publicacao-prova-digital-sem-hash.html` (Pub Nº 2 — comentário ao AgRg no HC 1.014.212/ES, abr/2026, com box "Para quem está chegando" para público misto).

**Princípios invioláveis:**
- Nunca inventar julgados, normas ou citações.
- Nunca atribuir caso concreto da banca como exemplo.
- Nunca prometer resultado.
- Nunca quebrar o padrão visual sem solicitação explícita.

## 16. Roadmap recomendado

**Curto prazo:**
- Resolver os 6 itens de decisão pendentes.
- Currículo do Anderson → criar `perfil-anderson.html`.
- Próxima publicação: investigação defensiva à luz do Provimento CFOAB 188/2018 (próxima do calendário editorial).

**Médio prazo:**
- Integração de e-mail próprio (Google Workspace ou Zoho Mail) — MX, SPF, DKIM, DMARC no DNS.
- Submeter sitemap ao Google Search Console e Bing Webmaster Tools.
- Atualizar `/publicacoes` à medida que os artigos saem.
- Reorganizar publicações em subpasta `publicacoes/` se ultrapassar 5-6 artigos.
- Considerar áudio TTS narrando as publicações (acessibilidade).

**Longo prazo:**
- Versão em inglês (`/en/`) se houver atuação internacional.
- Speed Insights / Analytics avançado para monitorar performance.
- Integração com CMS leve (Decap CMS sobre o repo) se outras pessoas precisarem editar conteúdo.

---

*Briefing preparado em sessão Cowork. Última atualização: 25/04/2026.*
*Para usar como contexto em Claude Projects: copiar o conteúdo deste arquivo e colar como knowledge file no Project, ou fazer upload do `.md` diretamente.*
