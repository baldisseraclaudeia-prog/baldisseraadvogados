# DEPLOY — Como publicar o site

Guia passo a passo para colocar o site no ar no domínio `baldisseraadvogados.com.br`.

## OPÇÃO RECOMENDADA: VERCEL (gratuito, 5 minutos)

A Vercel é a melhor plataforma de hospedagem para sites estáticos como este. Gratuita para projetos pessoais, performática (servidores em todo o mundo), HTTPS automático, integração simples com domínio próprio.

### Passo 1 — Criar conta na Vercel

1. Acesse `vercel.com`
2. Clique em "Sign Up"
3. Use sua conta Google (a mesma do Workspace `luiz@baldisseraadvogados.com.br`) ou GitHub
4. Confirme o cadastro

### Passo 2 — Fazer upload do site

**Caminho A — Drag & Drop (mais simples):**
1. Na dashboard da Vercel, clique em "Add New..." → "Project"
2. Procure a opção "Deploy without Git" (ou clique em "Browse Templates" e role para baixo)
3. Arraste a pasta `public/` para a área de upload
4. **Importante:** edite o arquivo `vercel.json` (se solicitar configuração) ou apenas confirme o deploy
5. Aguarde 30 segundos
6. A Vercel gerará um link tipo `baldissera-advogados-xyz.vercel.app` — o site já está no ar!

**Caminho B — Via GitHub (recomendado para atualizações futuras):**
1. Crie uma conta no GitHub (gratuito) em `github.com`
2. Crie um repositório novo chamado `baldissera-site`
3. Faça upload de todos os arquivos do pacote (incluindo a pasta `assets/`)
4. Na Vercel, clique "Add New..." → "Project" → "Import Git Repository"
5. Selecione `baldissera-site`
6. Confirme — deploy automático

### Passo 3 — Conectar domínio próprio

1. Na dashboard da Vercel, abra o projeto
2. Clique em "Settings" → "Domains"
3. Digite `baldisseraadvogados.com.br` e clique "Add"
4. A Vercel mostrará registros DNS que você precisa adicionar no Registro.br
5. Adicione também `www.baldisseraadvogados.com.br` (subdomínio)
6. Aguarde 10 minutos para propagação DNS

### Passo 4 — Configurar DNS no Registro.br

1. Acesse `registro.br` e faça login
2. Vá em "Painel" → escolha o domínio `baldisseraadvogados.com.br`
3. Clique em "Configurar zona DNS" → "Modo avançado"
4. Adicione os registros que a Vercel forneceu (geralmente CNAME ou A):
   - **Tipo A** para `@`: `76.76.21.21` (IP da Vercel)
   - **Tipo CNAME** para `www`: `cname.vercel-dns.com`
5. Salve

A propagação DNS leva entre 10 minutos e 24 horas. Em geral, em 1 hora o site está acessível em `https://baldisseraadvogados.com.br` com HTTPS automático configurado pela Vercel.

---

## OPÇÕES ALTERNATIVAS

### Netlify (similar à Vercel)
- Mesma simplicidade, gratuito, performance similar
- `netlify.com`

### GitHub Pages (gratuito, mais técnico)
- Requer conta GitHub
- Domínio: `usuario.github.io/repositorio`
- Pode apontar domínio próprio também

### Hospedagem tradicional (HostGator, Hostinger, KingHost)
- Custo mensal R$ 15-40
- Faça upload via FTP do conteúdo da pasta `public/` para o diretório raiz
- Indicada apenas se você já tem essa hospedagem por outros motivos

---

## CHECKLIST PÓS-DEPLOY

Antes de divulgar o site publicamente, verifique:

- [ ] Todas as páginas carregam (testar cada link do menu superior)
- [ ] As imagens dos perfis (Luiz e Karla) aparecem corretamente
- [ ] O formulário de contato envia mensagens (testar com seu próprio e-mail)
- [ ] Os e-mails listados (`contato@`, `luiz@`, `charys@`, `karla@`, `dpo@`) estão criados no Workspace
- [ ] HTTPS está ativo (cadeado verde no navegador)
- [ ] O site abre tanto em `baldisseraadvogados.com.br` quanto em `www.baldisseraadvogados.com.br`
- [ ] As páginas legais (Privacidade e Provimento 205) estão linkadas no rodapé
- [ ] O telefone clicável funciona em mobile
- [ ] O botão WhatsApp abre o aplicativo corretamente

---

## ATUALIZAÇÕES FUTURAS

Para editar conteúdo:

1. Abra o arquivo HTML correspondente em qualquer editor de texto (VS Code, Notepad++, Sublime)
2. Edite o conteúdo entre as tags HTML
3. Salve
4. Faça upload da nova versão na Vercel (drag & drop) — substitui automaticamente

Para adicionar uma nova publicação ao hub editorial:

1. Crie um novo arquivo HTML em `public/`, copiando a estrutura de `perfil-charys.html` como base (ela tem layout para card de publicação)
2. Adicione um link na lista da página `publicacoes.html`
3. Faça upload

---

**Suporte técnico:** A Vercel tem documentação extensa em `vercel.com/docs`. Para questões específicas do site, consulte os arquivos comentados no código.
