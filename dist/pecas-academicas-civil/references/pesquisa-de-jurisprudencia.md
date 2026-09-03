# Pesquisa de jurisprudência e doutrina

## 0. O princípio que governa este módulo

**O agente não sabe jurisprudência. O agente busca jurisprudência.**

Número de súmula, de tema repetitivo e de acórdão é exatamente o tipo de dado
que uma IA reproduz errado com aparência de certeza. Por isso: nenhum número
sai da memória, em hipótese alguma. Ou veio de busca real, com o inteiro teor
aberto, ou não existe para efeito de peça.

### Os dois estados de operação — declare qual está em uso

**Estado A — com ferramenta de busca disponível na sessão.** O agente pesquisa
de verdade nos portais oficiais, abre o inteiro teor, extrai o trecho verbatim
e monta a ficha do precedente. Resultado sai marcado `[LASTREADO]` apenas
quando o inteiro teor foi efetivamente aberto.

**Estado B — sem ferramenta de busca.** O agente **não fornece nenhum número**.
Entrega o **roteiro de busca**: as queries prontas para colar, o portal, os
filtros e a ficha em branco para o aluno preencher. Isso não é uma entrega
pobre — é a única entrega honesta possível nesse estado.

Abrir o módulo dizendo em qual estado se está é obrigatório. Silenciar sobre
isso e produzir texto que pareça pesquisa é o pior resultado possível.

---

## 1. Quando buscar

**Depois de fixada a tese, nunca antes.** Jurisprudência confirma tese; não a
inventa. Quem pesquisa antes de ter tese acaba montando a peça em torno do
julgado que achou — e o julgado quase nunca é do caso.

Ordem correta: fatos → tese → dispositivo → **busca** → ajuste da tese, se a
busca revelar algo que a enfraquece.

---

## 2. O que procurar, em ordem de força

| Ordem | O que | Por que primeiro |
|---|---|---|
| 1 | **Precedente vinculante ou qualificado** — súmula vinculante, controle concentrado, repetitivos, IRDR, IAC, súmulas dos tribunais superiores `[A CONFIRMAR]` CPC art. 927 | Obriga o juiz do caso. É o de maior força |
| 2 | **Súmula do tribunal do caso** | Orienta a própria câmara que vai julgar |
| 3 | **Jurisprudência dominante do tribunal do caso** | É quem decide de fato — e é o que o professor cobra numa peça endereçada àquele tribunal |
| 4 | **STJ e STF** sobre a tese | Autoridade persuasiva e horizonte recursal |
| 5 | **Doutrina** | Reforço conceitual, nunca substituto de norma ou precedente |

**Busque também o contrário.** Procure a tese adversa: é assim que se descobre
se a jurisprudência do tribunal está contra o cliente, e é isso que permite
antecipar a objeção na própria peça. Peça que só procura o que confirma é peça
cega.

---

## 3. Ordem de busca (protocolo da casa)

**Tribunal do caso → STJ → STF → demais tribunais.**

A razão é prática, não hierárquica: quem vai julgar é o tribunal do caso.
Precedente do TJ de outro estado, por mais bonito que seja, não move o juiz da
comarca — e o professor sabe disso.

---

## 4. Como montar a query

- **Não pesquise em linguagem natural.** Portal de tribunal não é buscador
  web. Use o vocabulário do julgado: nome do instituto, do vício, da
  consequência jurídica.
- **Combine três elementos:** instituto + consequência pretendida + dispositivo.
  Ex.: `"cláusula penal" "redução" "artigo 413"`.
- **Aspas para expressão exata.** Sem aspas, o portal quebra a expressão e
  devolve ruído.
- **Use os operadores do portal** (E, OU, NÃO, ADJ, PROX, conforme o sistema) —
  cada portal tem os seus, verifique na página de ajuda da própria pesquisa.
- **Filtre por órgão julgador e por data.** Julgado recente do órgão competente
  vale mais que julgado antigo de outro órgão.
- **Varie o vocabulário forense.** O mesmo fenômeno aparece com nomes
  diferentes: "esbulho" / "turbação"; "revisão contratual" / "onerosidade
  excessiva"; "dano moral" / "abalo anímico" / "lesão a direito da
  personalidade". Rode a busca com dois ou três sinônimos antes de concluir
  que não há nada.
- **Se a busca voltar vazia, o problema costuma ser a query, não a
  jurisprudência.** Amplie: tire um termo, troque a expressão, busque só o
  instituto.

---

## 5. Portais — onde se busca

| Fonte | O que tem | Ponto de entrada usual |
|---|---|---|
| **Tribunal do caso** (TJ do estado) | Acórdãos e súmulas do tribunal que vai julgar | Portal oficial do tribunal → seção Jurisprudência |
| **STJ** | Acórdãos, súmulas, informativos de jurisprudência | Portal do STJ → Pesquisa de Jurisprudência |
| **STJ — precedentes qualificados** | Repetitivos, IAC, temas afetados e suspensos | Portal do STJ → seção de precedentes qualificados |
| **STF** | Acórdãos, súmulas, súmulas vinculantes | Portal do STF → Pesquisa de Jurisprudência |
| **STF — repercussão geral** | Temas de repercussão geral e seu andamento | Portal do STF → Repercussão Geral |
| **TRF da região** | Matéria de competência federal | Portal do respectivo TRF |
| **Turmas Recursais** | Juizados Especiais | Portal do TJ do estado |
| **Planalto** | Legislação, redação vigente | Portal da Presidência → Legislação |

> Endereços de portal mudam. Se um link falhar, chegue pelo nome oficial do
> tribunal, nunca por link de terceiro.

### Proibido como fonte

Agregadores comerciais de jurisprudência, portais de notícia jurídica, blogs,
resumos, mapas mentais e material de cursinho **não são fonte**. Podem servir
de **pista** para descobrir que existe um julgado sobre o tema — e só. Achou a
pista, reabra no portal oficial e confira. Citar a partir do agregador é
citação de segunda mão, que é vedada.

---

## 6. Ficha do precedente — obrigatória por resultado

Nenhum julgado entra na peça sem esta ficha preenchida:

```
Tribunal:
Órgão julgador (câmara / turma / seção):
Relator:
Processo (numeração ÚNICA COMPLETA, sem truncar):
Data do julgamento:
Data da publicação:
Tese / ratio, em uma frase:
Trecho verbatim que sustenta o uso:
Link do inteiro teor:
Data da consulta:
Status: [LASTREADO] / [CANDIDATO] / [NÃO LOCALIZADO] / [SUPERADO OU AFETADO]
Serve para: (qual tópico da peça)
```

A numeração completa é regra fixa: o final do número é o que permite reencontrar
o julgado depois.

---

## 7. Os cinco testes antes de usar

Falhou **um**, o julgado não entra.

1. **Existe?** Localizado no portal oficial, com link que abre.
2. **Inteiro teor aberto?** Ementa não é o precedente — é resumo feito por
   terceiro, e frequentemente diz mais do que o acórdão decidiu.
3. **A ratio corresponde ao uso?** A frase existir não basta. O que o tribunal
   *decidiu* tem de ser o que você está afirmando.
4. **Há similitude fática?** Precedente sem semelhança de fatos é distinguível
   — e o adversário vai distinguir.
5. **Continua vigente?** Não foi superado, revisto, distinguido nem afetado com
   suspensão. Verifique antes de apostar a tese nele.

---

## 8. Estados do resultado

| Marcador | Significado |
|---|---|
| `[LASTREADO]` | Inteiro teor aberto no portal oficial, trecho copiado verbatim, data de consulta anotada. **Único estado que autoriza citação na peça** |
| `[CANDIDATO]` | Localizado, mas inteiro teor não aberto ou ratio não conferida. Vai para o aluno conferir — não entra na peça |
| `[NÃO LOCALIZADO]` | A busca não achou. Diga isso. Não preencha |
| `[SUPERADO OU AFETADO]` | Existe, mas foi superado, revisto ou está suspenso. Serve de alerta, não de fundamento |
| `[CONTRÁRIO]` | Achado que **milita contra** o cliente. Vai na análise interna, para antecipar a objeção — não na peça |

---

## 9. Vedações do módulo

- Fornecer número de súmula, tema ou acórdão **de memória**.
- Citar de **segunda mão** — a partir de outro acórdão, de artigo, de resumo ou
  de agregador.
- Usar **ementa** como se fosse o precedente.
- **Colar ratio**: completar o sentido de um julgado com frase de outro.
- Montar **parede de ementas** — dez julgados empilhados sem uso argumentativo.
  Um precedente bem trabalhado vale mais que dez colados, e o espelho pontua o
  uso, não a quantidade.
- Apresentar como pesquisa o que foi geração de texto.

---

## 10. Como citar na peça

**Formato forense, no corpo do texto** — o suficiente para o julgador
reencontrar: tribunal, órgão julgador, número completo do processo, relator,
data do julgamento. Em seguida, o trecho que interessa, entre aspas, e **o uso**
— o que aquele trecho prova no seu caso. Julgado citado sem uso explicado é
enfeite.

**Formato ABNT, quando o trabalho exigir referências** — conforme o manual da
instituição, que costuma ter regra própria. Elementos mínimos: jurisdição,
tribunal, tipo e número da decisão, partes ou processo, relator, data do
julgamento, veículo e data de publicação, link e data de acesso.

**Quantidade:** um a três por tese. Mais que isso é peso morto.

---

## 11. Adaptação (a exigência do professor manda)

- **Professor veda jurisprudência na peça:** não cite. Mas pesquise mesmo
  assim, para uso interno — serve para saber se a tese se sustenta e o que
  esperar do outro lado.
- **Professor exige N julgados:** entregue N **candidatos com roteiro de
  busca** para o aluno confirmar. Se a busca real achou menos que N, diga o
  número achado — nunca complete a cota com invenção.
- **Professor exige ABNT:** formato de referência conforme o manual da
  instituição.
- **Professor pede julgado do tribunal local:** a ordem de busca já começa por
  ele.

---

## 12. Doutrina — mesma trava

Doutrina inventada é tão grave quanto jurisprudência inventada, e mais difícil
de detectar. Regras:

- **Não atribua tese a autor** sem ter a obra à vista. Nome, título, edição,
  página e ano só entram se o aluno tiver o livro aberto.
- Sem a obra: entregue **o conceito** sem atribuição, e indique onde procurar
  (manual da disciplina, comentários ao código, a bibliografia do plano de
  ensino).
- Enunciado de jornada, súmula de conselho e orientação de órgão de classe
  seguem a mesma regra dos julgados: só com o texto conferido na fonte oficial.

---

## 13. Entregável do módulo

```
## Jurisprudência pesquisada
[Estado de operação: A (busca real) ou B (sem ferramenta — roteiro).]

[Estado A — tabela de fichas, uma por julgado, com status.]

[Estado B — queries prontas para colar, por tese, com portal e filtros,
mais a ficha em branco a preencher.]

## Achados contrários
[O que milita contra o cliente e como a peça o neutraliza — ou por que não
neutraliza.]

## O que não foi localizado
[Teses para as quais a busca não achou apoio. Dizer é obrigatório.]
```
