/* ==========================================================================
   PERFORMADOG — concept theme logic
   Real catalogue + pricing mirrored from the live WooCommerce store.
   ========================================================================== */
(function () {
'use strict';

/* ─────────────── catalogue ─────────────── */
var IMG = 'assets/img/';

var PRODUCTS = [
  {
    id:'pd-puppy', cat:'dog', kind:'Dog · Puppy',
    name:'Performadog Puppy Lamb &amp; Fish',
    img:IMG+'01_Performadog_Puppy-Single.jpg',
    desc:'Australian grass-fed lamb with wild-caught ocean tuna. Nutrient ratios tuned for brain, bone and muscle development to maturity.',
    chips:['Lamb','Wild tuna','Beta glucans','Gluten free'],
    sizes:[{kg:2.5,price:48},{kg:9,price:125},{kg:15,price:168}],
    flag:'Puppy formula', flagClass:''
  },
  {
    id:'pd-ocean', cat:'dog', kind:'Dog · All life stages',
    name:'Performadog Ocean Fish',
    img:IMG+'performa_GF_ocean-fish.jpg',
    desc:'Hypoallergenic and nutritionally dense. The formula we reach for with sensitivities, itchy skin and dull coats — balanced herbs plus yeast extract for the microbiome.',
    chips:['Wild tuna','Grass-fed lamb','Omega rich','Hypoallergenic'],
    sizes:[{kg:2.5,price:48},{kg:9,price:120},{kg:15,price:160}],
    flag:'Best seller', flagClass:'flame'
  },
  {
    id:'pd-turkey', cat:'dog', kind:'Dog · High performance',
    name:'Performadog Grain Free Turkey &amp; Lamb',
    img:IMG+'performa_GFturkey_lamb.jpg',
    desc:'Concentrated and grain free. Built for canine athletes, heavy workloads and dogs recuperating — the food behind breeding, competition, police and military dogs.',
    chips:['Turkey','Grain free','32% protein','High digestibility'],
    sizes:[{kg:2.5,price:48},{kg:9,price:125},{kg:15,price:168}],
    flag:'Grain free', flagClass:''
  },
  {
    id:'ip-roo', cat:'cat', kind:'Cat · All ages',
    name:'iPurr Kangaroo &amp; Lamb',
    img:IMG+'iPurr_GFOKangaroo.jpg',
    desc:'Wild kangaroo with grass-fed lamb. Low magnesium and high sulphur amino acids promote a healthy urinary tract and optimum urine pH — especially effective for older felines.',
    chips:['Wild kangaroo','Poultry free','Urinary pH','Microbiome'],
    sizes:[{kg:2.5,price:48}],
    flag:'Poultry free', flagClass:''
  },
  {
    id:'ip-ocean', cat:'cat', kind:'Cat · All ages',
    name:'iPurr Grain Free Ocean Fish',
    img:IMG+'iPurr_GFOceanFish.jpg',
    desc:'Freshly caught wild tuna with Australian lamb. A concentrated, highly digestible diet for cats with sensitive stomachs, allergies, or skin and coat issues.',
    chips:['Wild tuna','Grain free','Taurine','Omega 3'],
    sizes:[{kg:2.5,price:48}],
    flag:'Grain free', flagClass:''
  },
  {
    id:'pb', cat:'supp', kind:'Supplement · Dogs &amp; cats',
    name:'Purple Boost',
    img:IMG+'purple-boost-2.jpg',
    desc:'100% purple carrot powder blended with pre and probiotics. An immuno-stimulant with antioxidants, MOS and beta glucans — sprinkle over any meal.',
    chips:['28× anthocyanins','Probiotics','MOS','Beta glucans'],
    sizes:[{kg:0.18,price:43,label:'180 g',supp:1},{kg:1.08,price:190,label:'1.08 kg',supp:1}],
    flag:'Add-on', flagClass:'purple'
  }
];

var byId = {};
PRODUCTS.forEach(function (p) { byId[p.id] = p; });

/* ─────────────── breeds ───────────────
   w = typical adult weight (kg), lean = the concern this breed most often
   presents with, used when the owner picks "general thriving".            */
var BREEDS = [
  // dogs
  {n:'Australian Cattle Dog',s:'dog',w:20,lean:'work'},
  {n:'Australian Kelpie',s:'dog',w:17,lean:'work'},
  {n:'Australian Shepherd',s:'dog',w:24,lean:'work'},
  {n:'Australian Terrier',s:'dog',w:6,lean:'thrive'},
  {n:'Beagle',s:'dog',w:11,lean:'weight'},
  {n:'Bernese Mountain Dog',s:'dog',w:44,lean:'thrive'},
  {n:'Bichon Frise',s:'dog',w:6,lean:'skin'},
  {n:'Border Collie',s:'dog',w:19,lean:'work'},
  {n:'Borzoi',s:'dog',w:38,lean:'gut'},
  {n:'Boston Terrier',s:'dog',w:8,lean:'skin'},
  {n:'Boxer',s:'dog',w:29,lean:'gut'},
  {n:'British Bulldog',s:'dog',w:23,lean:'skin'},
  {n:'Bull Arab',s:'dog',w:36,lean:'work'},
  {n:'Bull Terrier',s:'dog',w:27,lean:'skin'},
  {n:'Cavalier King Charles Spaniel',s:'dog',w:7,lean:'thrive'},
  {n:'Chihuahua',s:'dog',w:3,lean:'thrive'},
  {n:'Cocker Spaniel',s:'dog',w:13,lean:'skin'},
  {n:'Collie (Rough)',s:'dog',w:25,lean:'skin'},
  {n:'Dachshund',s:'dog',w:8,lean:'weight'},
  {n:'Dalmatian',s:'dog',w:27,lean:'skin'},
  {n:'Doberman',s:'dog',w:36,lean:'work'},
  {n:'Dogue de Bordeaux',s:'dog',w:48,lean:'gut'},
  {n:'English Springer Spaniel',s:'dog',w:20,lean:'skin'},
  {n:'French Bulldog',s:'dog',w:11,lean:'skin'},
  {n:'German Shepherd',s:'dog',w:34,lean:'gut'},
  {n:'German Shorthaired Pointer',s:'dog',w:28,lean:'work'},
  {n:'Golden Retriever',s:'dog',w:31,lean:'skin'},
  {n:'Great Dane',s:'dog',w:60,lean:'gut'},
  {n:'Greyhound',s:'dog',w:30,lean:'gut'},
  {n:'Groodle / Goldendoodle',s:'dog',w:24,lean:'skin'},
  {n:'Havanese',s:'dog',w:5,lean:'skin'},
  {n:'Hungarian Vizsla',s:'dog',w:25,lean:'work'},
  {n:'Irish Setter',s:'dog',w:29,lean:'gut'},
  {n:'Jack Russell Terrier',s:'dog',w:7,lean:'work'},
  {n:'Japanese Spitz',s:'dog',w:8,lean:'skin'},
  {n:'Kelpie x Border Collie',s:'dog',w:18,lean:'work'},
  {n:'Labradoodle',s:'dog',w:23,lean:'skin'},
  {n:'Labrador Retriever',s:'dog',w:32,lean:'weight'},
  {n:'Lagotto Romagnolo',s:'dog',w:14,lean:'skin'},
  {n:'Maltese',s:'dog',w:4,lean:'skin'},
  {n:'Maremma Sheepdog',s:'dog',w:38,lean:'thrive'},
  {n:'Mastiff',s:'dog',w:68,lean:'gut'},
  {n:'Miniature Fox Terrier',s:'dog',w:5,lean:'skin'},
  {n:'Miniature Schnauzer',s:'dog',w:7,lean:'skin'},
  {n:'Newfoundland',s:'dog',w:60,lean:'thrive'},
  {n:'Papillon',s:'dog',w:4,lean:'thrive'},
  {n:'Pomeranian',s:'dog',w:3,lean:'skin'},
  {n:'Poodle (Standard)',s:'dog',w:24,lean:'skin'},
  {n:'Poodle (Toy / Mini)',s:'dog',w:6,lean:'skin'},
  {n:'Pug',s:'dog',w:8,lean:'weight'},
  {n:'Rhodesian Ridgeback',s:'dog',w:37,lean:'work'},
  {n:'Rottweiler',s:'dog',w:48,lean:'work'},
  {n:'Samoyed',s:'dog',w:23,lean:'skin'},
  {n:'Schnauzer (Giant)',s:'dog',w:40,lean:'work'},
  {n:'Shar Pei',s:'dog',w:22,lean:'skin'},
  {n:'Shetland Sheepdog',s:'dog',w:9,lean:'thrive'},
  {n:'Shih Tzu',s:'dog',w:6,lean:'skin'},
  {n:'Siberian Husky',s:'dog',w:23,lean:'gut'},
  {n:'Spoodle / Cockapoo',s:'dog',w:11,lean:'skin'},
  {n:'Staffordshire Bull Terrier',s:'dog',w:15,lean:'skin'},
  {n:'American Staffordshire Terrier',s:'dog',w:27,lean:'skin'},
  {n:'Weimaraner',s:'dog',w:32,lean:'gut'},
  {n:'Welsh Corgi',s:'dog',w:12,lean:'weight'},
  {n:'West Highland White Terrier',s:'dog',w:8,lean:'skin'},
  {n:'Whippet',s:'dog',w:13,lean:'gut'},
  {n:'Belgian Malinois',s:'dog',w:29,lean:'work'},
  {n:'Bloodhound',s:'dog',w:45,lean:'gut'},
  {n:'Cane Corso',s:'dog',w:47,lean:'work'},
  {n:'Cross breed / not listed',s:'dog',w:20,lean:'thrive'},
  // cats
  {n:'Domestic Short Hair',s:'cat',w:4.5,lean:'thrive'},
  {n:'Domestic Long Hair',s:'cat',w:5,lean:'skin'},
  {n:'Abyssinian',s:'cat',w:4,lean:'thrive'},
  {n:'Bengal',s:'cat',w:5.5,lean:'gut'},
  {n:'British Shorthair',s:'cat',w:6,lean:'weight'},
  {n:'Burmese',s:'cat',w:4.5,lean:'gut'},
  {n:'Devon Rex',s:'cat',w:3.5,lean:'skin'},
  {n:'Cornish Rex',s:'cat',w:3.5,lean:'skin'},
  {n:'Maine Coon',s:'cat',w:7.5,lean:'thrive'},
  {n:'Oriental Shorthair',s:'cat',w:4,lean:'gut'},
  {n:'Persian',s:'cat',w:4.5,lean:'skin'},
  {n:'Ragdoll',s:'cat',w:6.5,lean:'weight'},
  {n:'Russian Blue',s:'cat',w:4.5,lean:'thrive'},
  {n:'Scottish Fold',s:'cat',w:4.5,lean:'thrive'},
  {n:'Siamese',s:'cat',w:4,lean:'gut'},
  {n:'Siberian',s:'cat',w:6.5,lean:'skin'},
  {n:'Sphynx',s:'cat',w:4,lean:'skin'},
  {n:'Cross breed / not listed',s:'cat',w:4.5,lean:'thrive'}
];

/* ─────────────── feeding maths ───────────────
   Anchored to the feeding-rate table printed on the bag.             */
var DOG_CURVE = [[2,45],[7.5,95],[15,125],[25,160],[35,200],[45,250],[60,310],[70,350]];
var CAT_CURVE = [[2,35],[4,55],[6,72],[8,90],[10,105]];

function interp(curve, kg) {
  if (kg <= curve[0][0]) return curve[0][1] * (kg / curve[0][0]);
  for (var i = 1; i < curve.length; i++) {
    if (kg <= curve[i][0]) {
      var a = curve[i - 1], b = curve[i];
      var t = (kg - a[0]) / (b[0] - a[0]);
      return a[1] + t * (b[1] - a[1]);
    }
  }
  return curve[curve.length - 1][1];
}

function gramsPerDay(species, kg, stage, goal) {
  var g = interp(species === 'cat' ? CAT_CURVE : DOG_CURVE, kg);
  if (stage === 'puppy')  g *= 1.55;
  if (stage === 'senior') g *= 0.90;
  if (goal === 'work')    g *= 1.15;
  if (goal === 'weight')  g *= 0.85;
  return Math.round(g / 5) * 5;
}

/* ─────────────── recommendation ─────────────── */
var WHY = {
  skin:'Hypoallergenic, omega-rich and built around skin and coat — this is the formula owners switch to when the scratching will not stop.',
  gut:'Grain free with very high digestibility and yeast extracts for microbiome support. Firmer, smaller stools within the first fortnight is the usual report.',
  work:'A concentrated, nutritionally dense diet for canine athletes and heavy workloads — the same food behind breeding, competition, police and military dogs.',
  weight:'Nutritionally dense, so a smaller portion satisfies. Owners consistently report feeding less by weight than their previous brand.',
  thrive:'A scientifically balanced, holistic diet with a balanced supply of herbs plus yeast extract for optimal intestinal microbiome support.',
  puppy:'Nutrient ratios tuned for brain, bone and muscle development — designed to be the sole food from weaning through to maturity.',
  senior:'Low magnesium with high sulphur amino acids for a healthy urinary tract and optimum urine pH — especially effective for older felines.'
};

function recommend(species, stage, goal) {
  if (species === 'cat') {
    if (goal === 'skin' || goal === 'gut') return { id:'ip-ocean', why:WHY[goal] };
    if (stage === 'senior' || goal === 'weight') return { id:'ip-roo', why:WHY.senior };
    return { id:'ip-roo', why:'Cats love the taste of wild kangaroo. Combined with grass-fed lamb it is a complete diet for cats of all ages, with a formulation built for urinary tract health.' };
  }
  if (stage === 'puppy') return { id:'pd-puppy', why:WHY.puppy };
  if (goal === 'gut' || goal === 'work') return { id:'pd-turkey', why:WHY[goal] };
  return { id:'pd-ocean', why:WHY[goal] || WHY.thrive };
}

/* ─────────────── helpers ─────────────── */
var $  = function (s, c) { return (c || document).querySelector(s); };
var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
var money = function (n) { return '$' + (n % 1 === 0 ? n : n.toFixed(2)); };
var sizeLabel = function (s) { return s.label || (s.kg + ' kg'); };

/* ─────────────── product grid ─────────────── */
function renderGrid() {
  $('#grid').innerHTML = PRODUCTS.map(function (p) {
    var sizes = p.sizes.map(function (s, i) {
      return '<button class="sz' + (i === p.sizes.length - 1 ? ' on' : '') +
             '" data-p="' + p.id + '" data-i="' + i + '">' + sizeLabel(s) + '</button>';
    }).join('');
    var last = p.sizes[p.sizes.length - 1];
    return '' +
    '<article class="card rv" data-cat="' + p.cat + '">' +
      '<div class="card-media">' +
        '<span class="flag mono ' + p.flagClass + '">' + p.flag + '</span>' +
        '<img src="' + p.img + '" alt="' + p.name.replace(/&amp;/g, '&') + '">' +
      '</div>' +
      '<div class="card-body">' +
        '<span class="mono card-for">' + p.kind + '</span>' +
        '<h3>' + p.name + '</h3>' +
        '<p class="card-desc">' + p.desc + '</p>' +
        '<div class="chips">' + p.chips.map(function (c) { return '<span class="chip">' + c + '</span>'; }).join('') + '</div>' +
        '<div class="card-sizes">' + sizes + '</div>' +
        '<div class="card-foot">' +
          '<div class="price"><b id="pr-' + p.id + '">' + money(last.price) + '</b>' +
            '<span class="per" id="pk-' + p.id + '">' + perKg(last) + '</span></div>' +
          '<button class="btn btn-primary btn-sm" data-add="' + p.id + '">Add</button>' +
        '</div>' +
      '</div>' +
    '</article>';
  }).join('');
}
function perKg(s) {
  if (s.supp) return 'per tub';
  return s.kg >= 1 ? money(Math.round(s.price / s.kg * 100) / 100) + '/kg' : 'per tub';
}

/* size switch on cards */
document.addEventListener('click', function (e) {
  var sz = e.target.closest('.sz');
  if (sz) {
    var p = byId[sz.dataset.p], s = p.sizes[+sz.dataset.i];
    $$('.sz[data-p="' + p.id + '"]').forEach(function (b) { b.classList.toggle('on', b === sz); });
    $('#pr-' + p.id).textContent = money(s.price);
    $('#pk-' + p.id).textContent = perKg(s);
    return;
  }
  var add = e.target.closest('[data-add]');
  if (add) {
    var prod = byId[add.dataset.add];
    var on = $('.sz[data-p="' + prod.id + '"].on');
    addToCart(prod, prod.sizes[on ? +on.dataset.i : prod.sizes.length - 1]);
  }
});

/* filters */
$('#filters').addEventListener('click', function (e) {
  var b = e.target.closest('button'); if (!b) return;
  $$('#filters button').forEach(function (x) { x.classList.toggle('on', x === b); });
  var f = b.dataset.f;
  $$('#grid .card').forEach(function (c) {
    c.classList.toggle('hide', f !== 'all' && c.dataset.cat !== f);
  });
});

/* ─────────────── cart ─────────────── */
var cart = 0;
function addToCart(p, size) {
  cart++;
  var dot = $('#cartDot');
  dot.textContent = cart;
  dot.classList.add('on');
  dot.animate(
    [{ transform:'scale(1)' }, { transform:'scale(1.55)' }, { transform:'scale(1)' }],
    { duration:420, easing:'cubic-bezier(.22,.61,.36,1)' }
  );
  $('#toastName').innerHTML = p.name + ' — ' + sizeLabel(size);
  $('#toastSub').textContent = money(size.price) + ' · free delivery applied';
  var t = $('#toast');
  t.classList.add('on');
  clearTimeout(addToCart._t);
  addToCart._t = setTimeout(function () { t.classList.remove('on'); }, 3600);
}

/* ─────────────── finder ─────────────── */
var state = { species:'dog', breed:null, kg:30, stage:'adult', goal:'thrive', sizeIx:null };

function segBind(sel, key, after) {
  $(sel).addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    $$(sel + ' button').forEach(function (x) { x.classList.toggle('on', x === b); });
    state[key] = b.dataset[key] || b.dataset.species || b.dataset.stage || b.dataset.goal;
    state.sizeIx = null;
    if (after) after();
    update();
  });
}
segBind('#segSpecies', 'species', function () {
  state.breed = null;
  $('#breedInput').value = '';
  $('#breedInput').placeholder = state.species === 'cat'
    ? 'Start typing — e.g. Domestic Short Hair'
    : 'Start typing — e.g. German Shepherd';
  state.kg = state.species === 'cat' ? 4.5 : 30;
  var r = $('#wt');
  r.min = state.species === 'cat' ? 2 : 2;
  r.max = state.species === 'cat' ? 12 : 60;
  r.step = state.species === 'cat' ? 0.5 : 1;
  r.value = state.kg;
  $('#wtVal').textContent = state.kg;
});
segBind('#segStage', 'stage');
segBind('#segGoal',  'goal');

/* breed autocomplete */
var input = $('#breedInput'), sugg = $('#sugg'), cursor = -1, list = [];

function openSugg(q) {
  q = (q || '').toLowerCase().trim();
  list = BREEDS.filter(function (b) {
    return b.s === state.species && (!q || b.n.toLowerCase().indexOf(q) > -1);
  }).slice(0, 40);
  cursor = -1;
  if (!list.length) {
    sugg.innerHTML = '<div class="empty">No match — drag the weight slider and we will still find the right food.</div>';
  } else {
    sugg.innerHTML = list.map(function (b, i) {
      return '<button data-i="' + i + '"><span>' + b.n + '</span><span class="mono">' + b.w + ' kg</span></button>';
    }).join('');
  }
  sugg.classList.add('on');
}
function pick(b) {
  state.breed = b;
  state.kg = b.w;
  state.sizeIx = null;
  input.value = b.n;
  $('#wt').value = b.w;
  $('#wtVal').textContent = b.w;
  sugg.classList.remove('on');
  update();
}

input.addEventListener('focus', function () { openSugg(input.value); });
input.addEventListener('input', function () { openSugg(input.value); });
input.addEventListener('keydown', function (e) {
  if (!sugg.classList.contains('on') || !list.length) return;
  var btns = $$('#sugg button');
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    cursor += (e.key === 'ArrowDown' ? 1 : -1);
    if (cursor < 0) cursor = btns.length - 1;
    if (cursor >= btns.length) cursor = 0;
    btns.forEach(function (b, i) { b.classList.toggle('cursor', i === cursor); });
    btns[cursor].scrollIntoView({ block:'nearest' });
  } else if (e.key === 'Enter') {
    e.preventDefault();
    pick(list[cursor < 0 ? 0 : cursor]);
  } else if (e.key === 'Escape') {
    sugg.classList.remove('on');
  }
});
sugg.addEventListener('mousedown', function (e) {
  var b = e.target.closest('button[data-i]'); if (!b) return;
  e.preventDefault();
  pick(list[+b.dataset.i]);
});
document.addEventListener('click', function (e) {
  if (!e.target.closest('.pick')) sugg.classList.remove('on');
});

$('#wt').addEventListener('input', function () {
  state.kg = +this.value;
  $('#wtVal').textContent = state.kg;
  state.sizeIx = null;
  update();
});

/* the actual match */
function update() {
  $('#wtLabel').textContent = state.stage === 'puppy' ? 'Expected adult weight' : 'Adult weight';
  $$('#steps .step-pip')[0].classList.toggle('done', !!state.breed);
  $$('#steps .step-pip')[1].classList.toggle('done', !!state.breed);
  $$('#steps .step-pip')[2].classList.toggle('done', !!state.breed);

  if (!state.breed) {
    $('#out').classList.remove('on');
    $('#outEmpty').style.display = '';
    return;
  }
  $('#outEmpty').style.display = 'none';
  $('#out').classList.add('on');

  var goal = state.goal === 'thrive' ? state.breed.lean : state.goal;
  var rec = recommend(state.species, state.stage, goal);
  var p = byId[rec.id];

  var g = gramsPerDay(state.species, state.kg, state.stage, goal);
  if (state.sizeIx === null) state.sizeIx = p.sizes.length - 1;
  if (state.sizeIx >= p.sizes.length) state.sizeIx = p.sizes.length - 1;
  var size = p.sizes[state.sizeIx];

  var days = Math.round(size.kg * 1000 / g);
  var perDay = size.price / days;

  $('#outTag').textContent = state.breed.n + ' · ' + state.stage;
  $('#outImg').src = p.img;
  $('#outName').innerHTML = p.name;
  $('#outWhy').textContent = rec.why;
  $('#statFeed').innerHTML = g + '<i>g</i>';
  $('#statLast').innerHTML = days + '<i> days</i>';
  $('#statCost').innerHTML = '$' + perDay.toFixed(2);

  $('#outSizes').innerHTML = p.sizes.map(function (s, i) {
    return '<button class="size-pill' + (i === state.sizeIx ? ' on' : '') + '" data-si="' + i + '">' +
      sizeLabel(s) + ' <span>' + money(s.price) + '</span></button>';
  }).join('');

  $('#outPrice').textContent = money(size.price);
  $('#outAdd').onclick = function () { addToCart(p, size); };
}

$('#outSizes').addEventListener('click', function (e) {
  var b = e.target.closest('[data-si]'); if (!b) return;
  state.sizeIx = +b.dataset.si;
  update();
});

/* ─────────────── static content ─────────────── */
var EXCLUSIONS = ['No gluten','No dairy','No soy','No fillers','No artificial flavours',
  'No artificial colours','No added preservatives','GMO free','Irradiation free',
  'Fumigation free','No meat meal mystery','Hypoallergenic options'];

function renderExcl() {
  $('#excl').innerHTML = EXCLUSIONS.map(function (x) {
    return '<div class="excl-item">' +
      '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">' +
      '<circle cx="12" cy="12" r="9"/><path d="m8.5 15.5 7-7"/></svg><span>' + x + '</span></div>';
  }).join('');
}

var REVIEWS = [
  { t:'Never going back!', i:'AJ', n:'Abigail Jones-Walker', m:'Yellow Labrador · Ocean Fish',
    q:'I was hesitant to switch because she had such a sensitive stomach. But since starting Nala on the Ocean Fish around two years ago she has been so healthy and full of energy — healthy weight, runs 5–7 km with me, great digestion, and her coat is shiny and thick.' },
  { t:'Hands down the best', i:'BT', n:'Brett Talty', m:'NSW · 4 dogs · 7 years on Performadog',
    q:'I have done extensive research into a lot of different foods and Performadog comes out on top by a very long way. Everyone who knows my dogs cannot believe how healthy and shiny their coats look. Been using this food for over 7 years and there is just no other option for us.' },
  { t:'A whole industry standard', i:'CC', n:'Troy Seraceno · Core Canine', m:'Board &amp; train · 5–10 dogs weekly',
    q:'What a difference in every dog’s performance and functionality. The coats are now shining, dogs that had skin allergies were starting to clear. Many are meeting our goals and standards a lot quicker.' },
  { t:'First year without an injection', i:'DR', n:'Drew Romeo', m:'Perth WA · Ocean Fish',
    q:'My dog’s first year without an injection for itching. After trying reputable high-end brands, grain-free, sensitive skin — nothing fit. Now he has a diet full of clean ingredients and I have never seen his fur shine like this.' },
  { t:'Simply the best', i:'MK', n:'Dr Michael Kern', m:'Dobermann · Working title champion',
    q:'My Dobermann Caesar has been thriving — healthy, energetic, powerful and his coat is glowing. We recently accomplished the highest working dog title in competition and Performadog has been an essential part of our success.' },
  { t:'I tried every cat food', i:'VM', n:'Victoria Mariettakis', m:'Devon Rex · iPurr Kangaroo',
    q:'I own a Devon Rex who is allergic to chicken, so finding a cat food with the right proteins without poultry meal was becoming impossible. My girl is back at a healthy weight, her fur is even softer and she absolutely gobbles this up.' }
];

function renderReviews() {
  var star = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 3 6.6 7 .8-5.2 4.8 1.4 7L12 17.8 5.8 21.2l1.4-7L2 9.4l7-.8L12 2Z"/></svg>';
  $('#revGrid').innerHTML = REVIEWS.map(function (r) {
    return '<article class="rev rv">' +
      '<div class="stars">' + star.repeat(5) + '</div>' +
      '<h4>' + r.t + '</h4><p>' + r.q + '</p>' +
      '<div class="rev-who"><div class="av">' + r.i + '</div>' +
        '<div><b>' + r.n + '</b><span class="mono">' + r.m + '</span></div></div>' +
    '</article>';
  }).join('');
}

var FAQS = [
  { q:'How should I transition my dog onto Performadog?',
    a:'Move across over 7–10 days, replacing roughly a quarter of the old food every couple of days. Because the food is nutritionally dense you will generally feed less by weight than your previous brand, so start at the lower end of the feeding rate and adjust to condition. If you would like a transition plan for a specific issue, call us — we build them daily.' },
  { q:'How long will delivery take?',
    a:'We ship within 24 hours of your order being processed. Most addresses receive their food in 2–5 working days; allow 5–7 if you are remote. You will get tracking by email, plus SMS the day before and the morning of delivery so you can nominate a safe-drop location.' },
  { q:'What is the guarantee, exactly?',
    a:'A full palatability guarantee on every bag. If your dog will not eat it, return the uneaten portion in the original bag — provided it is at least 80% full — with a copy of your invoice, and we refund the purchase price in full.' },
  { q:'Why do you not sell treats?',
    a:'Because a complete diet does the work. Every formula is AAFCO-complete and balanced for everyday feeding, so there is no need to supplement with a multivitamin or anything else — it is already in the bag.' },
  { q:'Can I feed the same food to my puppy and my adult dog?',
    a:'The puppy formula is designed as the sole food from weaning through to maturity. Ocean Fish and Grain Free Turkey are balanced for all life stages, which is why many multi-dog households run a single bag across the whole pack.' },
  { q:'Is Purple Boost necessary if I am already feeding Performadog?',
    a:'No — the food is complete on its own. Purple Boost is an immuno-stimulant add-on for owners who want additional antioxidant and microbiome support, and it is the one we reach for with dogs under stress, in recovery, or carrying extra weight.' },
  { q:'Do you ship to PO boxes or internationally?',
    a:'Food cannot be delivered to a PO box — we need a street address. We ship Australia-wide only. If you would like to discuss distribution outside Australia, email sales@performadog.com.au.' },
  { q:'Are the prices on the site GST inclusive?',
    a:'Yes. Every price displayed includes GST, and delivery is free on every order.' }
];

function renderFaq() {
  $('#acc').innerHTML = FAQS.map(function (f) {
    return '<div class="acc-item"><button class="acc-q">' + f.q +
      '<span class="acc-ic"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg></span></button>' +
      '<div class="acc-a"><p>' + f.a + '</p></div></div>';
  }).join('');

  $('#acc').addEventListener('click', function (e) {
    var q = e.target.closest('.acc-q'); if (!q) return;
    var item = q.parentElement, body = $('.acc-a', item), open = item.classList.contains('on');
    $$('#acc .acc-item').forEach(function (i) {
      i.classList.remove('on');
      $('.acc-a', i).style.maxHeight = null;
    });
    if (!open) {
      item.classList.add('on');
      body.style.maxHeight = body.scrollHeight + 'px';
    }
  });
}

/* ─────────────── chrome ─────────────── */
function announce() {
  var items = $$('#announce .announce-item'), i = 0;
  setInterval(function () {
    items[i].classList.remove('on');
    i = (i + 1) % items.length;
    items[i].classList.add('on');
  }, 4200);
}

function header() {
  var h = $('#hdr'), hero = $('.hero');
  /* stay transparent glass while it sits over the dark hero; only frost up once
     real content is passing underneath */
  var onScroll = function () {
    var trigger = hero ? hero.offsetHeight - h.offsetHeight - 38 : 12;
    h.classList.toggle('stuck', window.scrollY > trigger);
  };
  window.addEventListener('scroll', onScroll, { passive:true });
  window.addEventListener('resize', onScroll);
  onScroll();
}

/* mega menu: hover is CSS, this adds click/keyboard and touch */
function mega() {
  var groups = $$('#nav > div');
  groups.forEach(function (g) {
    var btn = $('.navlink', g);
    if (!btn) return;
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = g.classList.contains('open');
      groups.forEach(function (x) {
        x.classList.remove('open');
        var b = $('.navlink', x); if (b) b.setAttribute('aria-expanded', 'false');
      });
      if (!open) { g.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('#nav')) {
      groups.forEach(function (x) {
        x.classList.remove('open');
        var b = $('.navlink', x); if (b) b.setAttribute('aria-expanded', 'false');
      });
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    groups.forEach(function (x) {
      x.classList.remove('open');
      var b = $('.navlink', x); if (b) b.setAttribute('aria-expanded', 'false');
    });
  });
}

function reveal() {
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { threshold:0.08, rootMargin:'0px 0px -40px 0px' });

  $$('.rv').forEach(function (el, i) {
    el.style.transitionDelay = (Math.min(i % 4, 3) * 70) + 'ms';
    io.observe(el);
  });

  /* never leave content hidden if IO is starved (background tab, hidden pane) */
  setTimeout(function () { $$('.rv').forEach(function (el) { el.classList.add('in'); }); }, 2600);
}

function smooth() {
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]'); if (!a) return;
    var id = a.getAttribute('href');
    if (id === '#') return;
    var t = document.querySelector(id); if (!t) return;
    e.preventDefault();
    window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - 104, behavior:'smooth' });
  });
}

/* ─────────────── boot ─────────────── */
/* start the matcher on Australia's most common dog so the panel is never dead */
(function seed() {
  var b = BREEDS.filter(function (x) { return x.n === 'Labrador Retriever'; })[0];
  if (!b) return;
  state.breed = b; state.kg = b.w;
  document.querySelector('#breedInput').value = b.n;
  var r = document.querySelector('#wt'); r.value = b.w;
  document.querySelector('#wtVal').textContent = b.w;
})();

renderGrid();
renderExcl();
renderReviews();
renderFaq();
announce();
header();
mega();
smooth();
reveal();
update();

})();
