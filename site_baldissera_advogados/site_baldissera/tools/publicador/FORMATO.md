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

## Área e "Tribunais Superiores" (desde 27/09/2026)

- `area` tem de ser uma das 7 da lista do site: **Direito Penal, Tribunais Superiores, Execução Penal, Imobiliário, Civil, Família e Sucessões, Ambiental**. O publicador aceita grafias próximas ("Direito Civil", "Processual Penal", "Recursos aos Tribunais Superiores", "Direito Penal · Lei de Drogas") e as traduz para a oficial; área desconhecida trava a publicação.
- `superior` (opcional, `true`/`false`): marca a publicação como análise de julgado do STF/STJ, o que a faz aparecer também no botão "Tribunais Superiores" da lista, agrupada pela sua área. Sem o campo, o publicador detecta sozinho (STF, STJ, REsp, AREsp, ADPF, ADI, RE n., Tema n., repercussão geral no título, subtítulo, resumo, citações ou referências). Quem aprova pode desligar com `"superior": false`.
- Cada cartão da lista sai com `class="pub-card" data-area data-superior data-data`; a página `publicacoes.html` filtra por esses atributos (botões) e ordena por data. `classificar_existentes.py` aplicou isso às publicações anteriores a 27/09/2026.

## Ilustração (desde 27/09/2026)

Campos opcionais:

```json
{
  "imagem": "publicacao-adpf-347-na-execucao-penal.png",
  "imagem_alt": "Arco de pedra sobre água noturna, com um caminho de folhas de papel que o atravessa."
}
```

- `imagem`: nome (ou caminho) do PNG gerado pelo diretor de arte (agente `baldissera-diretor-arte`), guardado em `PAINEL-PUBLICACAO\IMAGENS\`. Se o campo faltar, o publicador procura sozinho `IMAGENS\<endereço>.png`; `"imagem": false` desliga a ilustração.
- `imagem_alt`: descrição neutra da imagem (acessibilidade e buscadores). Sem ela, entra "Ilustração editorial da publicação".
- O publicador converte o PNG em JPG leve (1600 px) em `public/assets/images/publicacoes/<endereço>.jpg`, põe a figura abaixo da linha de autoria do hero (`<figure class="pub-fig">`) e usa a mesma ilustração como fundo das capas.
- Regras da imagem (checklist do agente): sem pessoas, martelo, balança, algemas, grades, brasão, texto; sem alusão a caso ou cliente; nas cores da marca.

## Capas

A cada publicação o publicador gera três capas com a marca (`capa.py`): `og` 1200x630 (prévia de link, usada no og:image), `quadrado` 1080x1080 e `vertical` 1080x1350 (posts). Ficam em `public/assets/images/capas/<endereço>-<formato>.png`. Com ilustração, ela ocupa o fundo da capa sob um véu marinho com a marca vetorial oficial (`public/assets/images/marca/baldissera-advogados-escuro.svg`); sem ilustração, a capa é tipográfica. `capas_existentes.py` gerou as das publicações anteriores a 27/09/2026.
