# Product

<!-- impeccable:product-schema 1 -->

> Registro escrito em 08/10/2026 a partir de `docs/BRIEFING.md`, `CLAUDE.md` e do site no ar, por ordem do Dr. Luiz ("faça tudo"), sem a entrevista do `init`. Fatos inferidos dos documentos do projeto; o que não consta deles fica marcado como aberto.

## Platform

web

## Users

- Quem procura defesa ou orientação jurídica, muitas vezes a família de alguém investigado, preso ou condenado, chegando pelo celular a partir do Instagram, do Google ou de um link compartilhado.
- Advogados e estudantes que leem as análises de julgados (STJ, STF, Corte IDH) publicadas pelo escritório.
- O trabalho do visitante: entender o que uma decisão muda para ele, saber quem é o escritório e marcar um atendimento.

## Product Purpose

Site institucional e editorial da Baldissera Advogados (sociedade OAB/PR 4.545), escritório com foco em defesa criminal e execução penal, também cível, imobiliário/leilões, ambiental, família e sucessões, e recursos aos tribunais superiores. Sucesso: o visitante entende a análise, confia na técnica da casa e agenda atendimento sem que o site peça por isso.

## Positioning

O site se lê como peça forense: análises de julgados escritas com a disciplina de uma petição (ementa, fundamentação, fontes oficiais, assinatura), e não como página de vendas.

## Operating Context

- Publicações geradas por `tools/publicador/publicar.py` a partir de JSON; molde comum por `tools/molde.py`; notícias diárias dos tribunais por `tools/noticias/noticias.py`.
- Publicação e post do Instagram às 12h (segunda do dia às 19h).
- Unidades: Cascavel/PR, Porto Alegre/RS, Foz do Iguaçu/PR, Porto Belo/SC.

## Capabilities and Constraints

- Site estático (HTML + CSS + `site.js` pequeno), servido pela Vercel; sem build.
- Uma folha de estilo só (`public/assets/css/liturgia.css`); nenhum `style=""` nas páginas.
- HTML de publicação nunca se edita à mão: corrige-se o JSON ou o gerador.
- Formulários por FormSubmit para contato@baldisseraadvogados.com.br.

## Brand Commitments

- Provimento OAB 205/2021: sem superlativos, comparações, promessa de resultado, menção a caso ou cliente, chamada mercantil, valores ou foto de sala/gabinete.
- Tom sóbrio e técnico, português do Brasil, sem emojis, sem autoelogio.
- Rodapé com a sociedade (OAB/PR 4.545 · CNPJ 24.129.499/0001-08); OAB pessoal só em publicação e perfil.
- @luizhbaldissera e @baldisseraadvocacia em toda publicação.

## Evidence on Hand

Publicações reais em `public/publicacao-*.html`; fotos reais da equipe; ilustrações em gravura a traço aprovadas. Não há depoimentos, números de casos nem resultados — e não podem ser criados.

## Product Principles

1. Técnica antes de retórica: a análise prova a competência; o site não a declara.
2. Efeito prático na primeira tela: o que muda para o preso e para a família.
3. Conformidade com o Provimento 205 vale mais que qualquer recurso de conversão.
4. Fonte oficial em toda afirmação jurídica.

## Accessibility & Inclusion

Barra de acessibilidade própria (A−/A+, alto contraste); público inclui pessoas idosas e leitura em celular. Meta: WCAG 2.1 AA.
