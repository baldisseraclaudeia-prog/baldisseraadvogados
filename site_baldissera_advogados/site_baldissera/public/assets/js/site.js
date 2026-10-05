/* Botão flutuante do WhatsApp no celular (04/10/2026):
   recolhe enquanto a pessoa rola para baixo lendo, para não cobrir o texto,
   e volta quando ela sobe a página, para de rolar no topo ou chega ao fim. */
(function () {
  var botao = document.querySelector('.wa-float-btn');
  if (!botao || !window.matchMedia) return;
  var estreita = window.matchMedia('(max-width: 900px)');
  var ultimo = window.scrollY;

  function atualizar() {
    var y = window.scrollY;
    var fim = y + window.innerHeight >= document.documentElement.scrollHeight - 120;
    if (!estreita.matches || y < 240 || fim || y < ultimo - 4) {
      botao.classList.remove('recolhido');
    } else if (y > ultimo + 4) {
      botao.classList.add('recolhido');
    }
    ultimo = y;
  }

  window.addEventListener('scroll', atualizar, { passive: true });
})();

/* Página inicial — abas "Dos tribunais." (STJ | STF | Corte IDH), 04/10/2026.
   Sem este script os três painéis aparecem um embaixo do outro. */
(function () {
  var secao = document.querySelector('.trib-noticias');
  if (!secao) return;
  var abas = Array.prototype.slice.call(secao.querySelectorAll('[role="tab"]'));
  if (!abas.length) return;

  function escolher(aba, foco) {
    abas.forEach(function (a) {
      var ativa = a === aba;
      a.setAttribute('aria-selected', ativa ? 'true' : 'false');
      a.tabIndex = ativa ? 0 : -1;
      document.getElementById(a.getAttribute('aria-controls')).hidden = !ativa;
    });
    if (foco) aba.focus();
  }

  abas.forEach(function (aba, i) {
    aba.addEventListener('click', function () { escolher(aba, false); });
    aba.addEventListener('keydown', function (e) {
      var n = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: abas.length - 1 }[e.key];
      if (n === undefined) return;
      e.preventDefault();
      escolher(abas[(n + abas.length) % abas.length], true);
    });
  });
  secao.classList.add('com-abas');
  escolher(abas[0], false);
})();
