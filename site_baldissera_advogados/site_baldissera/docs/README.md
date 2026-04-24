# BALDISSERA ADVOGADOS — Site Institucional

Pacote completo do site institucional da banca Baldissera Advogados, pronto para deploy.

## CONTEÚDO

```
site_baldissera/
├── public/                          → 18 páginas HTML autônomas
│   ├── index.html                   → Página inicial
│   ├── sobre.html                   → Sobre o escritório
│   ├── areas-de-atuacao.html        → Índice de áreas
│   ├── area-direito-penal.html      → 7 páginas de áreas internas
│   ├── area-recursos-tribunais-superiores.html
│   ├── area-execucao-penal.html
│   ├── area-direito-imobiliario.html
│   ├── area-direito-civil.html
│   ├── area-familia-sucessoes.html
│   ├── area-direito-ambiental.html
│   ├── advogados.html               → Índice de advogados
│   ├── perfil-luiz.html             → 3 perfis individuais
│   ├── perfil-charys.html
│   ├── perfil-karla.html
│   ├── publicacoes.html             → Hub editorial
│   ├── contato.html                 → Contato + unidades + formulário
│   ├── politica-de-privacidade.html → LGPD
│   └── aviso-provimento-205.html    → Conformidade OAB
│
├── assets/
│   ├── css/
│   │   └── style.css                → CSS global compartilhado
│   └── images/
│       ├── luiz-henrique-baldissera.jpg → 600×750 PB editorial
│       └── karla-sampaio.jpg            → 600×750 PB editorial
│
└── docs/
    ├── README.md                    → Este documento
    ├── DEPLOY.md                    → Instruções de publicação
    └── PENDENCIAS.md                → Lista de pendências para fechar antes do go-live
```

## ESPECIFICAÇÕES TÉCNICAS

- **Total de páginas:** 18 HTMLs autônomos + 1 CSS global + 2 imagens
- **Tamanho total:** aproximadamente 250 KB (extremamente leve)
- **Tipografia:** Cormorant Garamond (Google Fonts) + sistema sans-serif
- **Paleta:** Navy #0F172A · Dourado #9B7B3A · Ivory #F5F1E8
- **Responsivo:** Sim, adaptado para mobile e desktop
- **Sem dependências:** HTML/CSS puro, sem JavaScript externo, sem build system
- **SEO-ready:** Meta tags, títulos, descriptions em todas as páginas
- **Compatibilidade:** Todos os navegadores modernos

## TESTE LOCAL

Para visualizar o site no seu computador antes de publicar:

1. Descompacte o pacote ZIP
2. Abra a pasta `public/`
3. Clique duas vezes em `index.html` — abre no navegador

Todas as páginas se abrem com links funcionais entre elas. As imagens são carregadas relativamente.

## PRÓXIMO PASSO

Veja `docs/DEPLOY.md` para instruções completas de publicação no Vercel (gratuito, leva 5 minutos).

---

**Baldissera Advogados** · OAB/PR 55.717
Cascavel · Porto Alegre · Foz do Iguaçu · Rio de Janeiro
