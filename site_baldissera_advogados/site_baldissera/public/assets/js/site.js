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
