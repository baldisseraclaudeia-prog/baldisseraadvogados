# Formato de uma publicação (JSON)

É o que a página "Publicar no site", o comando `/publicar` e a rotina de minutas produzem,
e o que `publicar.py` transforma em página do site.

```json
{
  "titulo": "Título completo, como aparece no topo da página",
  "titulo_curto": "Versão curta para a aba do navegador e a trilha (opcional)",
  "subtitulo": "Frase de abertura em itálico, abaixo do título",
  "resumo": "Duas ou três frases para o cartão da lista e para o Google",
  "area": "Direito Penal",
  "autor": "luiz | charys | karla | anderson",
  "data": "2026-09-25 (opcional; padrão = hoje)",
  "corpo": [
    {"tipo": "destaque", "texto": "Citação ou frase de impacto que abre o texto"},
    {"tipo": "paragrafo", "texto": "Parágrafo. Aceita **negrito** e *itálico*."},
    {"tipo": "intertitulo", "texto": "Título de seção"},
    {"tipo": "caixa", "rotulo": "Do voto", "titulo": "Título da caixa", "texto": "Texto da caixa"},
    {"tipo": "citacao", "texto": "Trecho literal de ementa ou voto", "fonte": "STJ — HC 000.000/UF, Rel. Min. ..., j. dd/mm/aaaa"}
  ],
  "referencias": [
    {"nome": "STJ · HC 000.000/UF", "descricao": "Órgão, relator, data e o que decidiu"}
  ]
}
```

Regras que o publicador aplica sozinho:
- Nada de HTML no texto: tudo é escapado; só `**negrito**` e `*itálico*` viram formatação.
- Sem numeração de publicação (decisão do Dr. Luiz, 25/09/2026). A ordem é a da lista: a mais nova no topo.
- Tempo de leitura calculado pelas palavras do corpo (250 por minuto).
- Endereço da página = `publicacao-` + título curto sem acento; se já existir, ganha `-2`, `-3`.
- Assinatura no fim = iniciais do autor; bloco "Sobre o autor" com os dados da página Advogados.

## Capas

A cada publicação o publicador gera três capas com a marca (`capa.py`): `og` 1200x630 (prévia de link, usada no og:image), `quadrado` 1080x1080 e `vertical` 1080x1350 (posts). Ficam em `public/assets/images/capas/<endereço>-<formato>.png`. `capas_existentes.py` gerou as das publicações anteriores a 27/09/2026.
