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

**Escreve como advogado, não como máquina.** Antes de fechar a peça ele roda um
passe de redação: corta as muletas ("é importante ressaltar que", "resta
demonstrado", "merece prosperar"), tira intensificador que não tem fato ao lado
("inequívoco", "cristalino") e exige âncora concreta em cada bloco — data,
valor, documento, folha. Texto que serviria para qualquer processo não sustenta
o seu, e é isso que denuncia tanto o texto de máquina quanto a peça mal feita.
Sobre detectores de IA, ele te diz a verdade: erram nos dois sentidos, e a
proteção real é você reescrever na sua voz os trechos centrais — que é, aliás,
o que a faculdade te pede de qualquer jeito.

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

**Antes de tudo:** se alguém te mandou um `.zip` deste agente por WhatsApp ou
e-mail, descarte. Baixe sempre pelo link abaixo — é onde fica a versão atual.

**Link permanente do pacote:**
https://github.com/baldisseraclaudeia-prog/baldisseraadvogados/raw/main/dist/pecas-academicas-civil.zip

Escolha **um** dos três caminhos. O A serve para a maioria.

---

### Caminho A — claude.ai (web ou aplicativo)

1. Baixe o `.zip` pelo link acima.
2. Abra o claude.ai e entre em **Configurações** (ícone da sua conta).
3. Procure a seção **Capacidades** → **Skills**. Se o menu estiver em inglês,
   é *Settings* → *Capabilities* → *Skills*.
4. Clique em enviar/adicionar skill e selecione o `.zip` **sem descompactar**.
5. Confirme que apareceu na lista o nome **pecas-academicas-civil**.
6. Abra uma conversa nova e mande a mensagem de teste do fim deste arquivo.

Não achou a seção Skills nas configurações? O recurso não está liberado nessa
conta. Vá para o Caminho C.

---

### Caminho B — Claude Code (terminal, Mac ou Linux)

Cole o bloco inteiro no terminal e dê Enter. Ele baixa, remove versão antiga se
houver, instala e confere:

```bash
mkdir -p ~/.claude/skills && \
curl -fsSL -o /tmp/pac.zip https://github.com/baldisseraclaudeia-prog/baldisseraadvogados/raw/main/dist/pecas-academicas-civil.zip && \
rm -rf ~/.claude/skills/pecas-academicas-civil && \
unzip -oq /tmp/pac.zip -d ~/.claude/skills && \
rm -f /tmp/pac.zip && \
ls ~/.claude/skills/pecas-academicas-civil
```

**Deu certo se a última linha listar:**

```
LEIA-ME.md   SKILL.md   perfil-do-curso.md   references
```

Depois **feche e abra o Claude Code de novo** — a skill é lida na abertura da
sessão.

Para instalar só em um projeto específico, troque `~/.claude/skills` por
`.claude/skills` dentro da pasta do projeto, nos três lugares em que aparece.

---

### Caminho C — sem instalar nada (funciona em qualquer conta)

1. Baixe o `.zip` e descompacte.
2. No claude.ai, crie um **Projeto** novo.
3. Anexe ao conhecimento do projeto os arquivos `SKILL.md`,
   `perfil-do-curso.md` e a pasta `references/` inteira.
4. Nas instruções do projeto, escreva:
   *"Siga integralmente o SKILL.md anexado. Consulte os arquivos de
   references/ conforme ele indicar."*
5. Converse dentro desse projeto.

Funciona bem. A única diferença é que o agente não é acionado sozinho por
gatilho — ele vale dentro daquele projeto.

---

### Teste depois de instalar

Mande esta mensagem:

> Qual peça cabe: meu cliente foi citado numa ação de cobrança, o prazo de
> resposta está correndo e ele também quer cobrar do autor uma dívida do mesmo
> contrato.

Resposta certa menciona **contestação com reconvenção** e explica por que
descartou a petição inicial autônoma. Se vier isso, está instalado e
funcionando.

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
