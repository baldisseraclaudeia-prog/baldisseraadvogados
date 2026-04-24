# PENDÊNCIAS — Para fechar antes do go-live

Este documento lista todas as pendências identificadas até o momento da compilação deste pacote (21/04/2026). Algumas são bloqueantes para a publicação; outras podem ser resolvidas após o site já estar no ar.

---

## PENDÊNCIAS BLOQUEANTES (resolver antes do go-live)

### 1. Configuração DNS no Registro.br

Apontar o domínio `baldisseraadvogados.com.br` para a Vercel (ou outra hospedagem escolhida). Sem isso, o site fica acessível apenas pelo link temporário da Vercel (`baldissera-advogados-xyz.vercel.app`).

**Passo a passo em `DEPLOY.md`.**

### 2. Configuração DNS do Google Workspace

Para que os e-mails (`luiz@`, `charys@`, `karla@`, `contato@`, `dpo@`) funcionem:

- TXT de verificação: `google-site-verification=oPKaR1Knb9jMkCshs4ulmcroCN-evUXZtrAB19lEmFo`
- MX records do Google Workspace
- SPF: `v=spf1 include:_spf.google.com ~all`
- DKIM: gerar no painel do Workspace e copiar para o Registro.br
- DMARC: `v=DMARC1; p=quarantine; rua=mailto:dpo@baldisseraadvogados.com.br`

### 3. Criação dos aliases de e-mail no Workspace

No painel admin do Workspace (`admin.google.com`), criar:

- `contato@baldisseraadvogados.com.br` (alias → `luiz@`)
- `dpo@baldisseraadvogados.com.br` (alias → `luiz@`)
- `charys@baldisseraadvogados.com.br` (conta paga ou alias)
- `karla@baldisseraadvogados.com.br` (conta paga ou alias)

Cada conta paga adicional custa R$ 49/mês após os primeiros 3 meses promocionais. Alias é gratuito.

### 4. ~~Foto institucional definitiva da Charys~~ ✓ CONCLUÍDO

Foto recebida em 21/04/2026, tratada em PB editorial com crop 4:5 (600×750px) e integrada ao site. Arquivo final em `assets/images/charys-baldissera.jpg`. Páginas atualizadas: `perfil-charys.html` e `advogados.html`.

---

## PENDÊNCIAS NÃO BLOQUEANTES (podem ser resolvidas após o go-live)

### 5. Perfil completo do Anderson Spanhol

O índice de advogados (`advogados.html`) hoje mostra um card placeholder com "perfil em preparação". Quando os dados dele estiverem disponíveis, basta criar `perfil-anderson.html` (replicar a estrutura do `perfil-luiz.html`) e atualizar o card no índice.

### 6. Endereço definitivo da unidade Rio de Janeiro

Hoje a unidade aparece como "em implantação" na página Contato e no rodapé. Quando o endereço estiver definido, atualizar:

- `contato.html` — substituir o card "em implantação" por endereço real
- Footer de todas as páginas — opcional adicionar telefone específico se for o caso

### 7. Forma jurídica da banca na OAB

Confirmar se a banca opera como **sociedade de advogados** (com contrato social registrado na OAB e CNPJ próprio, com nomenclatura tipo "Baldissera Advogados Associados") ou se opera como **inscrição individual de Luiz Henrique Baldissera + advogados associados/colaboradores**.

Esta definição afeta:

- Como Charys aparece (sócia formal ou advogada com vínculo associativo)
- Como Karla aparece (advogada associada ou apenas responsável pela unidade)
- O fluxo tributário e contábil interno
- A nomenclatura nas páginas de perfil

Quando definida, atualizar os subtítulos institucionais ("SÓCIA", "ADVOGADA RESPONSÁVEL") nos perfis se necessário.

### 8. Domínios defensivos

Recomendado registrar variantes para proteção de marca:

- `baldisseraadvogados.adv.br` (~R$ 60/ano)
- `baldissera.adv.br` (~R$ 60/ano, se disponível)
- `baldisseraadvocacia.com.br` (já é domínio anterior — manter ativo, redirecionando para o novo)

Configurar redirecionamento 301 de todos esses domínios para `baldisseraadvogados.com.br`.

### 9. Estender registro do domínio principal para 10 anos

Hoje o domínio expira em 20/04/2028 (registro de 2 anos). Recomenda-se estender para 10 anos quando houver disponibilidade de fluxo de caixa, por dois motivos:

- Custo proporcional menor (cerca de R$ 38/ano contra R$ 38/ano agora, mas com proteção até 2036)
- Sinal positivo para algoritmos de busca (Google considera domínios com longo prazo como mais legítimos)

### 10. Lançamento do hub editorial

A página `publicacoes.html` está pronta com calendário editorial, formulário de newsletter e cards estruturais — mas o conteúdo do primeiro artigo ainda não está produzido. Recomenda-se:

- Lançar o site mesmo sem o primeiro artigo (a página tem placeholder elegante "§ O hub editorial entra no ar em breve")
- Em até 30 dias após o go-live, publicar o primeiro artigo do calendário (jan: cadeia de custódia digital)
- Manter cadência mensal a partir daí

Para criar uma publicação:

1. Criar arquivo HTML em `public/publicacao-NOME.html` (replicar estrutura de uma página de área)
2. Adicionar card linkando para ela na lista de publicações
3. Atualizar página `publicacoes.html`

### 11. Configuração da newsletter (Substack ou Mailchimp)

O formulário de newsletter na página `publicacoes.html` hoje aponta para `mailto:` por padrão. Para coletar e-mails com conformidade LGPD e enviar newsletters reais:

**Opção A — Substack (recomendado, gratuito):**
- Criar conta em `substack.com`
- Configurar newsletter "Baldissera Advogados"
- Substituir o `<form>` da página por código de embed do Substack

**Opção B — Mailchimp (gratuito até 500 contatos):**
- Criar conta em `mailchimp.com`
- Criar audiência
- Substituir formulário por código de embed do Mailchimp

### 12. Reserva do Instagram institucional

Reservar `@baldisseraadvogados` no Instagram para uso institucional, mesmo que não vá ser muito ativo. Estratégia:

- Criar conta com foto institucional simples (monograma BA)
- Postar 1 conteúdo institucional por mês (anúncio de novo artigo do hub editorial, por exemplo)
- Não fazer impulsionamento pago (vedação do Provimento 205)
- Manter compatibilidade com o Instagram pessoal da Charys (`@charysbaldissera`)

### 13. WhatsApp Business

Hoje o link do WhatsApp aponta para `wa.me/5545991029806`. Quando houver tempo, configurar o WhatsApp Business no mesmo número, com:

- Mensagem de boas-vindas automatizada
- Catálogo das áreas de atuação
- Etiquetas de atendimento
- Horário de funcionamento

### 14. Google Search Console + Google Analytics

Após o site estar no ar com domínio próprio, registrar em:

- `search.google.com/search-console` — para monitoramento SEO e indexação
- `analytics.google.com` — para mensurar tráfego e comportamento

Adicionar o ID de tracking ao final de cada página HTML (no head antes de `</head>`).

### 15. Auditoria de acessibilidade WCAG 2.1

Antes de divulgar amplamente, executar auditoria com ferramentas como WAVE (`wave.webaim.org`) ou Lighthouse (built-in no Chrome) para verificar:

- Contraste de cores adequado
- Alt text em todas as imagens
- Hierarquia semântica de headings
- Navegação por teclado funcional

A maioria dos itens já está coberta na construção, mas auditoria formal é boa prática institucional.

---

## RESUMO DAS DECISÕES PENDENTES

Decisões que dependem do escritório:

1. **Forma jurídica** da banca (sociedade ou inscrição individual)
2. **Endereço** da unidade RJ
3. **Foto** definitiva da Charys
4. **Dados** completos do Anderson para perfil
5. **Posicionamento societário** de Charys (sócia, sócia associada, associada) e Karla (responsável, associada, sócia)
6. **Cronograma editorial** — quando lançar o primeiro artigo

Decisões técnicas que dependem da publicação:

1. Contratação de plataforma de e-mail marketing
2. Configuração de Analytics
3. Reserva do Instagram institucional
4. Decisão sobre domínios defensivos

---

**Documento preparado em:** 21/04/2026
**Para acompanhamento das pendências:** Recomenda-se revisar este documento mensalmente.
