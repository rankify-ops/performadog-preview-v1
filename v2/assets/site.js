/* Performadog v2 preview, small, dependency-free behaviours. */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Mobile menu
  var mb = $('.menu-btn'), dr = $('.drawer');
  if (mb && dr) mb.addEventListener('click', function () {
    var open = dr.classList.toggle('open');
    mb.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Filter chips: <div data-filter-group="x"> chips with data-filter, items with data-tags
  $$('[data-filter-group]').forEach(function (grp) {
    var target = $(grp.getAttribute('data-target'));
    $$('[data-filter]', grp).forEach(function (chip) {
      chip.addEventListener('click', function () {
        $$('[data-filter]', grp).forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
        chip.setAttribute('aria-pressed', 'true');
        var f = chip.getAttribute('data-filter');
        $$('[data-tags]', target).forEach(function (it) {
          it.style.display = (f === 'all' || (' ' + it.getAttribute('data-tags') + ' ').indexOf(' ' + f + ' ') > -1) ? '' : 'none';
        });
      });
    });
  });

  // Postcode demo (preview logic only, real zones live in Shopify)
  var METRO = [[3000, 3207], [3335, 3341], [3427, 3429], [3750, 3810], [3910, 3920], [3926, 3944], [3975, 3978],
    [2000, 2234], [2555, 2574], [2740, 2786], [4000, 4207], [4300, 4305], [4500, 4519], [5000, 5199],
    [6000, 6199], [7000, 7099], [2600, 2620], [2900, 2914], [800, 832]];
  function zone(pc) {
    var n = parseInt(pc, 10); if (isNaN(n) || String(pc).length < 3) return null;
    for (var i = 0; i < METRO.length; i++) if (n >= METRO[i][0] && n <= METRO[i][1]) return 'metro';
    return 'regional';
  }
  $$('[data-postcode]').forEach(function (box) {
    var inp = $('input', box), btn = $('button', box), out = $('[data-postcode-out]', box);
    function run() {
      var z = zone(inp.value.trim());
      if (!z) { out.textContent = 'Enter a 4-digit postcode.'; return; }
      out.innerHTML = z === 'metro'
        ? '<strong>Metro area.</strong> Free delivery on orders over $150, otherwise a flat metro rate. Usually 2–4 business days.'
        : '<strong>Regional area.</strong> We deliver here. A freight surcharge applies and is shown before you pay. No surprises at checkout. Usually 5–7 business days.';
    }
    btn.addEventListener('click', run);
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); run(); } });
  });

  // Product page: size + purchase option
  var pdp = $('[data-pdp]');
  if (pdp) {
    var sizes = $$('.size', pdp), price = $('[data-price]', pdp), per = $('[data-per]', pdp);
    var subP = $('[data-sub-price]', pdp), onceP = $('[data-once-price]', pdp), atc = $('[data-atc]', pdp);
    function pick(b) {
      sizes.forEach(function (s) { s.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      var p = parseFloat(b.getAttribute('data-p')), kg = parseFloat(b.getAttribute('data-kg'));
      if (onceP) onceP.textContent = '$' + p.toFixed(2);
      if (price) price.textContent = '$' + p.toFixed(2);
      if (per && kg) per.textContent = '$' + (p / kg).toFixed(2) + '/kg';
      var pdEl = $('[data-pdp-pd]'); if (pdEl && b.getAttribute('data-pd')) pdEl.textContent = '$' + b.getAttribute('data-pd') + '/day';
      var sa = $('[data-sa-price]'); if (sa) sa.textContent = '$' + p + ' · ' + b.getAttribute('data-size');
    }
    sizes.forEach(function (b) { if (!b.disabled) b.addEventListener('click', function () { pick(b); }); });
    var opts = $$('.opt', pdp);
    opts.forEach(function (o) {
      o.addEventListener('click', function () {
        opts.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        o.setAttribute('aria-pressed', 'true');
        var l = atc && atc.querySelector('[data-atc-label]'); if (l) l.textContent = o.getAttribute('data-mode') === 'sub' ? 'Add to cart · subscribe' : 'Add to cart';
      });
    });
  }

  // Feeding calculator, anchored to the feeding table printed on the bag
  var calc = $('[data-calc]');
  if (calc) {
    var CURVE = [[2, 45], [7.5, 95], [15, 125], [25, 160], [35, 200], [45, 250], [60, 310]];
    function interp(kg) {
      if (kg <= CURVE[0][0]) return CURVE[0][1] * (kg / CURVE[0][0]);
      for (var i = 1; i < CURVE.length; i++) if (kg <= CURVE[i][0]) {
        var a = CURVE[i - 1], b = CURVE[i], t = (kg - a[0]) / (b[0] - a[0]); return a[1] + t * (b[1] - a[1]);
      }
      return CURVE[CURVE.length - 1][1];
    }
    var FOODS = {
      turkey: { name: 'Turkey Grain Free', url: 'turkey-grain-free.html', bag: 15, price: 168 },
      ocean: { name: 'Ocean Fish', url: 'ocean-fish.html', bag: 15, price: 160 },
      puppy: { name: 'Puppy Lamb & Fish', url: 'puppy-lamb-and-fish.html', bag: 15, price: 168 }
    };
    var state = { stage: 'adult', load: 'active', gut: 'no', pup: '5' };
    var params = new URLSearchParams(location.search);
    if (params.get('goal') === 'work') state.load = 'working';
    if (params.get('goal') === 'puppy') state.stage = 'puppy';
    if (params.get('goal') === 'gut') state.gut = 'yes';
    if (params.get('goal') === 'family') state.load = 'active';
    var w = $('#cw'), wOut = $('[data-cw]');
    function setPressed(group, val) {
      $$('[data-set="' + group + '"]', calc).forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-val') === val ? 'true' : 'false'); });
    }
    function run() {
      var kg = +w.value; wOut.textContent = kg + ' kg';
      var g = interp(kg);
      if (state.stage === 'puppy') g *= ({ '3': 2.0, '5': 1.65, '7': 1.4, '10': 1.2 })[state.pup] || 1.55;
      if (state.stage === 'senior') g *= 0.9;
      if (state.load === 'working') g *= 1.15;
      if (state.load === 'light') g *= 0.85;
      g = Math.round(g / 5) * 5;
      var food = state.stage === 'puppy' ? FOODS.puppy : (state.gut === 'yes' ? FOODS.ocean : (state.load === 'working' ? FOODS.turkey : FOODS.ocean));
      var days = Math.round(food.bag * 1000 / g);
      $('[data-o-g]').textContent = g + 'g';
      $('[data-o-food]').textContent = food.name;
      $('[data-o-food-link]').setAttribute('href', food.url);
      $('[data-o-days]').textContent = days + ' days';
      $('[data-o-cost]').textContent = '$' + (food.price / days).toFixed(2);
      calc._food = food;
      $('[data-o-every]').textContent = 'every ' + Math.max(1, Math.round(days / 7)) + ' weeks';
      $('[data-o-meals]').textContent = Math.round(g / 2) + 'g twice a day';
      $('[data-pup-row]').style.display = state.stage === 'puppy' ? '' : 'none';
    }
    $$('[data-set]', calc).forEach(function (b) {
      b.addEventListener('click', function () { state[b.getAttribute('data-set')] = b.getAttribute('data-val'); setPressed(b.getAttribute('data-set'), b.getAttribute('data-val')); run(); });
    });
    ['stage', 'load', 'gut', 'pup'].forEach(function (k) { setPressed(k, state[k]); });
    w.addEventListener('input', run); run();
  }

  // Contact form (preview)
  $$('form[data-preview]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); var o = $('[data-form-out]', f); if (o) o.textContent = 'Preview only. On the live site this sends to the Performadog inbox.'; });
  });
})();
(function () {
  // Library search
  var q = document.querySelector('[data-lib-search]');
  if (q) q.addEventListener('input', function () {
    var v = q.value.trim().toLowerCase();
    document.querySelectorAll('#lgrid [data-title]').forEach(function (c) {
      c.style.display = !v || c.getAttribute('data-title').indexOf(v) > -1 || c.textContent.toLowerCase().indexOf(v) > -1 ? '' : 'none';
    });
  });
  // Click-to-load YouTube
  document.querySelectorAll('[data-yt]').forEach(function (b) {
    b.addEventListener('click', function () {
      var id = b.getAttribute('data-yt'), t = b.querySelector('.vthumb');
      t.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1" title="Video" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>';
    });
  });
})();

/* ===== v2.1 store: cart, buy boxes, sticky ATC, steel sheen ===== */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var FREE = 150, KEY = 'pd-preview-cart', cart = [];
  try { cart = JSON.parse(localStorage.getItem(KEY) || '[]') || []; } catch (e) { cart = []; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {} }
  function money(v) { return '$' + (Math.round(v * 100) / 100).toFixed(v % 1 ? 2 : 0); }
  var drawer = $('[data-cart]'), scrim = $('.cart-scrim');
  function open() { if (!drawer) return; drawer.hidden = false; void drawer.offsetWidth; drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); scrim.hidden = false; }
  function close() { if (!drawer) return; drawer.classList.remove('open'); setTimeout(function () { if (!drawer.classList.contains('open')) drawer.hidden = true; }, 300); drawer.setAttribute('aria-hidden', 'true'); scrim.hidden = true; }
  $$('[data-cart-open]').forEach(function (b) { b.addEventListener('click', open); });
  $$('[data-cart-close]').forEach(function (b) { b.addEventListener('click', close); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  function render() {
    var n = cart.reduce(function (a, i) { return a + i.qty; }, 0), sub = cart.reduce(function (a, i) { return a + i.qty * i.price; }, 0);
    $$('[data-cart-count]').forEach(function (c) { c.textContent = n; c.setAttribute('data-n', n); });
    var box = $('[data-cart-items]'); if (!box) return;
    box.innerHTML = cart.length ? '' : '<p class="cart-empty">Your cart is empty.<br><a href="shop.html" style="font-weight:700">Shop the range →</a></p>';
    cart.forEach(function (it, i) {
      var row = document.createElement('div'); row.className = 'ci';
      row.innerHTML = '<img alt="" src="' + it.img + '"><div><b></b><p class="small muted"></p><div class="qty"><button type="button" aria-label="Fewer">−</button><span></span><button type="button" aria-label="More">+</button><button class="rm" type="button">Remove</button></div></div><b class="pr"></b>';
      row.querySelector('div > b').textContent = it.name; row.querySelector('.small').textContent = it.size;
      row.querySelector('.qty span').textContent = it.qty; row.querySelector('.pr').textContent = money(it.qty * it.price);
      var bs = row.querySelectorAll('.qty button');
      bs[0].onclick = function () { it.qty = Math.max(1, it.qty - 1); save(); render(); };
      bs[1].onclick = function () { it.qty++; save(); render(); };
      bs[2].onclick = function () { cart.splice(i, 1); save(); render(); };
      box.appendChild(row);
    });
    $('[data-cart-sub]').textContent = money(sub);
    var left = FREE - sub, fill = $('[data-ship-fill]'), msg = $('[data-ship-msg]');
    fill.style.width = Math.min(100, sub / FREE * 100) + '%';
    msg.innerHTML = sub === 0 ? 'Free metro delivery on orders over <b>$' + FREE + '</b>.' : (left > 0 ? 'You\'re <b>' + money(left) + '</b> away from free metro delivery.' : '<b>Free metro delivery unlocked.</b>');
  }
  var toastT;
  function toast(t) { var el = $('[data-toast]'); if (!el) return; el.textContent = t; el.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function () { el.classList.remove('on'); }, 2200); }
  function add(item) {
    var ex = cart.filter(function (i) { return i.id === item.id && i.size === item.size; })[0];
    if (ex) ex.qty++; else cart.push({ id: item.id, name: item.name, size: item.size, price: +item.price, img: item.img, qty: 1 });
    save(); render(); open();
  }
  var co = $('[data-checkout]'); if (co) co.addEventListener('click', function () { $('[data-checkout-msg]').textContent = 'Preview only. On the live site this goes to Shopify checkout.'; });
  // Buy boxes
  $$('[data-buy]').forEach(function (bx) {
    var szs = $$('.sz', bx), bp = $('[data-bp]', bx), bpd = $('[data-bpd]', bx);
    szs.forEach(function (s) {
      s.addEventListener('click', function () {
        szs.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); s.setAttribute('aria-pressed', 'true');
        bp.textContent = money(+s.getAttribute('data-price')); bpd.textContent = '$' + s.getAttribute('data-pd');
      });
    });
    $('[data-add]', bx).addEventListener('click', function () {
      var s = szs.filter(function (x) { return x.getAttribute('aria-pressed') === 'true'; })[0] || szs[0];
      add({ id: bx.getAttribute('data-id'), name: bx.getAttribute('data-name'), img: bx.getAttribute('data-img'), size: s.getAttribute('data-size'), price: s.getAttribute('data-price') });
    });
  });
  $$('[data-quick-add]').forEach(function (b) {
    b.addEventListener('click', function () { add({ id: b.getAttribute('data-id'), name: b.getAttribute('data-name'), img: b.getAttribute('data-img'), size: b.getAttribute('data-size'), price: b.getAttribute('data-price') }); });
  });
  // Product page
  var atc = $('[data-atc]');
  function pdpAdd() {
    var s = $('.size[aria-pressed="true"]'); if (!s) return;
    var sub = $('.opt[data-mode="sub"][aria-pressed="true"]');
    add({ id: atc.getAttribute('data-id'), name: atc.getAttribute('data-name'), img: atc.getAttribute('data-img'), size: s.getAttribute('data-size') + (sub ? ' · subscription' : ''), price: s.getAttribute('data-p') });
  }
  if (atc) {
    atc.addEventListener('click', pdpAdd);
    var sa = $('[data-sticky-atc]'), saBtn = $('[data-sa-add]'); if (sa) sa.hidden = false;
    if (saBtn) saBtn.addEventListener('click', pdpAdd);
    if (sa && 'IntersectionObserver' in window) new IntersectionObserver(function (es) { sa.classList.toggle('on', !es[0].isIntersecting && es[0].boundingClientRect.top < 0); }).observe(atc);
  }
  // Feeding guide add
  var ca = $('[data-calc-add]'), calcEl = $('[data-calc]');
  if (ca && calcEl) ca.addEventListener('click', function () {
    var f = calcEl._food || { name: 'Ocean Fish', url: 'ocean-fish.html', price: 160 };
    var img = { 'turkey-grain-free.html': 'performa_GFturkey_lamb-cut.webp', 'ocean-fish.html': 'performa_GF_ocean-fish-cut.webp', 'puppy-lamb-and-fish.html': '01_Performadog_Puppy-Single-cut.webp' }[f.url];
    add({ id: f.url.replace('.html', ''), name: f.name, img: 'assets/img/product/' + img, size: '15 kg', price: f.price });
  });
  render();
  // Steel sheen that travels with scroll (and with the pointer on tiles)
  var steel = $$('.steelfx');
  if (steel.length && !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var ticking = false;
    function upd() {
      ticking = false; var vh = innerHeight;
      steel.forEach(function (el) {
        if (el._hover) return;
        if (el.classList.contains('hdr')) { el.style.setProperty('--sx', (50 + Math.sin(scrollY / 900) * 50).toFixed(2) + '%'); return; }
        var r = el.getBoundingClientRect(); if (r.bottom < -50 || r.top > vh + 50) return;
        var p = (vh - r.top) / (vh + r.height);
        el.style.setProperty('--sx', (100 - p * 100).toFixed(2) + '%');
      });
    }
    addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    addEventListener('resize', upd); upd();
    $$('.pack.steelfx,.pimg.steelfx,.pdp-media.steelfx').forEach(function (el) {
      el.addEventListener('pointermove', function (e) { var r = el.getBoundingClientRect(); el._hover = true; el.style.setProperty('--sx', (100 - (e.clientX - r.left) / r.width * 100).toFixed(1) + '%'); });
      el.addEventListener('pointerleave', function () { el._hover = false; upd(); });
    });
  }
})();

/* v2.2: USP rotator (phones), interactive timeline, shop filter from URL */
(function () {
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  $$('[data-usp]').forEach(function (ul) {
    var li = $$('li', ul), i = 0; if (li.length < 2) return;
    
  });
  $$('[data-tline]').forEach(function (tl) {
    var ys = $$('.tl-y', tl), ps = $$('.tl-p', tl), fill = tl.querySelector('[data-tl-fill]'), cur = 0;
    function go(n) {
      cur = (n + ys.length) % ys.length;
      ys.forEach(function (b, k) { b.setAttribute('aria-selected', k === cur ? 'true' : 'false'); b.tabIndex = k === cur ? 0 : -1; });
      ps.forEach(function (p, k) { p.hidden = k !== cur; });
      fill.style.width = (ys.length > 1 ? cur / (ys.length - 1) * 100 : 100) + '%';
      var b = ys[cur], row = b.parentNode; row.scrollTo({ left: b.offsetLeft - row.clientWidth / 2 + b.clientWidth / 2, behavior: 'smooth' });
    }
    ys.forEach(function (b, k) { b.addEventListener('click', function () { go(k); }); });
    tl.querySelector('[data-tl-prev]').addEventListener('click', function () { go(cur - 1); });
    tl.querySelector('[data-tl-next]').addEventListener('click', function () { go(cur + 1); });
    tl.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(cur + 1); if (e.key === 'ArrowLeft') go(cur - 1); });
    go(0);
  });
  var h = location.hash.replace('#', '');
  var map = { cats: 'cat', working: 'working', puppy: 'puppy', sensitive: 'sensitive', supplements: 'supplement' };
  if (map[h]) { var chip = document.querySelector('[data-filter="' + map[h] + '"]'); if (chip) chip.click(); }
})();
