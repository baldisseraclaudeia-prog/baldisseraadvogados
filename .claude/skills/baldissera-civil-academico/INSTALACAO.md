# INSTALAÇÃO — onde colocar e como pôr o agente para trabalhar

## O que é

`baldissera-civil-academico` é o agente advogado sênior de direito civil e
processo civil voltado à **produção de peças acadêmicas** — Prática Jurídica,
NPJ, estágio supervisionado, simulados de 2ª fase da OAB e trabalhos de
disciplina. Segue a metodologia das faculdades brasileiras: identificação da
peça, endereçamento e competência, qualificação, fatos sem inovação,
fundamentação com subsunção, pedidos completos, valor da causa, fecho — e
correção pelo espelho.

## Estrutura da pasta

```
baldissera-civil-academico/
├── SKILL.md                                  ← o agente
├── INSTALACAO.md                             ← este arquivo
└── references/
    ├── identificacao-da-peca.md              ← árvore de decisão e pares confusos
    ├── anatomia-das-pecas.md                 ← estrutura bloco a bloco de cada peça
    ├── competencia-e-enderecamento.md        ← escada de competência e linhas de endereçamento
    ├── base-legal.md                         ← âncoras CPC/CC/leis + prazos + protocolo antialucinação
    ├── espelho-de-correcao.md                ← espelhos genéricos, erros que zeram, checklist
    └── formatacao-academica.md               ← formatação, assinatura acadêmica, vedações
```

## Onde colocar

**Opção 1 — pasta de skills do usuário (Mac / Claude Code local).** Copie a
pasta inteira `baldissera-civil-academico/` para o mesmo diretório onde já
vivem `baldissera-acordo-civel/`, `baldissera-homicidio-hc/` e as demais
`baldissera-*`. O reconhecimento é pelo `SKILL.md` na raiz da pasta.

**Opção 2 — conta claude.ai (skills sincronizadas).** Compacte a pasta em
`.zip` e envie em Configurações → Capacidades → Skills. A skill passa a
aparecer em todas as superfícies (Claude Code, Cowork, app), como as demais
`baldissera-*`.

**Opção 3 — pelo repositório.** A pasta já vive em
`.claude/skills/baldissera-civil-academico/` do repositório
`baldisseraadvogados`: quem abrir uma sessão nesse repositório carrega o
agente automaticamente, sem instalar nada.

## Como pôr para trabalhar

Basta um gatilho em linguagem natural. Exemplos:

- "segue o enunciado, faz a peça" (+ o texto do caso) → **Modo 2**, modelo
  comentado
- "me ajuda a montar essa peça, quero escrever eu mesmo" → **Modo 1**,
  orientação
- "corrige minha contestação" (+ o texto do aluno) → **Modo 3**, correção pelo
  espelho
- "qual peça cabe aqui?" / "é agravo ou apelação?" → identificação com descarte

Se o professor tiver fornecido **espelho de correção** ou critérios próprios,
mande junto: eles prevalecem sobre o espelho genérico do agente.

## O que se recebe de volta

Identificação da peça com o **descarte fundamentado** das alternativas, ficha
do caso, a peça redigida (ou o esqueleto, no Modo 1), notas didáticas bloco a
bloco, mapa de força e fragilidade das teses, espelho de autoavaliação, lista
de pendências do enunciado e o **quadro de fontes** com os marcadores
`[ENUNCIADO]` / `[A CONFIRMAR]` / `[NÃO VERIFICADO]` / `[LASTREADO]`.

## O que o agente não faz

- Não inventa fato que não está no enunciado.
- Não fornece número de súmula, tema repetitivo ou acórdão de memória — entrega
  o **roteiro de busca** no portal oficial.
- Não aplica timbre da Baldissera Advogados nem número de OAB real em peça
  acadêmica.
- Não promete nota.
- Não entrega texto pronto sem o raciocínio que o produziu.

## Governança

O `CLAUDE.md` da casa e a trava de citação do escritório prevalecem em caso de
conflito. Toda peça gerada é **minuta para revisão humana**: o aluno relê
integralmente e confere cada fonte no portal antes de entregar.
