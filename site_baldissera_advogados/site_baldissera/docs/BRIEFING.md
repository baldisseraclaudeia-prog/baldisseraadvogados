# Briefing — Site Baldissera Advogados

> **Documento de contexto para Claude Projects.** Cole o conteúdo deste arquivo na knowledge base de um novo Project para que futuras sessões de Claude conheçam o site, o stack técnico, as convenções editoriais, o histórico recente e as pendências em aberto sem precisar reauditar do zero.

---

## 1. Identidade do projeto

- **Cliente / titular:** Luiz Henrique Baldissera — sócio titular da banca **Baldissera Advogados** (OAB/PR 55.717).
- **Domínio em produção:** `https://www.baldisseraadvogados.com.br/`
- **Domínio apex:** `https://baldisseraadvogados.com.br/` → redirect 307 para `www`.
- **Domínio de staging Vercel:** `https://baldisseraadvogados.vercel.app/` (continua funcionando em paralelo).
- **Repositório GitHub:** `github.com/baldisseraclaudeia-prog/baldisseraadvogados` (atenção: nome do repo é com `g`, **não** com `c` como o runbook original sugeria).
- **Branch de produção:** `main` — push direto, sem PR. Vercel auto-deploya.
- **Conta Vercel:** plano Hobby. Scope: `luiz-henrique-baldisseras-projects`. Project: `baldisseraadvogados`.

## 2. Stack técnico

- **Stack:** site estático puro. **HTML + CSS** apenas. Sem framework, sem build step, sem JavaScript de aplicação. Vercel serve o conteúdo de `public/` como arquivos estáticos.
- **Tipografia:** Cormorant Garamond (Google Fonts), carregada via `<link rel="preconnect">` + `<link rel="stylesheet">` no `<head>` de cada HTML.
- **Identidade visual:** paleta navy (`#0F172A`) + dourado (`#9B7B3A`) + ivory (`#F5F1E8`/`#FAFAF7`). Variáveis CSS no `:root` do `style.css`.
- **Formulários:** apontam para `https://formsubmit.co/contato@baldisseraadvogados.com.br` com captcha + honeypot. Não requer cadastro; basta confirmar uma vez o e-mail de ativação enviado pelo formsubmit.
- **Deployment Protection:** **desabilitada** (Vercel Authentication off). Site é público.

## 3. Estrutura do repo

```
baldisseraadvogados/                                  ← repo root no GitHub
└── site_baldissera_advogados/
    └── site_baldissera/                              ← Vercel "Root Directory" aponta para abaixo
        ├── docs/
        ├── public/                                   ← Vercel "Root Directory" REAL
        │   ├── index.html                            ← home
        │   ├── sobre.html
        │   ├── advogados.html
        │   ├── areas-de-atuacao.html
        │   ├── publicacoes.html
        │   ├── publicacao-cadeia-de-custodia.html
        │   ├── contato.html
        │   ├── politica-de-privacidade.html
        │   ├── aviso-provimento-205.html
        │   ├── area-direito-penal.html
        │   ├── area-recursos-tribunais-superiores.html
        │   ├── area-execucao-penal.html
        │   ├── area-direito-imobiliario.html
        │   ├── area-direito-civil.html
        │   ├── area-familia-sucessoes.html
        │   ├── area-direito-ambiental.html
        │   ├── perfil-luiz.html
        │   ├── perfil-charys.html
        │   ├── perfil-karla.html
        │   ├── vercel.json                           ← config: cleanUrls + redirects + headers
        │   ├── robots.txt
        │   ├── sitemap.xml
        │   ├── favicon.svg
        │   ├── favicon-32x32.png
        │   ├── apple-touch-icon.png
        │   └── assets/
        │       ├── css/
        │       │   └── style.css                     ← single CSS file
        │       └── images/
        │           ├── luiz-henrique-baldissera.jpg
        │           ├── charys-baldissera.jpg
        │           ├── karla-sampaio.jpg
        │           ├── anderson-spanhol.jpg
        │           └── og-default.png                ← 1200×630 para Open Graph
        └── (outros)
```

**Importante:** A Vercel está configurada com Root Directory = `site_baldissera_advogados/site_baldissera/public/`. Isso significa que **`vercel.json` precisa estar dentro de `public/`**, não no nível superior. Já está corrigido. As referências de assets nos HTMLs são relativas (`assets/css/style.css`, sem `../`).

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

Notas:
- `cleanUrls: true` faz o Vercel servir `/sobre` → `sobre.html` automaticamente, sem precisar de rewrite explícita.
- `redirects` (não rewrites) são usados para os três aliases curtos (atuacao, privacidade, provimento-205) — rewrites com destino `.html` entravam em loop com `cleanUrls`.
- Headers de segurança (HSTS, frame, referrer policy) aplicados a todas as rotas.

## 5. Arquitetura de páginas

| Slug | Função | Notas |
|---|---|---|
| `/` | Home institucional, hero + grid de áreas | hoje sem `<h1>` por escolha editorial |
| `/sobre` | Página sobre o escritório | **órfã do nav principal** — pendência |
| `/advogados` | Equipe (4 membros) | Anderson sem perfil dedicado ainda |
| `/areas-de-atuacao` | Listagem das 7 áreas | aponta para `area-*.html` |
| `/publicacoes` | Hub editorial | 1 publicação real + 12 pautas previstas |
| `/publicacao-cadeia-de-custodia` | Único artigo publicado | autoria: Luiz |
| `/contato` | 4 unidades + form | RJ marcado "em implantação" |
| `/politica-de-privacidade` | LGPD | conformidade Lei 13.709/2018 |
| `/aviso-provimento-205` | OAB 205 | declarações de conformidade |
| `/area-direito-penal` | Núcleo I | |
| `/area-recursos-tribunais-superiores` | Núcleo II | |
| `/area-execucao-penal` | Núcleo III | menciona Catanduvas, Campo Grande, Porto Velho, Mossoró, Brasília |
| `/area-direito-imobiliario` | Conexa IV | |
| `/area-direito-civil` | Conexa V | |
| `/area-familia-sucessoes` | Conexa VI | |
| `/area-direito-ambiental` | Transversal VII | |
| `/perfil-luiz` | Perfil Sócio Titular | currículo subdimensionado — pendência |
| `/perfil-charys` | Perfil Sócia | inclui artigos no Migalhas |
| `/perfil-karla` | Perfil Advogada Responsável (POA) | |

## 6. Equipe

| Nome | Cargo | OAB | Lotação | Foto | Perfil |
|---|---|---|---|---|---|
| Luiz Henrique Baldissera | Sócio titular | OAB/PR 55.717 | Cascavel | ✓ | ✓ |
| Charys Gabriella Baldissera | Sócia | OAB/PR 69.897 | Cascavel | ✓ | ✓ |
| Karla da Costa Sampaio | Advogada responsável | OAB/RS 66.523 | Porto Alegre | ✓ | ✓ |
| Anderson Spanhol | Sócio | OAB/PR 96.871 | Porto Belo | ✓ | ✗ (currículo em breve) |

## 7. Histórico de commits desta sessão (cronológico)

A sessão de Cowork começou com o site quebrado (CSS não carregava, vercel.json fora do lugar, domínio próprio dando `DEPLOYMENT_NOT_FOUND`, Vercel Authentication ativada bloqueando acesso público). Ao final, o site está em produção, estilizado, indexável e com formulários funcionais.

| Hash | Tema | O que mudou |
|---|---|---|
| `3279e55` | CSS | move `assets/` para dentro de `public/`, corrige 26 referências `../assets/` → `assets/` em 19 HTMLs |
| `f4b6165` | Rewrites | remove prefixo `/public/` das destinations do vercel.json |
| `b50c1fc` | Config | move `vercel.json` para dentro de `public/` (Root Directory da Vercel) |
| `df67e46` | Config | simplifica `vercel.json` (drop `version`/`name` deprecados, remove rewrites redundantes) |
| `942dd93` | Roteamento | converte rewrites de aliases em redirects (`/atuacao`, `/privacidade`, `/provimento-205`) |
| `9a39f26` | Editorial | refaz hero da home — H1 e subtítulo refletem as 7 frentes (não só recursais) |
| `c8a1b94` | Bug | restaura tags de fechamento truncadas no `index.html` (`</span></div></footer></body></html>`) |
| `b2ec442` | Equipe | promove Anderson Spanhol a Sócio em `/advogados`, insere foto, mantém "Currículo em breve" |
| `a78da66` | Editorial | remove o `<h1>` "Advocacia construída para o direito complexo" do hero da home |
| `bc49735` | Site review | metas + Open Graph + Twitter Card em 19 páginas, formsubmit.co em 2 forms, robots.txt + sitemap.xml + JSON-LD LegalService, favicon, og-default.png, ajustes cosméticos (preconnect Google Fonts, reword "não generalista", remove redundância "Bacharelado · Graduação") |

## 8. Operações na Vercel feitas no painel (não em código)

1. **Deployment Protection desabilitada** em Settings → Deployment Protection. Sem isso, visitantes recebiam tela "You are logged in as…" (autenticação Vercel SSO) em vez do site.
2. **Domínio próprio adicionado** em Settings → Domains:
   - `baldisseraadvogados.com.br` (apex) com redirect 307 → `www`.
   - `www.baldisseraadvogados.com.br` como Production.
   - SSL provisionado automaticamente pela Vercel.
   - Aviso "DNS Change Recommended" no www: Vercel sugere migrar do CNAME legado (`cname.vercel-dns.com`) para o novo (`bfeb0a03dfb72088.vercel-dns-017.com.`). O legado continua funcionando — atualização opcional.

## 9. Conformidade — Provimento CFOAB 205/2021

O site está **em conformidade substancial**. Auditoria feita: não há promessa de resultado, menção a casos concretos, menção a clientes, superlativos mercadológicos comparativos, depoimentos, descontos ou ofertas mercantilizadas. A página `/aviso-provimento-205` é robusta.

Borderlines mantidos por enquanto:
- Em `/areas-de-atuacao` e `/perfil-luiz`, lista nominal das cinco unidades penitenciárias federais (Catanduvas, Campo Grande, Porto Velho, Mossoró, Brasília). Não é menção a casos — é escopo geográfico de prática. Se quiser maximizar zelo, suavizar para "atuação nos cinco estabelecimentos do sistema penitenciário federal" sem nomear.
- Headline "Banca construída sobre especialização técnica" em `/areas-de-atuacao` (versão neutra de "não generalista" — o original foi reformulado).

## 10. Convenções editoriais

- **Idioma:** português do Brasil em todo o site.
- **Tom:** sóbrio, técnico, sem auto-elogio mercadológico.
- **Tipografia:** Cormorant Garamond para serif (titulos, números, callouts); sans-serif system-stack para corpo.
- **Cores:** navy + gold + ivory. Sem outras cores de marca.
- **Pessoa:** terceira pessoa institucional ("a banca", "o escritório") nos institucionais; primeira pessoa só nos perfis individuais quando apropriado (atualmente nenhum usa).
- **Provimento 205:** evitar "melhor", "maior", "garantia", "êxito", "especialista em X" em sentido comercial, depoimentos, comparações nominais, casos concretos.
- **Citações jurisprudenciais:** identificar tribunal, classe processual, número, relator e data quando possível.
- **Sem emojis** em conteúdo do site.

## 11. Convenções de manutenção

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

# contagem total de palavras/caracteres por página (proxy de densidade editorial)
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

Se algo quebrar:
```bash
git revert HEAD
git push origin main
```

## 12. Pendências em aberto (que precisam de decisão do Luiz)

| # | Item | Decisão necessária |
|---|---|---|
| 1 | **Status do Rio de Janeiro** | Hoje incoerente em 4 lugares. Operacional? Em implantação? Omitir? Aplicar uma única linha em `/sobre`, `/contato`, footer (todas pgs), subtítulo home, perfil-luiz. |
| 2 | **Porto Belo** | Adicionar como 5ª unidade formal (criar card em `/contato` + linha no footer + menção em `/sobre`)? Ou reatribuir lotação do Anderson? |
| 3 | **Currículo do Luiz no `/perfil-luiz`** | Adicionar os dois mestrados (Recursos para Tribunais Superiores; Civil e Processo Civil) com instituição e ano. Nome da instituição do bacharelado e da pós em Ciências Criminais, se quiser listar. |
| 4 | **Nav vs `/sobre`** | A página `/sobre` é órfã do nav. Três opções: (a) remover `/sobre` e mesclar conteúdo na home; (b) renomear "Escritório" no nav para apontar a `/sobre` e criar item "Início" para `/index`; (c) adicionar item "Sobre" ao nav. |
| 5 | **Narrativa "três vetores" × "sete frentes"** | `/sobre` ainda diz "três vetores"; home diz sete. Definir e padronizar. |
| 6 | **Currículo do Anderson Spanhol** | Quando chegar: (a) substituir "Currículo em breve" pela descrição curta no card de `/advogados`; (b) criar `perfil-anderson.html` no padrão dos outros três; (c) converter `<div>` do card em `<a href="perfil-anderson.html">`. |

### Opcionais (sem urgência)

- **Submissão do sitemap ao Google Search Console** — autenticar conta Google → adicionar propriedade `baldisseraadvogados.com.br` → submeter `https://www.baldisseraadvogados.com.br/sitemap.xml`.
- **Migração do CNAME do www** para o endpoint novo da Vercel — `bfeb0a03dfb72088.vercel-dns-017.com.` (no painel do provedor de DNS, provavelmente Registro.br).
- **Atualizar e-mail de envio dos formulários** se quiser que cheguem em endereço diferente de `contato@baldisseraadvogados.com.br` — basta trocar o destino na URL `https://formsubmit.co/<email>` em `/contato.html` e `/publicacoes.html`.

## 13. Acessos e credenciais

- **GitHub:** conta `baldisseraclaudeia-prog`. Push autenticado por PAT (Personal Access Token) com escopo `repo`. PATs usados nesta sessão foram revogados após o uso.
- **Vercel:** conta de Luiz, plano Hobby. Login via Google.
- **Domínio:** registrado em provedor brasileiro (provavelmente Registro.br, considerando `.com.br`).
- **E-mail institucional:** `contato@baldisseraadvogados.com.br` — provedor a definir (Google Workspace foi mencionado como próximo passo no runbook original).
- **formsubmit.co:** sem cadastro. Primeiro envio do form dispara confirmação no e-mail destino, basta clicar uma vez.

## 14. Limites operacionais conhecidos

- **OneDrive na pasta de trabalho local:** edições simultâneas em arquivos na pasta `C:\Users\LuizH\OneDrive\Área de Trabalho\site_baldissera_advogados\` durante sync do OneDrive podem truncar arquivos. Trabalhar sempre no sandbox e sincronizar com `cp` em batch.
- **Sandbox Cowork:** sem egress para `vercel.com` ou `api.github.com` (cowork-egress-blocked). Operações no painel da Vercel feitas via Claude in Chrome com a sessão autenticada do usuário. Push para GitHub via `github.com` (sem proxy).
- **Claude in Chrome:** ocasionalmente engasga em screenshots/scrolls de páginas pesadas. Fallback: usar `get_page_text` que é mais leve.

## 15. Roadmap recomendado

**Curto prazo** (próxima sessão de trabalho):
- Resolver os 6 itens de decisão acima.
- Quando o currículo do Anderson chegar, criar `perfil-anderson.html` e atualizar card.

**Médio prazo:**
- Integração de e-mail próprio (Google Workspace ou Zoho Mail) com `@baldisseraadvogados.com.br` — MX, SPF, DKIM, DMARC no DNS.
- Submeter sitemap ao Google Search Console e Bing Webmaster Tools.
- Adicionar mais publicações reais (atualizar `/publicacoes` à medida que os artigos saem).
- Reorganizar publicações em subpasta `publicacoes/` se ultrapassar 5-6 artigos.

**Longo prazo:**
- Considerar versão em inglês (`/en/`) se houver atuação internacional.
- Speed Insights / Analytics da Vercel para monitorar performance.
- Integração com CMS leve (ex.: Decap CMS sobre o repo) se outras pessoas precisarem editar conteúdo sem tocar em código.

---

## 16. Módulo editorial — produção de publicações

Sistema dedicado para a produção contínua de conteúdo da aba `/publicacoes`. Documentação em `docs/editorial/`:

| Arquivo | Função |
|---|---|
| `PADRAO-EDITORIAL.md` | Anatomia visual + tom + vedações Provimento 205 + convenções de citação |
| `TEMPLATE.html` | Template HTML com marcadores `{{...}}` para preenchimento |
| `INSTRUCOES.md` | Workflow operacional passo a passo para Claude executar a geração |

**Modalidades cobertas:** comentário a julgado · ensaio dogmático · análise de tese recursal · roteiro de defesa.

**Como usar em Claude Project:**
1. Anexar os três arquivos do `docs/editorial/` como knowledge files do Project (junto com o `BRIEFING.md`).
2. Colar o julgado (ementa, voto ou URL) com direcionamento curto sobre o ângulo desejado.
3. Claude entrega: HTML completo + atualização de `publicacoes.html` + linha nova para `sitemap.xml`.
4. Revisar, comitar, pushar — Vercel publica em ~60-90s.

**Espelho de referência:** `public/publicacao-cadeia-de-custodia.html` (publicação inaugural, jan/2026).

**Princípios invioláveis** (estão detalhados em `INSTRUCOES.md`):
- Nunca inventar julgados, normas ou citações.
- Nunca atribuir caso concreto da banca como exemplo.
- Nunca prometer resultado.
- Nunca quebrar o padrão visual sem solicitação explícita.

---

*Briefing preparado em sessão Cowork. Última atualização: 2026-04-25. Para usar como contexto em Claude Projects: copiar o conteúdo deste arquivo e colar como knowledge file no Project.*
