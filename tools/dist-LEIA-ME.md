# Peças acadêmicas — Direito Civil e Processo Civil

Agente para acadêmico de direito montar as peças da faculdade — Prática
Jurídica, NPJ, estágio supervisionado, simulados de 2ª fase da OAB e trabalhos
de disciplina — pela metodologia usada pelas faculdades brasileiras.

Ele não é um gerador de petição. É um **orientador**: entrega a peça junto com
o raciocínio que a produziu, para você saber defender cada linha se o professor
perguntar.

---

## O que ele faz

**Identifica a peça pelo método certo.** Pela posição do cliente, pelo momento
processual e pela pretensão — nunca pelo tema de direito material. É o erro que
mais zera peça na faculdade: ler "dano moral" e sair fazendo inicial quando o
cliente é réu e o que corre é prazo de contestação. E entrega o **descarte
fundamentado**: por que esta peça e por que não as outras duas ou três que
pareciam caber.

**Trabalha em três modos**, escolhidos pelo que você mandar:

| Modo | Quando | O que você recebe |
|---|---|---|
| **Orientação** | "me ajuda a montar, quero escrever eu mesmo" | Roteiro e esqueleto em blocos, com o que vai em cada um |
| **Modelo comentado** (padrão) | Você manda o enunciado e pede a peça | Peça redigida + notas didáticas bloco a bloco + espelho de autoavaliação |
| **Correção** | Você manda a peça que escreveu | Correção item a item pelo espelho, com reescrita dos trechos fracos |

**Pesquisa jurisprudência de verdade.** Quando há ferramenta de busca na
sessão, ele procura nos portais oficiais (tribunal do caso → STJ → STF), abre o
**inteiro teor**, monta a ficha do julgado e testa se a ratio serve ao seu caso.
Quando não há busca disponível, ele diz isso e entrega o roteiro com as queries
prontas para você colar no portal — **sem inventar nenhum número**.

**Adapta-se ao seu curso.** Manda o espelho do professor, o manual da
instituição ou só uma frase ("meu professor numera os tópicos em romanos",
"limite de 2 laudas", "é PJe", "sou do 4º período") e ele se molda. A exigência
do professor sempre vence o padrão do agente.

---

## O que ele NÃO faz — e por quê

Estas travas não se desligam, nem a pedido:

- **Não inventa jurisprudência.** Nenhum número de súmula, tema repetitivo ou
  acórdão sai da memória. Ou veio de busca real com inteiro teor aberto, ou não
  entra. Jurisprudência inventada em peça não é só nota baixa — é o vício que
  destrói advogado depois.
- **Não inventa fatos.** O universo fático é o enunciado. Fato que não está lá
  vira lacuna declarada, não preenchimento.
- **Não usa timbre de escritório real nem número de OAB de advogado
  existente.** Assinatura acadêmica fictícia, sempre.
- **Não promete nota.** Aponta o que o espelho cobra e onde a peça está frágil.
  Quem corrige é o professor.
- **Não improvisa fora do escopo.** Núcleo: civil e processo civil, mais as
  adjacências civis (consumidor, família e sucessões, imobiliário, locação,
  responsabilidade civil, contratos). Penal, trabalhista e tributário ele
  declara como fora do alcance em vez de arriscar.

---

## Como instalar

**No claude.ai (mais simples).** Abra as configurações da conta, vá à seção de
capacidades/skills e envie o arquivo `.zip` que você recebeu. Depois disso o
agente fica disponível nas conversas.

**No Claude Code.** Descompacte a pasta `pecas-academicas-civil/` dentro de
`~/.claude/skills/` (vale para qualquer projeto) ou dentro de
`.claude/skills/` de um projeto específico. O reconhecimento é pelo arquivo
`SKILL.md` na raiz da pasta.

---

## Como usar

Basta escrever em português normal. Primeira mensagem, por exemplo:

> Segue o enunciado da peça de Prática Jurídica. Sou do 6º período, a
> disciplina é processo civil, o professor pede no máximo 3 laudas. Faz a peça
> comentada.
>
> [colar o enunciado inteiro, com os anexos]

Outros exemplos que funcionam:

- "qual peça cabe aqui?" — identificação com descarte, sem escrever a peça
- "é agravo ou apelação nesse caso?"
- "corrige minha contestação" + o texto que você escreveu
- "acha jurisprudência do TJ sobre essa tese"
- "segue o espelho do professor" + o arquivo

**Dica que economiza tempo:** preencha `perfil-do-curso.md` uma vez
(instituição, professor, espelho, formatação, limite de páginas, jurisdição,
seu período) e mande junto na primeira conversa. Depois não precisa repetir
nada disso a cada peça.

---

## Antes de entregar ao professor

1. **Releia a peça inteira.** Ela é minuta, não produto final.
2. **Confira cada fonte no portal oficial.** Todo dispositivo legal no site do
   Planalto; todo julgado no portal do tribunal, com o inteiro teor aberto.
   Nada com marcação `[NÃO VERIFICADO]` ou `[A CONFIRMAR]` deve sobreviver na
   versão entregue.
3. **Cheque se você sabe defender cada linha.** Se houver um argumento que você
   não conseguiria sustentar numa arguição oral, peça ao agente para explicar
   até você dominar — ou troque por outro que você domine.

A peça tem que ser sua. O agente serve para você aprender a fazer, mais rápido
e com menos erro — não para entregar o que você não entende.
