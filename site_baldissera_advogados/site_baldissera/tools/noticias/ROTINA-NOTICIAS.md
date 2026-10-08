# Rotina diária de notícias dos tribunais — regras do Dr. Luiz (07/10/2026)

Fonte única das instruções da rotina `noticias-stj-site` (Windows, 7h), da rotina `noticias-tribunais-mac`
(Mac, 8h30, desde 08/10/2026, ordem do Dr. Luiz) e de qualquer rodada feita à mão. Trava contra duplicidade:
se já houver commit "Notícias dos tribunais na home" do dia, a segunda rotina faz só o complemento: triagem das notícias que entraram depois e as traduções que faltarem; erro de git = para e avisa, nunca força. O programa é `noticias.py`; quem lê e decide é a rotina (Claude), não o programa.

## Ordem do Dr. Luiz (07/10/2026, verbatim)

> "existe notícia nos sites dos tribunais toda hora. vc deve buscar no stj e no stf uma vez por dia e
> atualizar, quando é sobre nossas áreas de atuação as notícias merecem ser detacadas, no penal vamos
> colocar somente notícias favoráveis, nunca contra. nas demais pode ser um tema aberto. quando os
> servidoes dos sites bloquearem vc deve acionar o chat imediatamente pelo duplo agente e pedir para
> ele. ele faz muito bem esse trabalho."

## O rito, todo dia

1. `python noticias.py candidatos --fonte stj --dias 7` (depois `stf`, depois `corteidh`). Ler o
   **texto** de cada candidata (campo `texto`), não só o título.
2. Montar um arquivo por fonte no formato do `registrar`:
   `{"avaliadas": [todos os links lidos], "destaques": [{"link", "motivo"}], "ocultar": [links],
     "materias": {link: ["chave-da-area", ...]}}`.
3. `python noticias.py registrar --fonte <fonte> <arquivo.json>` para cada fonte.
4. `python noticias.py atualizar --push` (vai ao ar sozinho, decisão do Dr. Luiz de 04/10/2026).
5. Conferir a última linha (`{"ok": true, ... "no_ar": true}`) e, se `erros` não estiver vazio,
   aplicar a seção "Quando o tribunal bloquear".

## Regras de classificação (chaves aceitas: `noticias.py: AREAS`)

| Área | Chave | O que entra |
|---|---|---|
| Direito Penal | `direito-penal` | **Só decisão ou notícia favorável à defesa.** Nunca notícia contra o réu (condenação mantida, pena aumentada, liberdade negada, tese da acusação acolhida). Decisão "de gume" (favorável num ponto e contrária noutro) não entra. |
| Execução Penal | `execucao-penal` | Mesma regra do penal: só o favorável ao apenado (progressão, detração, remição, livramento, prisão domiciliar, condições degradantes). |
| Tribunais Superiores | `tribunais-superiores` | Tema aberto: repetitivos, relevância da questão federal, repercussão geral, regimento e funcionamento do STJ/STF, pautas. Decisão penal favorável também entra aqui quando for repetitivo/relevância. |
| Imobiliário | `imobiliario` | Tema aberto: usucapião, condomínio, locação, registro, posse, incorporação, Airbnb. |
| Civil | `civil` | Tema aberto: contratos, responsabilidade civil, consumidor, bancos, prescrição, prova, execução civil, planos de saúde. |
| Família e Sucessões | `familia-e-sucessoes` | Tema aberto: guarda, alimentos, união estável, herança, testamento, animais de estimação. |
| Ambiental | `ambiental` | Tema aberto: licenciamento, fiscalização, Ibama, infração ambiental, povos indígenas e território. |
| Leilões | `leiloes` | Tema aberto: leilão judicial e extrajudicial, arrematação, penhora e expropriação de bens, alienação fiduciária. |

- **Destaque** (`destaques`, com `motivo` de uma frase): só decisão penal/execução **favorável à defesa**;
  o motivo diz por que é favorável. O destaque entra sozinho em Direito Penal; acrescente `materias`
  quando também couber em Execução Penal ou Tribunais Superiores.
- **Ocultar** (`ocultar`): título com **nome de parte, vítima ou investigado** (regra da casa; o item
  some da lista "últimas" da home). Notícia contra o réu não se oculta: apenas não se classifica.
- **Não entra em área nenhuma**: notícia institucional (posse, homenagem, evento, curso, podcast,
  programa de TV, manutenção de sistema, nota de pesar), tributário, administrativo, eleitoral,
  trabalhista. Fica só em `avaliadas`.
- Uma notícia pode levar mais de uma chave. Só se classifica link que esteja no feed atual
  (o `registrar` recusa o resto).

## Quando o tribunal bloquear (403, desafio anti-robô, feed vazio, `erros` na saída)

Ordem do Dr. Luiz: **acionar imediatamente a dupla** (`baldissera-dupla`, troca sem caso) e pedir ao
Codex que busque, com a ferramenta de navegação do próprio modelo, as notícias do dia no portal
bloqueado, devolvendo **título, data, link oficial e resumo** de cada uma. O Codex não grava nem
publica: a rotina recebe a lista, lê, classifica pelas regras acima e segue do passo 2.
- Brief: `~/.claude/plans/dupla-ia-claude-codex/trocas/<AAAA-MM-DD>-noticias-<fonte>/00-brief.md`
  (modelo nas trocas `2026-10-07-hc-*`); autorização a registrar: "ordem do Dr. Luiz de 07/10/2026
  (notícias bloqueadas → dupla)".
- No Mac, antes da dupla, vale tentar o navegador interno do app (abre STJ e STF quando o programa é
  barrado) e o navegador automático (`NAVEGADOR_PY`, scrapling).
- Fonte que continuar fora do ar não derruba as outras: o quadro dela fica como estava.

## Estado em 07/10/2026 (noite)

- Rodada feita à mão no Mac, com a classificação retroativa de tudo o que estava nos feeds
  (commit "Notícias dos tribunais na home (07/10/2026)"). A rotina do Windows **nunca tinha publicado**
  (nenhum commit dela no histórico) e nunca mandou `materias`: foi por isso que as áreas apareciam
  vazias. Ajustar o prompt da rotina no Windows por este arquivo.
- `noticias.py` passou a ler o STF por requisição simples quando o servidor responde (é o caso do Mac)
  e só abre o navegador automático se falhar; reconhece o scrapling do Mac
  (`~/.local/share/uv/tools/scrapling/bin/python`).


## Tradução das notícias em outra língua (ordem do Dr. Luiz, 08/10/2026)

Notícia em espanhol ou inglês (em regra da Corte IDH) fica no site com o título original, exatamente como está no site da fonte, e logo abaixo a tradução fiel para o português, com o rótulo "Tradução". O `candidatos` devolve a lista `traduzir` (itens das últimas notícias sem tradução); a rotina traduz cada um com exatidão, sem resumir, adaptar ou acrescentar, e manda no `registrar`:

```json
{"traducoes": {"<link>": {"titulo": "<tradução fiel do título>", "resumo": "<tradução fiel do resumo, se o resumo também estiver em outra língua>"}}}
```

As traduções ficam em `<fonte>/traducoes.json`. O idioma é detectado pelo texto do título (o site da Corte às vezes publica título em inglês na página em português).
