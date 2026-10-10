// Baldissera Advogados — comportamento das páginas (protótipo "liturgia", 06/10/2026).
// Sem biblioteca externa e sem cookies. Tudo funciona mesmo se o navegador bloquear
// a memória local (localStorage): só não guarda a preferência de letra e contraste.
(function () {
  var raiz = document.documentElement;

  // ---------- memória local tolerante a bloqueio ----------
  function ler(chave) { try { return localStorage.getItem(chave); } catch (e) { return null; } }
  function gravar(chave, valor) { try { localStorage.setItem(chave, valor); } catch (e) { /* sem memória: segue */ } }

  // ---------- acessibilidade: tamanho da letra e alto contraste ----------
  var letra = parseInt(ler('ba-letra') || '0', 10);
  if (!(letra >= 0 && letra <= 3)) letra = 0;
  function aplicarLetra() { raiz.setAttribute('data-letra', String(letra)); }
  aplicarLetra();
  var contraste = ler('ba-contraste') === '1';
  function aplicarContraste() {
    raiz.classList.toggle('contraste', contraste);
    document.querySelectorAll('[data-contraste]').forEach(function (b) { b.setAttribute('aria-pressed', contraste ? 'true' : 'false'); });
  }
  aplicarContraste();
  document.querySelectorAll('[data-letra]').forEach(function (b) {
    if (b === raiz) return;
    b.addEventListener('click', function () {
      letra = Math.max(0, Math.min(3, letra + parseInt(b.getAttribute('data-letra'), 10)));
      aplicarLetra(); gravar('ba-letra', String(letra));
    });
  });
  document.querySelectorAll('[data-contraste]').forEach(function (b) {
    b.addEventListener('click', function () { contraste = !contraste; aplicarContraste(); gravar('ba-contraste', contraste ? '1' : '0'); });
  });

  // ---------- cabeçalho: compacto ao rolar; botão voltar ao topo ----------
  var cab = document.getElementById('cabecalho');
  var topo = document.querySelector('.voltar-topo');
  var fecho = document.querySelector('.fecho');
  function aoRolar() {
    var y = window.scrollY || 0;
    // histerese: compacta depois de 140 px, volta antes de 60 px (sem piscar no limite)
    if (cab) {
      if (y > 140) cab.classList.add('compacto');
      else if (y < 60) cab.classList.remove('compacto');
    }
    if (topo) topo.hidden = y < 900 || (fecho && fecho.getBoundingClientRect().top < window.innerHeight);
  }
  window.addEventListener('scroll', aoRolar, { passive: true });
  aoRolar();
  if (topo) topo.addEventListener('click', function () {
    var reduzir = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduzir ? 'auto' : 'smooth' });
    var alvo = document.getElementById('conteudo'); if (alvo) alvo.focus({ preventScroll: true });
  });

  // ---------- menu do celular ----------
  var botaoMenu = document.querySelector('.menu-botao');
  var menu = document.getElementById('menu');
  if (botaoMenu && menu) {
    botaoMenu.addEventListener('click', function () {
      var aberto = botaoMenu.getAttribute('aria-expanded') === 'true';
      botaoMenu.setAttribute('aria-expanded', aberto ? 'false' : 'true');
      menu.classList.toggle('aberto', !aberto);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('aberto')) {
        botaoMenu.setAttribute('aria-expanded', 'false'); menu.classList.remove('aberto'); botaoMenu.focus();
      }
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) { botaoMenu.setAttribute('aria-expanded', 'false'); menu.classList.remove('aberto'); }
    });
  }

  // ---------- data de hoje em "Hoje nos tribunais" ----------
  var hoje = document.querySelector('[data-hoje]');
  if (hoje) {
    try {
      var txt = new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
      hoje.textContent = txt.charAt(0).toUpperCase() + txt.slice(1);
    } catch (e) { /* mantém o texto que veio no HTML */ }
  }

  // ---------- "Você sabia?": setas e aviso de fim ----------
  var sabia = document.getElementById('sabia-lista');
  if (sabia) {
    var setas = document.querySelectorAll('[data-rolar]');
    function estado() {
      var fim = sabia.scrollLeft + sabia.clientWidth >= sabia.scrollWidth - 4;
      sabia.classList.toggle('no-fim', fim);
      setas.forEach(function (b) {
        b.disabled = b.getAttribute('data-rolar') === '-1' ? sabia.scrollLeft <= 4 : fim;
      });
    }
    setas.forEach(function (b) {
      b.addEventListener('click', function () {
        var reduzir = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        sabia.scrollBy({ left: parseInt(b.getAttribute('data-rolar'), 10) * sabia.clientWidth * 0.8, behavior: reduzir ? 'auto' : 'smooth' });
      });
    });
    sabia.addEventListener('scroll', estado, { passive: true });
    window.addEventListener('resize', estado);
    estado();
  }


  // ---------- confirmação depois de formulário (o formsubmit volta com ?enviado=1 ou ?inscrito=1) ----------
  var conteudo = document.getElementById('conteudo');
  var aviso = /[?&]enviado=1/.test(location.search) ? 'Mensagem enviada. O escritório responde pelo contato informado.'
            : /[?&]inscrito=1/.test(location.search) ? 'Inscrição recebida. As próximas publicações chegarão ao seu e-mail.' : '';
  if (conteudo && aviso && !document.querySelector('#agendar')) {
    var p = document.createElement('p');
    p.className = 'confirmacao'; p.setAttribute('role', 'status'); p.textContent = aviso;
    conteudo.insertBefore(p, conteudo.firstChild);
  }

  // ---------- busca "O que você procura?" ----------
  var indice = null, carregando = null;
  function carregar() {
    if (indice) return Promise.resolve(indice);
    if (!carregando) {
      carregando = fetch('/assets/busca.json').then(function (r) { return r.json(); })
        .then(function (d) {
          indice = d.map(function (i) { i._chave = normal([i.titulo, i.area, i.resumo, i.tipo].join(' ')); return i; });
          return indice;
        })
        .catch(function () { indice = []; return indice; });
    }
    return carregando;
  }
  function normal(t) { return (t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }

  document.querySelectorAll('.busca').forEach(function (form, n) {
    var campo = form.querySelector('input[type="search"]');
    var lista = form.querySelector('.busca-resultados');
    if (!campo || !lista) return;
    var ativo = -1, achados = [];

    function fechar() { lista.hidden = true; campo.setAttribute('aria-expanded', 'false'); campo.removeAttribute('aria-activedescendant'); ativo = -1; }
    function marcar(i) {
      var itens = lista.querySelectorAll('[role="option"]');
      itens.forEach(function (li, k) { li.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
      ativo = i;
      if (i >= 0 && itens[i]) { campo.setAttribute('aria-activedescendant', itens[i].id); itens[i].scrollIntoView({ block: 'nearest' }); }
      else campo.removeAttribute('aria-activedescendant');
    }
    function mostrar(q) {
      var termos = normal(q).split(/\s+/).filter(function (t) { return t.length > 1; });
      if (!termos.length) { fechar(); return; }
      carregar().then(function (d) {
        // aceita singular e plural ("leilao" acha "leiloes"): termo longo vale também pelo radical
        function tem(chave, t) { return chave.indexOf(t) !== -1 || (t.length >= 6 && chave.indexOf(t.slice(0, -2)) !== -1); }
        achados = d.filter(function (i) { return termos.every(function (t) { return tem(i._chave, t); }); }).slice(0, 7);
        lista.innerHTML = '';
        if (!achados.length) {
          var vazio = document.createElement('li');
          vazio.className = 'busca-vazio';
          vazio.textContent = 'Nada encontrado para “' + q + '”. Tente o nome do tema, do tribunal ou da área.';
          lista.appendChild(vazio);
        }
        achados.forEach(function (i, k) {
          var li = document.createElement('li');
          li.setAttribute('role', 'option'); li.id = 'res-' + n + '-' + k; li.setAttribute('aria-selected', 'false');
          var a = document.createElement('a'); a.href = i.url; a.tabIndex = -1;
          var t = document.createElement('span'); t.className = 'res-titulo'; t.textContent = i.titulo;
          var m = document.createElement('span'); m.className = 'res-meta';
          m.textContent = i.tipo + (i.area ? ', ' + i.area : '') + (i.data ? ', ' + i.data : '');
          a.appendChild(t); a.appendChild(m); li.appendChild(a); lista.appendChild(li);
          li.addEventListener('mousedown', function (e) { e.preventDefault(); location.href = i.url; });
        });
        lista.hidden = false; campo.setAttribute('aria-expanded', 'true'); ativo = -1;
      });
    }
    campo.addEventListener('focus', carregar);
    campo.addEventListener('input', function () { mostrar(campo.value); });
    campo.addEventListener('keydown', function (e) {
      if (lista.hidden) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); marcar(Math.min(achados.length - 1, ativo + 1)); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); marcar(Math.max(-1, ativo - 1)); }
      else if (e.key === 'Escape') { fechar(); }
      else if (e.key === 'Enter' && ativo >= 0 && achados[ativo]) { e.preventDefault(); location.href = achados[ativo].url; }
    });
    campo.addEventListener('blur', function () { setTimeout(fechar, 150); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (achados[0]) location.href = achados[Math.max(0, ativo)].url;
    });
  });

  // Julgados explicados: escolha da voz (narração | na voz do advogado) e um áudio por vez
  Array.prototype.forEach.call(document.querySelectorAll('[data-faixas]'), function (caixa) {
    var botoes = caixa.querySelectorAll('.ex-faixas [data-faixa]'), faixas = caixa.querySelector('.ex-faixas');
    var audios = caixa.querySelectorAll('audio[data-faixa]'), nomes = caixa.querySelectorAll('.ex-faixa-nome[data-faixa]');
    if (audios.length < 2) return;
    faixas.hidden = false;
    function mostrar(k) {
      Array.prototype.forEach.call(audios, function (a) { a.hidden = a.getAttribute('data-faixa') !== k; if (a.hidden) a.pause(); });
      Array.prototype.forEach.call(nomes, function (n) { n.hidden = n.getAttribute('data-faixa') !== k; });
      Array.prototype.forEach.call(botoes, function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-faixa') === k ? 'true' : 'false'); });
    }
    Array.prototype.forEach.call(botoes, function (b) { b.addEventListener('click', function () { mostrar(b.getAttribute('data-faixa')); }); });
    mostrar(botoes[0].getAttribute('data-faixa'));
  });
  Array.prototype.forEach.call(document.querySelectorAll('audio'), function (a) {
    a.addEventListener('play', function () {
      Array.prototype.forEach.call(document.querySelectorAll('audio'), function (o) { if (o !== a) o.pause(); });
    });
  });

})();

/* Copiar o link da página (bloco "Compartilhar", 09/10/2026) */
document.addEventListener("click", function (e) {
  var b = e.target.closest && e.target.closest("[data-copiar]"); if (!b) return;
  var url = b.getAttribute("data-copiar");
  var ok = function () { var n = b.closest(".compartilhar").querySelector("[data-copiado]"); if (n) { n.hidden = false; setTimeout(function () { n.hidden = true; }, 2500); } };
  var velho = function () { var t = document.createElement("textarea"); t.value = url; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); } catch (x) {} t.remove(); ok(); };
  if (navigator.clipboard) navigator.clipboard.writeText(url).then(ok, velho); else velho();
});
