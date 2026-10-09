# Formato de um julgado explicado — `tools/execucao/julgados/<id>.json`

Um arquivo por julgado. É a fonte única da página `public/execucao-penal-em-linguagem-simples.html` e da lista "Julgamentos aguardados" da página de área. O HTML gerado nunca se edita à mão: corrige-se o JSON e gera-se de novo (`python3.12 tools/execucao/gerar_explicada.py`).

Regras da casa que o `validar.py` aplica: só `situacao: "publicar"` entra na página; nenhum `[CONFIRMAR`, `[COMPLETAR`, `[data]` ou `[SECUNDÁRIA` em texto publicado; sem "você", "procure um advogado", "fale conosco", "especializado", "esperança", "costuma"; "tem direito" só acompanhado de condição ("pode"); `url_oficial` em domínio oficial; `tese_verbatim` presente; `verificado_em` com data.

```json
{
  "id": "tema-1155",                       // = nome do arquivo; estável; prefixo do tribunal quando houver homônimo (stf-tema-1454)
  "materia": "detracao",                   // progressao | remicao | detracao | livramento | indulto | falta-grave | federal | condicoes | multa
  "ordem": 10,                             // ordem dentro da matéria (menor primeiro)
  "situacao": "publicar",                  // rascunho | aguarda-selagem | publicar
  "pendente": false,                       // true = bloco de julgamento aguardado (entra em "Do que ainda será julgado" e na lista da área)

  "titulo": "Quem ficou em casa à noite por ordem do juiz durante o processo pode ter esse tempo descontado da pena, com ou sem tornozeleira",
  "alcance": "Quem, enquanto respondia ao processo, ...",                 // "Quem pode ser alcançado" (≤ 60 palavras)
  "parabola": "Imagine um trabalhador que ... Na execução penal, a empresa é o Estado, ...",  // 80–130 palavras; abre com Imagine; fecha com a chave do mapa
  "exemplo": {                             // "Em números (exemplo fictício)"
    "premissas": "Recolhimento das 20h às 6h, dez horas por noite, durante trezentas noites.",
    "conta": "300 noites × 10 h = 3.000 h; 3.000 ÷ 24 = 125 dias",
    "texto": "São 3.000 horas. Convertidas em dias de 24 horas, dão 125 dias a menos de pena. ..."
  },
  "decidiu": "A Terceira Seção do STJ fixou, com efeito obrigatório ...",   // 1 frase, ≤ 45 palavras
  "limites": ["Só entra o período em que a medida esteve em vigor ...", "..."],   // 2–4 itens; sempre o que prejudica, inclusive o julgado contrário
  "documento": "O atestado de pena ... Se o desconto não aparece, o pedido de correção é feito ao juiz da execução.",
  "em_jogo": null,                         // só nos pendentes: "O STF vai dizer se ... Três saídas são possíveis: ..."
  "ate_la": null,                          // só nos pendentes: o que vale até o julgamento

  "selagem": {
    "tribunal": "STJ",
    "orgao": "Terceira Seção",
    "classe": "Tema Repetitivo 1.155 (REsp 1.977.135/SC)",
    "relator": "Min. Joel Ilan Paciornik",
    "julgamento": "2022-11-23",
    "publicacao": "2022-11-28",
    "transito": "2024-09-21",
    "tese_verbatim": "1) O período de recolhimento obrigatório noturno ...",   // integral, item por item, sem "(...)"
    "url_oficial": "https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?...",
    "situacao_publica": "em vigor",        // em vigor | afetado | repercussão geral reconhecida | aguardando publicação | pendente (ADI) | superado
    "nota_situacao": "A mesma matéria está pendente no STF (Tema 1.454).",
    "verificado_em": "2026-10-09",
    "verificado_por": "Claude, portal STJ (1ª passada); 2ª passada: pendente",
    "ficha": "dupla-ia-claude-codex/trocas/2026-10-09-execucao-levantamento-L1-stj"
  },

  "relacionados": {
    "publicacao": "publicacao-recolhimento-noturno-desconta-da-pena.html",   // ou null
    "revisao_ancora": "#roteiro",          // âncora na página "Revisão completa"
    "blocos": ["stf-tema-1454"],           // outros ids da própria página
    "erros_catalogo": ["E-07"]             // ids do catálogo da Revisão (quando migrado)
  },

  "audio": {
    "roteiro": "Este é um dos direitos de quem cumpre pena, explicado em linguagem simples. ...",   // 150–220 palavras; números por extenso; sem URL
    "narracao": {"arquivo": "assets/audio/execucao/tema-1155-narracao.mp3", "hash": null, "voz_id": null, "modelo": null, "gerado_em": null, "duracao_s": null, "caracteres": null},
    "titular":  {"arquivo": "assets/audio/execucao/tema-1155-titular.m4a", "gravado_em": null, "duracao_s": null}
  }
}
```

Os comentários `//` acima são explicativos; o arquivo real é JSON puro, sem comentários.
