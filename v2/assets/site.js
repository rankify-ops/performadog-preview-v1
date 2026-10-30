/* Performadog v2 preview — small, dependency-free behaviours. */
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

  // Postcode demo (preview logic only — real zones live in Shopify)
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
        : '<strong>Regional area.</strong> We deliver here. A freight surcharge applies and is shown before you pay — no surprises at checkout. Usually 5–7 business days.';
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
    }
    sizes.forEach(function (b) { if (!b.disabled) b.addEventListener('click', function () { pick(b); }); });
    var opts = $$('.opt', pdp);
    opts.forEach(function (o) {
      o.addEventListener('click', function () {
        opts.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        o.setAttribute('aria-pressed', 'true');
        if (atc) atc.textContent = o.getAttribute('data-mode') === 'sub' ? 'Start my subscription' : 'Add to cart';
      });
    });
  }

  // Feeding calculator — anchored to the feeding table printed on the bag
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
    f.addEventListener('submit', function (e) { e.preventDefault(); var o = $('[data-form-out]', f); if (o) o.textContent = 'Preview only — on the live site this sends to the Performadog inbox.'; });
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
