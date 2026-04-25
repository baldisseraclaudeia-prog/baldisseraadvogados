# Padrão editorial — publicações Baldissera Advogados

> **Para quem:** assistentes de IA (Claude, etc.) e pessoas que vão produzir publicações para a aba `/publicacoes` do site. **Para quê:** garantir que toda nova publicação preserve o tom, a estrutura visual e o rigor jurídico-editorial estabelecidos na publicação inaugural (cadeia de custódia, janeiro/2026), em conformidade com o Provimento CFOAB 205/2021.

---

## 1. Identidade editorial em uma frase

Banca técnica, voz autoral elegante, prosa limpa e cadenciada, didática para colega advogado, **nunca promocional**, nunca casuística sobre processos próprios, sempre ancorada em normas e julgados públicos com identificação completa.

## 2. Tipos de publicação cabíveis

A linha editorial admite quatro modalidades, todas com a mesma estrutura visual:

| Modalidade | Exemplo | Frequência sugerida |
|---|---|---|
| **Ensaio dogmático** | "Quando a cadeia de custódia se rompe" | mensal |
| **Comentário a julgado** | "O que a Sexta Turma decidiu no HC X — e por que muda a defesa em casos de Y" | quinzenal/mensal |
| **Análise de tese recursal** | "Prequestionamento ficto e o overruling implícito do Tema Z" | mensal |
| **Roteiro de defesa** | "Cinco teses para o defensor em audiência preliminar de organização criminosa" | conforme oportunidade |

Esta pasta foi criada especialmente para a modalidade **Comentário a julgado** — que é o caso de uso recorrente: o usuário apresenta um julgado favorável à defesa e a publicação é gerada a partir dele.

## 3. Anatomia visual de uma publicação

Toda publicação segue **a mesma estrutura HTML** (ver `TEMPLATE.html`). Não inventar componentes novos. Os blocos são:

1. **`<head>`** padrão da banca (meta + OG + favicon + fonts).
2. **`<header>`** institucional — sempre o mesmo.
3. **Breadcrumb**: `Publicações / [título da publicação]`.
4. **Hero da publicação**:
   - **Eyebrow**: `PUBLICAÇÃO Nº X · ÁREA · MÊS DE ANO`
   - **H1**: título descritivo, normalmente com dois pontos separando título e subtítulo (ex.: "Quando a cadeia de custódia se rompe: cinco hipóteses em que a falha do Estado pode anular a condenação.").
   - **Lead em itálico** (deck): aforismo ou síntese provocativa do tema, em Cormorant Garamond italic, gold-soft, 21px.
   - **Linha de autoria**: `por · [Nome] · OAB · leitura: X min`.
5. **Corpo do artigo** (section dedicada):
   - **Pull quote inicial** (font 24px, italic, navy, border-left gold) — frase curta de impacto que abre o texto. *Opcional, mas presente na publicação inaugural.*
   - Parágrafos de prosa fluida, font-size 16px, line-height 1.85, cor `var(--text-soft)`.
   - **Intertítulos `<h2>`**: Cormorant 30px navy, margin-top 50px. Devem dividir o argumento em 4-6 movimentos lógicos.
   - **Boxes destacados** (opcional, padrão "hipóteses"): background ivory, border-left gold 3px, padding 30px/32px. Cada box tem rótulo italic gold ("Hipótese I"), título serif 24px navy, descrição rápida em texto-muted 14px.
   - **Citações de jurisprudência**: sempre em `<strong>` (ex.: `<strong>HC 653.515/RJ</strong>`). Nome do tribunal, número, relator e data devem aparecer ao menos uma vez por julgado citado.
   - **Ênfases pontuais**: `<em>` italic.
   - **Referências a artigos**: por extenso ("art. 158-A do CPP", "art. 5º, LV, da CF").
   - **Assinatura final**: `— L.H.B.` (ou iniciais do autor) em gold italic alinhado à direita, margin-top 50px.
6. **Bloco de Referências**:
   - Cabeçalho "REFERÊNCIAS" + "Normas e julgados citados."
   - Cards individuais (background ivory-bg, border 0.5px gold-light): cada card lista o item (ex.: "STJ · HC 653.515/RJ") + descrição curta (1-2 linhas: turma, relator, data, motivo de relevância).
   - Listar **todos** os julgados, normas e doutrinas citados no corpo. Não deixar referência fora do bloco.
7. **Bloco do autor**: foto + nome + título + bio curta + link "Ver perfil →". Padrão pronto no template.
8. **Próximas publicações**: card-placeholder dummy com a próxima do calendário editorial + link genérico para `publicacoes.html`.
9. **`<footer>`** institucional — sempre o mesmo.

## 4. Tom e voz

- **Pessoa narrativa**: terceira pessoa institucional ("o defensor", "a defesa", "o Estado") **com** uso pontual de primeira pessoa autoral ("vinte e poucos anos de prática criminal me ensinaram que…"). A primeira pessoa é admitida quando o autor reflete ou compartilha experiência prática genérica — **nunca** para narrar caso concreto que conduziu.
- **Cadência**: alternar frases longas e curtas. Frases curtas para pontuar (ex.: "A pergunta que importa é simples."). Frases longas para análise dogmática.
- **Vocabulário técnico**: preciso, sem pedantismo. Latim e termos estrangeiros em itálico (`<em>habeas corpus</em>`, `<em>distinguishing</em>`, `<em>UFDR</em>`, `<em>mesmidade</em>`).
- **Recursos retóricos admitidos**: aforismo de abertura e fechamento (mesma frase reaparece com variação no final), pull quote inicial, perguntas retóricas curtas, paralelismos, anáforas pontuais.
- **Recursos vedados**: emoji, ponto de exclamação enfático, gírias, anglicismos desnecessários, jargão de "growth hacking", linguagem motivacional.

## 5. Conformidade com o Provimento CFOAB 205/2021 — checklist obrigatório

Antes de publicar **qualquer** texto, conferir mentalmente:

- [ ] **Não menciona caso concreto conduzido pela banca** (cliente, processo, valor, decisão envolvendo o escritório).
- [ ] **Não promete resultado** ("garantia de…", "certeza de…", "vencerá", "obterá êxito"). Falar em "pode levar à", "tende a", "dificilmente sobrevive a", "é frequentemente acolhido".
- [ ] **Não compara** com outros advogados ou bancas.
- [ ] **Não usa superlativos auto-elogiosos** ("o melhor", "o maior", "líder em").
- [ ] **Não contém depoimentos** de clientes.
- [ ] **Não oferece serviços, descontos, gratuidades, pacotes**.
- [ ] **Não usa "especialista em X"** em sentido comercial. Pode usar "Especialista pela [Instituição]" se houver título acadêmico de especialização.
- [ ] **Identifica todos os julgados citados** com tribunal, número, relator e data.
- [ ] **Identifica todas as normas citadas** com número e ano.
- [ ] **Tom sóbrio**, compatível com a dignidade da advocacia (art. 3º do Provimento 205).

Se um item passa no risco mas é defensável, manter; se é evitável sem perda de força argumentativa, evitar.

## 6. Convenções de citação

### Julgados
Formato canônico no corpo:
> A Sexta Turma do STJ, no **HC 653.515/RJ** (Rel. Min. Laurita Vaz, Rel. p/ acórdão Min. Rogerio Schietti Cruz, julgado em 23/11/2021), absolveu réu acusado de tráfico…

Formato canônico no bloco de referências:
> **STJ · HC 653.515/RJ** — Sexta Turma, Rel. Min. Laurita Vaz, Rel. para acórdão Min. Rogerio Schietti Cruz, julgado em 23/11/2021. Leading case sobre [síntese].

### Normas
> art. 158-A do Código de Processo Penal
> art. 5º, LV, da Constituição Federal
> Lei 13.964/2019 (Pacote Anticrime)

### Doutrina
> AURY LOPES JR., *Direito Processual Penal*, 18ª ed., 2021, p. 543.
(Usar `<em>` para títulos de obras.)

### Súmulas
> Súmula 568 do STJ
> Enunciado 32 do FONACRIM

## 7. Comprimento e densidade

- **Mínimo aceitável**: 800 palavras de corpo (excluindo blocos auxiliares).
- **Faixa ideal**: 1.500 a 2.500 palavras (8 a 14 minutos de leitura).
- **Máximo razoável**: 3.500 palavras. Acima disso, considerar dividir em duas publicações.
- Tempo de leitura no eyebrow: **calcular como `palavras_corpo / 250`**, arredondado para inteiro.

## 8. Numeração e nomeação dos arquivos

- **Próximo número de publicação**: ver `publicacoes.html` para o último `Nº X` usado e incrementar.
- **Nome do arquivo HTML**: `publicacao-[slug-curto].html` no diretório `public/`.
  - Exemplo: `publicacao-cadeia-de-custodia.html`.
  - Slug em minúsculas, sem acentos, sem caracteres especiais, hífens entre palavras.
- **Atualizações obrigatórias depois de criar**:
  1. Atualizar `publicacoes.html`: adicionar card no bloco "publicação em destaque" (substituindo o anterior) e mover o anterior para um bloco novo "edições anteriores" (criar se não existir).
  2. Atualizar `sitemap.xml`: adicionar a nova URL com `priority=0.7`, `changefreq=yearly`.
  3. Atualizar `BRIEFING.md` (seção 5 "Arquitetura de páginas") se for adição estruturalmente nova.

## 9. Imagem do autor no bloco final

- Sempre usar o JPG já presente em `assets/images/`:
  - `luiz-henrique-baldissera.jpg` (Luiz)
  - `charys-baldissera.jpg` (Charys)
  - `karla-sampaio.jpg` (Karla)
  - `anderson-spanhol.jpg` (Anderson)
- O `alt` deve ser o nome completo.
- Se houver mais de um coautor, usar layout em duas colunas (replicar pattern adaptado).

## 10. Open Graph e SEO da publicação

No `<head>` da publicação:
- `<title>`: `[Título curto] · Baldissera Advogados`
- `<meta name="description">`: 1 frase, ≤160 caracteres, com palavras-chave técnicas.
- `og:title`, `twitter:title`: igual ao `<title>`.
- `og:description`, `twitter:description`: igual à meta description.
- `og:url`: `https://www.baldisseraadvogados.com.br/publicacao-[slug]` (sem `.html` — `cleanUrls` está ativo).
- `og:image`: `https://www.baldisseraadvogados.com.br/assets/images/og-default.png` (padrão da banca).
- `og:type`: `article` (não `website`) para publicações.
- Adicionar também: `<meta property="article:author" content="Nome do Autor">` e `<meta property="article:published_time" content="2026-MM-DD">`.

## 11. Compliance jurídico-formal final

- Sempre incluir, mesmo que de forma sutil, **observação de que o conteúdo não constitui aconselhamento jurídico individualizado**. O bloco de Referências cumpre essa função quando bem-feito (artigo é claramente ensaio doutrinário, não consulta processual).
- Verificar que a publicação **não** se refere a clientes do escritório — nem por inicial, nem por descrição de fatos que poderiam identificá-los, nem por números de processo conduzidos pela banca.
- Verificar que a publicação **não** contém promessa explícita ou implícita de êxito processual.
- Manter **distância editorial**: a tese descrita é uma **possibilidade dogmática**, não uma estratégia individual.

## 12. Quando o usuário pede "gere uma publicação a partir deste julgado"

Workflow recomendado em quatro passos (ver `INSTRUCOES.md` para detalhes):

1. **Ler** o julgado integralmente (ementa, voto do relator, votos divergentes se houver).
2. **Identificar** o ponto técnico que torna o julgado relevante para a defesa.
3. **Estruturar** o argumento em 4-6 movimentos.
4. **Redigir** seguindo este padrão e gerar o HTML completo, pronto para colar em `public/`.

---

*Padrão editorial preparado em 25/04/2026. Atualizar este documento sempre que houver mudança estrutural no template visual ou em convenções editoriais.*
