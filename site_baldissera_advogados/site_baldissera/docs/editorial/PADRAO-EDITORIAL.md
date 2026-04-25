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
   - Citações de jurisprudência **em bold** ("HC 653.515/RJ"), com tribunal, número, relator e data ao menos uma vez por julgado citado.
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
- Ver também a **recalibração da seção 13.7** abaixo, para Comentários a Julgado densos com articulação jurisprudencial.

## 8. Numeração e nomeação dos arquivos

- **Próximo número de publicação**: ver `publicacoes.html` para o último `Nº X` usado e incrementar.
- **Nome do arquivo HTML**: `publicacao-[slug-curto].html` no diretório `public/`.
  - Exemplo: `publicacao-cadeia-de-custodia.html`.
  - Slug em minúsculas, sem acentos, sem caracteres especiais, hífens entre palavras.
- **Atualizações obrigatórias depois de criar**:
  1. Atualizar `publicacoes.html`: substituir o card de "publicação em destaque" pela nova edição e mover o anterior para a seção "edições anteriores" (criar se não existir).
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

## 13. Aprendizados consolidados na prática

> Esta seção reúne padrões refinados a partir de execuções reais do pipeline. Sempre que uma nova publicação revelar uma técnica ou cuidado relevante, registrar aqui.

### 13.1 — Citação direta do voto em box destacado

Quando o voto do relator contiver formulação inovadora ou doutrinariamente densa de um conceito-chave, **citar diretamente** dentro do box destacado padrão (border-left gold, background ivory), em vez de parafrasear no corpo. Preserva a autoridade da fonte e dá ao leitor jurista contato com o vocabulário exato da Corte.

Exemplo aplicado na Pub Nº 2: o trecho do Min. Carlos Pires Brandão sobre o `hash` como "marcador técnico de integridade" foi reproduzido em box, em itálico, com rótulo "Do voto" e atribuição implícita ao acórdão já identificado em parágrafo anterior. Padrão de markup:

```html
<div style="background:var(--ivory);border-left:3px solid var(--gold);padding:30px 32px;margin:30px 0 22px;">
<p style="font-family:var(--serif);font-style:italic;font-weight:500;color:var(--gold);font-size:18px;margin:0 0 6px;letter-spacing:.04em;">Do voto</p>
<p style="font-size:14px;line-height:1.7;color:var(--text-muted);margin:0;font-style:italic;">"[citação direta entre aspas]"</p>
</div>
```

### 13.2 — Conteúdo operacional em box (quesitos, requisitos, passos numerados)

Quando o julgado contiver conteúdo operacionalmente útil — quesitos sugeridos para perícia, requisitos formais, passos numerados, checklists — destacar em box dedicado com rótulo descritivo do conteúdo (não "Hipótese X" como na publicação inaugural, mas algo como "Quesitos da perícia complementar", "Requisitos formais", "Roteiro processual").

A entrega visual do conteúdo em box facilita a apropriação prática pelo defensor que vai usar o material na peça que está redigindo. Padrão de markup:

```html
<div style="background:var(--ivory);border-left:3px solid var(--gold);padding:30px 32px;margin:30px 0 22px;">
<p style="font-family:var(--serif);font-style:italic;font-weight:500;color:var(--gold);font-size:18px;margin:0 0 6px;letter-spacing:.04em;">[Rótulo descritivo]</p>
<p style="font-size:14px;line-height:1.75;color:var(--text-muted);margin:0;"><strong style="color:var(--navy);font-weight:500;">(i)</strong> primeiro item;<br><strong style="color:var(--navy);font-weight:500;">(ii)</strong> segundo item;<br>...</p>
</div>
```

### 13.3 — Não nominar paciente, réu ou partes do julgado, mesmo sendo informação pública

Embora os nomes apareçam na ementa pública, o tratamento editorial da banca é abstrato. Substituir por descrições funcionais: "o paciente preso desde novembro de 2022", "o agravante", "o acusado", "o réu condenado em primeira instância". A regra vale para nomes de pessoas físicas; nomes de tribunais, julgadores e advogados das partes (na ementa) seguem regras próprias.

**Exceções admitidas para nominar:**

- **Tribunais e turmas**: sempre nominar (STJ, STF, TJ-MG, Sexta Turma, etc.).
- **Ministros relatores e julgadores**: sempre nominar como referência da autoria do voto (ex.: "Rel. Min. Carlos Pires Brandão", "Min. Schietti", "Min. Sebastião Reis Júnior").
- **Doutrinadores e autores citados**: nominar com obra (ex.: "Aury Lopes Jr.").
- **Advogados das partes do julgado comentado**: **não citar** — não é pertinente nem editorialmente apropriado a banca chancelar ou identificar a atuação de colegas em casos alheios.
- **Paciente, réu, agravante, vítima, terceiros do caso**: não nominar.

### 13.4 — Articulação entre turmas/colegiados merece intertítulo dedicado

Quando o julgado comentado opera explicitamente sobre tensão jurisprudencial entre Quinta e Sexta Turmas, ou entre Plenário e turmas, ou entre seções, vale dedicar um intertítulo `<h2>` próprio à articulação. A clareza didática é maior, e o defensor que estuda a matéria entende rapidamente o estado da jurisprudência.

Padrão de título: nominar a tensão e a chave de superação, se houver. Exemplos:

- "A chave de proporcionalidade metodológica" (Pub Nº 2 — articulou Quinta e Sexta Turma).
- "A divergência entre Plenário e Primeira Turma — e o critério da Corte Especial".
- "Como a Sexta Turma reposicionou o entendimento da Quinta".

### 13.5 — Estrutura tripla de aplicação prática (impugnação · pleito pericial · pleito cautelar)

Para Comentários a Julgado em matéria de prova/cadeia de custódia, a seção "Como usar a tese na prática" beneficia-se de uma estrutura tripla, em três parágrafos sequenciais:

1. **Impugnação concreta** (não genérica) — descrever o que o defensor precisa documentar para que o pleito não seja rejeitado como hipótese abstrata.
2. **Pleito pericial nos termos exatos do julgado** — instruir a defesa a copiar os quesitos do voto, citando o precedente como fonte do modelo.
3. **Pleito de consequência prática** (substituição de cautelar, exclusão da prova, recálculo de pena, etc.) — articular o efeito processual que se pretende.

Esse trio funciona como "kit defensivo prático", e é o que diferencia uma análise puramente doutrinária de um texto que serve ao colega advogado.

### 13.6 — Limites e cuidados — sempre presentes

Toda publicação deve ter uma seção "Limites e cuidados" (ou equivalente) **antes** do fechamento. A defesa preparada conhece os limites da tese; a publicação que oculta limites perde credibilidade técnica. Listar 2-4 ressalvas concretas ao alcance da tese, com base no próprio julgado ou na jurisprudência conexa.

### 13.7 — Comprimento real ficou acima do estimado na Pub Nº 2

Pub Nº 2 ficou com ~3.500 palavras de corpo (acima da faixa "ideal" de 1.500-2.500 sugerida na seção 7). Isso decorreu da densidade técnica da matéria e da importância de articular Quinta e Sexta Turmas. A faixa ideal continua válida como referência, mas **publicações que envolvam tensão jurisprudencial relevante naturalmente migram para o limite superior** — e isso é aceitável, desde que a leitura permaneça fluida (sem repetições, sem digressões, com cada parágrafo avançando o argumento).

Recalibração informal:

- Faixa ideal **1.500 a 3.500 palavras** para Comentário a Julgado denso com articulação jurisprudencial.
- Faixa ideal **800 a 2.000 palavras** para Comentário a Julgado pontual (um único acórdão, sem articulação com outros precedentes).

---

### 13.8 — Box "Para quem está chegando" no início de Comentários a Julgado

Quando a publicação é um Comentário a Julgado destinado a público misto (cliente eventual + colega advogado), inserir, logo após o pull quote inicial e antes do primeiro intertítulo H2, um box destacado intitulado **"Para quem está chegando"** com 3-4 parágrafos em linguagem acessível (≈250-350 palavras totais) que:

1. Abre com uma **parábola/analogia** que traduza o problema técnico em situação cotidiana ("Imagine que…").
2. Conecta a parábola com **o caso real** sem usar jargão jurídico ("Foi mais ou menos isso que aconteceu nesse caso, mas em vez de…").
3. Resume **o que o tribunal decidiu** em uma frase clara, sem prometer resultado.
4. Faz a **ponte para a leitura técnica** que vem a seguir ("A história abaixo conta o caso em detalhe…").

Esse bloco serve simultaneamente:
- Ao **leitor leigo** (cliente potencial), que entende o caso em 90 segundos e percebe a sofisticação da defesa criminal sem precisar decifrar jargão.
- Ao **leitor jurista**, que pula o box e vai direto à análise — mas vê que a publicação é cuidadosa o suficiente para acolher quem chega de fora.
- À **conformidade Provimento 205**: a parábola é descritiva (não promete resultado), e a ponte explicita que o que vem abaixo é análise doutrinária, não consulta processual.

Padrão de markup (idêntico ao box de "Quesitos da perícia complementar", apenas com rótulo distinto):

```html
<div style="background:var(--ivory);border-left:3px solid var(--gold);padding:30px 36px;margin:32px 0 40px;">
<p style="font-family:var(--serif);font-style:italic;font-weight:500;color:var(--gold);font-size:18px;margin:0 0 14px;letter-spacing:.04em;">Para quem está chegando</p>
<p style="font-size:15px;line-height:1.8;color:var(--text-soft);margin:0 0 14px;">Imagine que…</p>
<p style="font-size:15px;line-height:1.8;color:var(--text-soft);margin:0 0 14px;">Foi mais ou menos isso que aconteceu…</p>
<p style="font-size:15px;line-height:1.8;color:var(--text-soft);margin:0 0 14px;">[O que o tribunal decidiu, em uma frase].</p>
<p style="font-size:15px;line-height:1.8;color:var(--text-soft);margin:0;">A história abaixo conta o caso em detalhe…</p>
</div>
```

Posicionamento: **logo após o pull quote inicial, antes do primeiro `<h2>`**. Aplicado pela primeira vez na Pub Nº 2 (`publicacao-prova-digital-sem-hash.html`).


---

*Padrão editorial preparado em 25/04/2026. Atualizado em 25/04/2026 com a seção 13 (Aprendizados consolidados), a partir da Pub Nº 2 (AgRg no HC 1.014.212/ES). Atualizar este documento sempre que uma execução real revelar técnica ou cuidado replicável.*
