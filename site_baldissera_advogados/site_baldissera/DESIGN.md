---
name: Baldissera Advogados — Liturgia
description: O site se lê como peça forense, sobre papel de autos.
colors:
  toga: "#0F172A"
  toga-2: "#1B2537"
  papel: "#F7F3EA"
  papel-2: "#EEE7D7"
  ouro: "#9B7B3A"
  ouro-texto: "#806328"
  tinta: "#1E222B"
  tinta-2: "#4A4F5A"
  linha: "#D6CCB6"
  marfim: "#F5F1E8"
  marfim-2: "#E7E1D2"
  marfim-3: "#D9D3C5"
  cinza-toga: "#C9C3B4"
  cinza-toga-2: "#A9A394"
  ouro-claro: "#C9B98A"
  ouro-palido: "#E7D6A8"
  noite: "#0A1020"
  campo: "#FFFDF8"
  borda-campo: "#8F8468"
  campo-escuro: "#16203A"
  whatsapp: "#1FA855"
typography:
  display:
    fontFamily: "Cormorant Garamond, Garamond, Times New Roman, serif"
    fontSize: "3.75rem"
    fontWeight: 500
    lineHeight: 1.08
  heading:
    fontFamily: "Cormorant Garamond, Garamond, Times New Roman, serif"
    fontSize: "2.25rem"
    fontWeight: 500
    lineHeight: 1.15
  body:
    fontFamily: "Source Serif 4, Georgia, Times New Roman, serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Source Serif 4, Georgia, serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    letterSpacing: "0.08em"
rounded:
  none: "0"
spacing:
  medida: "36rem"
  largura: "68rem"
  recuo: "1.27cm"
components:
  botao:
    backgroundColor: "{colors.toga}"
    textColor: "{colors.papel}"
    rounded: "{rounded.none}"
    padding: "0.95rem 2rem"
  botao-hover:
    backgroundColor: "{colors.toga-2}"
---

# Design System: Baldissera Advogados — Liturgia

Aprovado pelo Dr. Luiz em 06/10/2026. Fonte da verdade: `public/assets/css/liturgia.css` (tokens no `:root`). Este arquivo descreve o sistema; não o substitui.

## Overview

A página é uma peça forense: timbre, filete duplo dourado, seções numeradas em romano ("I. Das publicações"), ementa recuada, parágrafo justificado com recuo de primeira linha e fecho com assinatura. Referências: portais do STF, da Corte IDH e da Suprema Corte dos EUA. Sobriedade de documento oficial, nunca de página de vendas.

## Colors

### Primary
- **Toga** `#0F172A`: cabeçalho, rodapé, faixas escuras, botão.
- **Ouro** `#9B7B3A`: filetes, marca e ícones. Nunca texto pequeno.
- **Ouro-texto** `#806328`: dourado legível sobre o papel (rótulos, datas).

### Neutral
- **Papel** `#F7F3EA`: fundo, o "papel de autos". É a identidade, não um bege padrão.
- **Papel-2** `#EEE7D7`: caixas (ementa, aviso).
- **Tinta** `#1E222B` / **Tinta-2** `#4A4F5A`: texto corrido e secundário.
- **Linha** `#D6CCB6`: fios finos de separação.

### Sobre o marinho (cabeçalho, barra superior, rodapé, faixas escuras)
- **Marfim** `#F5F1E8` / `#E7E1D2` / `#D9D3C5`: texto e títulos sobre a toga.
- **Ouro-claro** `#C9B98A`: menu, rótulos e fios sobre a toga; **ouro-pálido** `#E7D6A8`: contorno de foco no escuro.
- **Cinza-toga** `#C9C3B4` / `#A9A394`: contatos e linha final do rodapé.
- **Noite** `#0A1020`: barra superior de contatos.

### Campos
- **Campo** `#FFFDF8` com **borda-campo** `#8F8468` (3,4:1 sobre o papel).

### Named Rules
- Alto contraste (`html.contraste`) troca papel por branco e tinta por preto.

## Typography

Cormorant Garamond para títulos; Source Serif 4 para o corpo. Escala de razão ~1,25 sobre 18 px (`--t-0` 13 px a `--t-7` 60 px). Rótulos em versalete (`all-small-caps`) com espaçamento 0,06–0,10em: é só para rótulos curtos, nunca para parágrafo.

### Hierarchy
- Título de abertura: `--t-7`; título de página/publicação: `--t-6`; seção: `--t-5`; subtítulo: `--t-4`/`--t-3`.
- Corpo de publicação: coluna `--medida` (~66 caracteres), justificado, hifenizado, recuo de 1,27 cm.

## Layout

Largura máxima 68rem, gutter 1.5rem. Seções separadas por fio fino (`--linha`) e cabeçalho centralizado com numeral romano dourado. Grades de 2 a 4 colunas que caem para 1 no celular.

## Elevation & Depth

Plano, como papel. Profundidade só onde há sobreposição real (resultados da busca, botão voltar ao topo). Sem cartões com sombra.

## Shapes

Cantos retos em tudo (`border-radius: 0`). Filete duplo (`4px`/`6px double` ouro) marca cabeçalho, rodapé e aberturas de bloco.

## Components

### Buttons
`.botao`: toga sobre papel, versalete, sem arredondamento. `.remissao`: link sublinhado em ouro, sem seta.

### Cards / Containers
Sem cartões. Listas separadas por fios; caixas (`.caixa`, `.aviso`) em papel-2 com filete lateral ouro, que é o grifo da peça.

### Inputs / Fields
Fundo `#FFFDF8`, borda `#B9AE95`, sem arredondamento, foco com contorno toga 2px.

### Navigation
Cabeçalho escuro fixo que compacta ao rolar; menu em versalete ouro-claro; no celular, botão "Menu".

### Ementa (signature component)
Recuada a 40% da coluna, com filete vertical ouro de 3px, como a ementa no alto do acórdão.

## Do's and Don'ts

### Do:
- Usar os tokens do `:root`; tudo por classe.
- Manter numeral romano, versalete e filete duplo: são a liturgia.
- Ilustração em gravura a traço, um símbolo por área.

### Don't:
- Sem gradientes, vidro, sombra decorativa, cantos arredondados, emojis.
- Sem foto de sala/gabinete, superlativos ou chamada mercantil (Provimento 205).
- Sem `style=""` nas páginas; sem editar à mão o HTML gerado pelo publicador.
