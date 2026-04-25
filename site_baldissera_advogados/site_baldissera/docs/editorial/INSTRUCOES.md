# Instruções operacionais — geração de publicações

> **Para Claude (e outros assistentes):** este é o manual de instrução para gerar uma publicação para o site Baldissera Advogados a partir de um julgado, um tema doutrinário, ou um texto bruto fornecido pelo usuário. Sempre leia primeiro `PADRAO-EDITORIAL.md` (ao lado deste arquivo).

> **Para o Luiz:** este documento explica o fluxo de trabalho. A ideia é que você simplesmente cole o julgado em qualquer Project Claude que tenha esses arquivos como knowledge base, e ele entrega a publicação pronta.

---

## Fluxo geral (visão do usuário)

```
[Você cola um julgado (ementa + voto, ou só URL)]
            ↓
[Claude analisa, identifica a tese favorável à defesa,
 estrutura o argumento, redige no padrão da banca]
            ↓
[Claude entrega: HTML completo + atualização de publicacoes.html
 + entrada para sitemap.xml, prontos para commit]
            ↓
[Você revisa, aprova, comita & pusha]
            ↓
[Vercel redeploya em ~60-90s, publicação está no ar]
```

## Como acionar (templates de prompt)

### Caso 1 — Comentário a julgado favorável à defesa
```
Gere uma publicação a partir deste julgado:

[colar ementa completa, ou colar voto inteiro, ou colar URL do inteiro teor]

Direcionamento: foque [no aspecto que você quer destacar — ex.: "no
voto vencido do Min. X que reconheceu a quebra da cadeia de custódia",
ou "no fundamento de que a busca pessoal sem indício mínimo é nula"].

Tom: [se quiser inflexão específica, dizer; senão, padrão da banca].
```

### Caso 2 — Ensaio dogmático sobre tema
```
Gere uma publicação ensaística sobre [tema], cobrindo [pontos a tratar],
ancorada em [normas e julgados que você quer usar como espinha].
```

### Caso 3 — Análise de tese recursal
```
Quero uma publicação analisando a tese de [tese], aplicada a [matéria].
Citar [julgados/precedentes específicos]. Destacar a técnica de
[prequestionamento/distinguishing/overruling/etc.].
```

### Caso 4 — Roteiro de defesa
```
Gere um roteiro técnico para defensores em [situação processual].
Estruturar em N teses sucessivas, com fundamento normativo de cada uma.
```

---

## Workflow detalhado para Claude

### Passo 1 — Validação de insumo
Antes de redigir, verificar:

- [ ] O julgado/material é público? (Não pode ser caso da banca, nem caso identificável de cliente.)
- [ ] Há identificação completa do julgado? (Tribunal, número, relator, data — se faltar algum, **avisar** o usuário em vez de inventar.)
- [ ] O direcionamento do usuário foi claro? (Se ambíguo, perguntar **uma única vez** antes de gerar.)

### Passo 2 — Análise técnica
Antes de escrever, montar mentalmente:

1. **Qual é a tese central** que torna o julgado relevante para a defesa.
2. **Qual norma** (artigo de lei, dispositivo constitucional, súmula, tema) sustenta a tese.
3. **Quais leading cases anteriores** convergem ou divergem do julgado em análise.
4. **Quais movimentos argumentativos** o texto vai cobrir (4-6 intertítulos `<h2>`).
5. **Qual é o aforismo de abertura** — frase curta de impacto que sintetize a posição.
6. **Qual a moral prática** para o defensor (a "lição transferível" do julgado).

### Passo 3 — Redação no padrão

**Estrutura sugerida para Comentário a Julgado:**

| Movimento | Conteúdo | Tamanho aproximado |
|---|---|---|
| Pull quote inicial | Frase curta provocativa | 1 linha |
| Cenário | Apresentação genérica do problema processual de fundo | 2-3 §§ |
| H2: O que o tribunal decidiu | Síntese técnica do julgado, citando o acórdão `<strong>` | 3-4 §§ |
| H2: A ratio decidendi | Análise do fundamento adotado, com normas e doutrina | 3-4 §§ |
| H2: Convergência/divergência com a jurisprudência anterior | Comparar com leading cases | 2-3 §§ |
| H2: Aplicação prática para a defesa | Como usar a tese; em que tipos de caso; com que cuidados | 3-4 §§ |
| H2: Limites e riscos | Distinguishing possível; situações em que a tese não funciona | 1-2 §§ |
| Fechamento | Retomar aforismo de abertura em variação; assinatura | 1-2 §§ |

**Estrutura sugerida para Ensaio Dogmático:**

| Movimento | Conteúdo |
|---|---|
| Pull quote inicial | Aforismo |
| Cenário concreto | Caso narrado em terceira pessoa, sem identificar partes |
| H2: Definição normativa do instituto | |
| H2: Hipóteses (boxes destacados, opcional) | |
| H2: Posição da jurisprudência | |
| H2: Consequências processuais | |
| H2: Janela temporal/preclusão (se aplicável) | |
| Fechamento | Síntese + retomada |

### Passo 4 — Geração do HTML

1. Copiar `TEMPLATE.html`.
2. Substituir todos os `{{MARCADORES}}` (ver lista no comentário do topo do template).
3. **Não modificar a estrutura visual** (CSS inline, espaçamentos, cores). Apenas o conteúdo.
4. **Calcular o tempo de leitura**: contar palavras do corpo do artigo, dividir por 250, arredondar.
5. **Calcular o número da publicação**: ler `publicacoes.html` (bloco "publicação em destaque" ou "edições anteriores") e incrementar.
6. **Gerar o slug do arquivo**: minúsculas, sem acentos, hífens entre palavras, prefixo `publicacao-`.

### Passo 5 — Atualizações colaterais

Junto com o HTML da publicação, também gerar:

**5.1 — Atualização de `publicacoes.html`:**
- Mover o card atual de "publicação em destaque" para uma seção "edições anteriores" (criar a seção se não existir, com layout de cards menores).
- Substituir o card de destaque pela nova publicação.
- Atualizar o calendário editorial (mover do "previsto" para "publicado", ou ajustar).

**5.2 — Atualização de `sitemap.xml`:**
Adicionar:
```xml
<url>
  <loc>https://www.baldisseraadvogados.com.br/{{SLUG}}</loc>
  <lastmod>{{ANO_MES_DIA}}</lastmod>
  <changefreq>yearly</changefreq>
  <priority>0.7</priority>
</url>
```

**5.3 — Bloco de "próximas publicações"** dentro do HTML da nova publicação:
Apontar para a próxima do calendário editorial (ler `publicacoes.html`).

### Passo 6 — Checklist final antes de entregar

- [ ] Todos os `{{MARCADORES}}` substituídos? (`grep -c '{{' arquivo.html` deve retornar 0)
- [ ] Todos os julgados citados no corpo aparecem no bloco de Referências?
- [ ] Tempo de leitura calculado e plausível?
- [ ] Compliance Provimento 205 verificada (ver checklist em `PADRAO-EDITORIAL.md` § 5)?
- [ ] HTML válido (`<html>` aberto, `</html>` fechado, sem tags pendentes)?
- [ ] Próxima publicação prevista atualizada no bloco "próximas publicações"?
- [ ] `publicacoes.html` atualizada com a nova edição em destaque?
- [ ] Entrada nova adicionada ao `sitemap.xml`?

### Passo 7 — Entrega ao usuário

Apresentar:

1. **Link clicável** para o arquivo HTML criado (`computer://...`).
2. **Resumo curto**: título, slug, número, área, comprimento, tempo de leitura.
3. **Lista das atualizações colaterais feitas** (publicacoes.html, sitemap.xml).
4. **Avisos pertinentes**: se algum dado precisa de revisão humana, se alguma referência ficou borderline para Provimento 205, se houve pressuposto interpretativo digno de nota.

---

## Princípios invioláveis

1. **Nunca inventar julgados, normas, súmulas, autores ou citações.** Se não houver certeza absoluta de que existe, declarar ao usuário e pedir confirmação ou suprimir a referência.
2. **Nunca atribuir a autoria a quem não escreveu.** Se o usuário não disse quem é o autor, perguntar (ou usar o autor padrão Luiz Henrique Baldissera, OAB/PR 55.717).
3. **Nunca incluir caso concreto da banca.** Mesmo que o usuário envie um julgado em que o escritório atuou, o texto deve ser escrito como análise pública doutrinária, sem identificar que houve atuação da banca naquele processo.
4. **Nunca prometer resultado.** Linguagem técnica e probabilística, nunca garantista.
5. **Nunca quebrar o padrão visual** descrito no template. Adicionar variantes só se o usuário pedir explicitamente.

---

## Exemplo concreto

Para ver como isso se materializa na prática, abrir `public/publicacao-cadeia-de-custodia.html`. É a publicação inaugural e funciona como "espelho" do padrão.

---

*Instruções preparadas em 25/04/2026. Atualizar este documento conforme o workflow evoluir.*
