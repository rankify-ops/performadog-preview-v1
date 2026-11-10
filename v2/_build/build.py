#!/usr/bin/env python3
"""Builds the Performadog v2 preview into ../ (static HTML for GitHub Pages).
Run:  python3 _build/build.py   (from v2/)"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import *  # noqa

OUT = os.environ.get('PD_OUT') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GLASS = os.path.exists(os.path.join(OUT, 'assets', 'glass.css'))
PV = 'v3' if GLASS else 'v2'
E = html.escape

# ---- image slots --------------------------------------------------------------
# slot -> {"src","alt","stock":bool} ; missing slot renders a "PHOTO NEEDED" panel.
import hashlib
VER = hashlib.md5((open(os.path.join(OUT, 'assets', 'site.css'), 'rb').read() + open(os.path.join(OUT, 'assets', 'site.js'), 'rb').read() + (open(os.path.join(OUT, 'assets', 'glass.css'), 'rb').read() if GLASS else b''))).hexdigest()[:8]
LIB, VIDEOS = [], []
IMG = json.load(open(os.path.join(os.path.dirname(__file__), 'images.json')))


def pic(slot, label, cls='ratio-43', extra='', eager=False):
    im = IMG.get(slot)
    if not im:
        return f'<div class="shot ph {cls}" {extra}><p class="mono">{E(label)}</p></div>'
    tag = '<span class="stock-tag">Stock, to replace</span>' if im.get('stock') else ''
    pos = f' style="object-position:{im["pos"]}"' if im.get('pos') else ''
    return (f'<div class="shot {cls}" {extra}>{tag}<img src="{im["src"]}" alt="{E(im["alt"])}" loading="{"eager" if eager else "lazy"}"{pos}></div>')


def tbc(text):
    return f'<span class="tbc" title="Needs Kris">{text}</span>'


def money(v):
    return f'${v:,.2f}'.replace('.00', '') if v == int(v) else f'${v:,.2f}'

# ---- layout -------------------------------------------------------------------
NAV = [('shop.html', 'Shop'), ('feeding-guide.html', 'Feeding guide'), ('science.html', 'The science'),
       ('library.html', 'Journal'), ('story.html', 'Our story'), ('reviews.html', 'Reviews')]
MENU_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'


CHEV = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LEARN_IC = {'science.html': '<path d="M9 3h6M10 3v6L4.5 18.5A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.5-2.5L14 9V3"/><path d="M7 15h10"/>',
            'case-study.html': '<path d="M3 12h4l3-8 4 16 3-8h4"/>', 'ingredients.html': '<path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19l7-7"/>',
            'library.html': '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M8 7h7"/>', 'story.html': '<path d="M3 11l9-7 9 7v9H3z"/><path d="M9 20v-6h6v6"/>',
            'reviews.html': '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>'}
LEARN = [('science.html', 'The science', 'Nutrient Ramping, gut health and how it is made'), ('case-study.html', 'Lab case study', 'One dog, two blood panels, twelve months apart'),
         ('ingredients.html', 'Ingredients', 'Every ingredient and nutrient, explained'), ('library.html', 'Journal', 'Handler interviews, Ask Bill and dog health'),
         ('story.html', 'Our story', 'Kris, Von Forell and 45 years of working dogs'), ('reviews.html', 'Reviews', f'{len(T)} handlers, breeders and owners')]


def mega_menus():
    prods = ''.join(f'''<a class="mm-prod" href="{p["slug"]}.html"><span class="mm-pimg tone"><img src="assets/img/product/{p["img"]}" alt="" loading="lazy"></span>
<span class="mm-ptxt"><span class="mm-tag">{E(p["job"])}</span><b>{E(p["name"])}</b><span class="mm-price">From {money(min(s[2] for s in p["sizes"] if s[2]))} · <em>{money(round(pday(p, default_size(p)[1], default_size(p)[2]), 2))}/day</em></span></span></a>''' for p in PRODUCTS[:4])
    needs = ''.join(f'<a href="{h}">{ic}<span>{t}</span></a>' for h, t, s, ic in NEEDS)
    learn = ''.join(f'<a class="mm-learn" href="{h}"><span class="mm-lic">{ico(LEARN_IC[h])}</span><b>{t}</b><span>{d}</span></a>' for h, t, d in LEARN)
    shop = f'''<div class="mm" id="mm-shop" data-mm hidden><div class="wrap mm-grid">
<div class="mm-col mm-needs"><p class="mm-h">Shop by need</p>{needs}<a class="mm-all" href="shop.html">Shop the full range →</a></div>
<div class="mm-col mm-prods"><p class="mm-h">Best sellers</p><div class="mm-pgrid">{prods}</div></div>
<a class="mm-feature tone" href="feeding-guide.html"><span class="mm-h">Not sure which?</span><b class="d">Build your dog's plan</b><span>Four questions. Which food, how much a day, and what it costs.</span><span class="btn btn-ember">Start · 1 min</span></a>
</div></div>'''
    lrn = f'''<div class="mm" id="mm-learn" data-mm hidden><div class="wrap mm-grid mm-grid-learn">
<div class="mm-lgrid">{learn}</div>
<a class="mm-feature mm-photo" href="case-study.html"><img src="assets/img/real/kris-heeling-dobermann.jpg" alt="" loading="lazy"><span class="mm-ov"><span class="mm-h">Proof, not promises</span><b class="d">Read the lab case study</b></span></a>
</div></div>'''
    return shop + lrn


def page(fname, title, desc, body, active=None):
    is_shop = active == 'shop.html'
    is_learn = active in ('science.html', 'library.html', 'story.html', 'reviews.html', 'ingredients.html')
    nav = (f'<button class="nav-t" type="button" aria-expanded="false" aria-controls="mm-shop" data-mm-t{" aria-current=\"page\"" if is_shop else ""}>Shop{CHEV}</button>'
           f'<button class="nav-t" type="button" aria-expanded="false" aria-controls="mm-learn" data-mm-t{" aria-current=\"page\"" if is_learn else ""}>Learn{CHEV}</button>'
           f'<a href="feeding-guide.html"{" aria-current=\"page\"" if active == "feeding-guide.html" else ""}>Feeding guide</a>'
           f'<a href="reviews.html">Reviews</a><a href="delivery.html">Delivery</a>')
    dprods = ''.join(f'<a class="dm-prod" href="{p["slug"]}.html"><span class="mm-pimg tone"><img src="assets/img/product/{p["img"]}" alt="" loading="lazy"></span><span><b>{E(p["name"])}</b><span class="small muted">From {money(min(s[2] for s in p["sizes"] if s[2]))}</span></span></a>' for p in PRODUCTS)
    dnav = (f'<details class="dm" open><summary>Shop</summary><div class="dm-body">{dprods}<a class="dm-link" href="shop.html">Shop the full range →</a></div></details>'
            f'<details class="dm"><summary>Learn</summary><div class="dm-body">' + ''.join(f'<a class="dm-link dm-lic" href="{h}">{ico(LEARN_IC[h])}{t}</a>' for h, t, d in LEARN) + '</div></details>'
            '<a class="dm-top" href="feeding-guide.html">Feeding guide</a><a class="dm-top" href="delivery.html">Delivery &amp; subscriptions</a><a class="dm-top" href="faq.html">FAQ</a><a class="dm-top" href="contact.html">Contact</a>')
    doc = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="assets/img/brand/logo-full.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Barlow+Condensed:wght@600;700;800;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css?v={VER}">{f'<link rel="stylesheet" href="assets/glass.css?v={VER}">' if GLASS else ''}
</head>
<body{' class="glass"' if GLASS else ''}>
<div class="ann"><span>Free metro delivery over ${FREE_SHIP}</span><span class="hide-s"> · Subscribe &amp; save on every bag · Dispatched within 24 hours</span></div>
<header class="hdr">
<div class="wrap">
<a class="logo" href="index.html" aria-label="Performadog home"><img src="assets/img/brand/logo-dark.png" alt="Performadog" width="630" height="125"></a>
<nav class="nav" aria-label="Main">{nav}</nav>
<div class="hdr-actions"><a class="btn btn-ember btn-shop" href="shop.html">Shop now</a>
<button class="cart-btn" type="button" data-cart-open aria-label="Open cart">{CART_SVG}<span class="cart-count" data-cart-count>0</span></button>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer">{MENU_SVG}<span class="hide-s">Menu</span></button></div>
</div>
{mega_menus()}
<div class="drawer" id="drawer"><nav aria-label="Mobile">{dnav}<a class="btn btn-ember btn-block" href="shop.html">Shop now</a></nav></div>
</header>
<main>
{body}
</main>
{footer()}
<div class="cart-scrim" data-cart-close hidden></div>
<aside class="cart" aria-label="Cart" aria-hidden="true" data-cart hidden>
<div class="cart-hd"><p class="d d-sm">Your cart</p><button class="cart-x" type="button" data-cart-close aria-label="Close cart">✕</button></div>
<div class="ship-bar"><p class="small" data-ship-msg></p><div class="track"><span data-ship-fill></span></div></div>
<div class="cart-items" data-cart-items></div>
<div class="cart-ft"><div class="row between" style="align-items:baseline"><span class="mono">Subtotal</span><span class="d d-sm" data-cart-sub>$0</span></div>
<p class="small muted">Subscribe at checkout and save on every bag. Regional freight shown before you pay.</p>
<button class="btn btn-ember btn-block" type="button" data-checkout>Checkout</button><p class="small muted center" data-checkout-msg></p>
<button class="btn btn-line btn-block" type="button" data-cart-close>Keep shopping</button></div></aside>
<script src="assets/site.js?v={VER}"></script>
</body>
</html>'''
    with open(os.path.join(OUT, fname), 'w') as f:
        for o, n in REMAP.items():
            doc = doc.replace(f'"{o}"', f'"{n}"').replace(f'"{o}#', f'"{n}#')
        f.write(doc.replace(' →', '&nbsp;→'))
    return fname


def footer():
    return f'''<footer class="ftr">
<div class="wrap pad-s">
<div class="cols">
<div class="col full"><img src="assets/img/brand/logo-lockup.png" alt="Performadog" style="height:40px;width:auto;margin-bottom:10px">
<p style="opacity:.85;max-width:30em">Performance nutrition built by a working-dog breeder. Formulated with animal nutritionist Bill Wiadrowski. Australian made and owned.</p>
<p class="mono" style="opacity:.85">{PHONE} · PO Box 372, Whittlesea VIC 3757</p></div>
<div class="col"><p class="mono" style="opacity:.7">Shop</p><a href="turkey-grain-free.html">Turkey Grain Free</a><a href="ocean-fish.html">Ocean Fish</a><a href="puppy-lamb-and-fish.html">Puppy Lamb &amp; Fish</a><a href="purple-boost.html">Purple Boost</a><a href="shop.html#cats">iPurr for cats</a><a href="where-to-buy.html">Where to buy</a></div>
<div class="col"><p class="mono" style="opacity:.7">Learn</p><a href="story.html">Our story</a><a href="science.html">The science</a><a href="case-study.html">Lab case study</a><a href="ingredients.html">Ingredients</a><a href="feeding-guide.html">Feeding guide</a><a href="reviews.html">Reviews</a></div>
<div class="col"><p class="mono" style="opacity:.7">Help</p><a href="delivery.html">Delivery &amp; freight</a><a href="delivery.html#subscribe">Subscribe &amp; save</a><a href="delivery.html#guarantee">Guarantee</a><a href="faq.html">FAQ</a><a href="contact.html">Contact</a></div>
</div>
<div class="base"><p class="mono" style="opacity:.7">© 2026 Forell Pty Ltd · ABN 14 128 573 693</p><p class="mono" style="opacity:.7">Preview build by Rankify</p></div>
</div>
</footer>'''


def rail_section(n, label, inner, theme='alt', node_top=80, sid=''):
    idattr = f' id="{sid}"' if sid else ''
    return f'''<section class="sec {theme}"{idattr}><div class="wrap"><div class="rail pad"><span class="node" style="top:{node_top}px"></span>
<p class="mono file steel">File {n:02d} · {label}</p>
{inner}
</div></div></section>'''


def plain_section(inner, theme='', cls='pad', sid=''):
    idattr = f' id="{sid}"' if sid else ''
    return f'<section class="sec {theme}"{idattr}><div class="wrap {cls}">{inner}</div></section>'


def page_head(eyebrow, title_lines, intro, theme='alt', aside=''):
    spans = ''.join(f'<span{" class=\"grad\"" if i == len(title_lines) - 1 and len(title_lines) > 1 else ""}>{t}</span>' for i, t in enumerate(title_lines))
    return f'''<section class="sec {theme}"><div class="wrap" style="padding-top:56px;padding-bottom:56px">
<p class="mono steel" style="margin-bottom:20px">{eyebrow}</p>
<div class="split split-wide" style="align-items:end"><h1 class="d d-lg" style="line-height:.9">{spans.replace('<span', '<span style="display:block"')}</h1>
<div class="stack"><p class="lead muted">{intro}</p>{aside}</div></div>
</div></section>'''


def cta_band(title='Feed your dog like a working dog.', sub=None):
    sub = sub or f'Free metro delivery over ${FREE_SHIP} · subscribe, skip or cancel anytime · palatability guarantee'
    return f'''<section class="cta-band tone"><div class="wrap pad"><div class="rail"><span class="node" style="top:6px"></span>
<p class="mono file">From $48 · 2.5 kg trial bag</p>
<h2 class="d d-lg">{title}</h2>
<div class="row mt" style="align-items:center"><a class="btn btn-ember" href="shop.html">{CART_SVG}Shop now</a><a class="btn btn-line" href="feeding-guide.html">Find my dog's food</a></div>
<p class="small mt-s" style="font-weight:600">{sub}</p>
</div></div></section>'''


STAR1 = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.6l2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 15l-5.2 2.8 1-5.9L1.5 7.8l5.9-.8z"/></svg>'


def stars(label=True):
    return f'<span class="stars" role="img" aria-label="5 out of 5 stars">{STAR1 * 5}</span>'



KERN_URL = 'library-with-dr-michael-kern.html'
IGP_FACTS = [('Tracking, obedience, protection', 'IGP is the international working dog sport, formerly IPO or Schutzhund. Every trial tests all three.'),
             ('Three levels. IGP 3 is the top.', 'Dogs work up through IGP 1 and IGP 2. IGP 3 is the highest standard title in the sport.'),
             ('Bred and backed by Kris', 'Caesar was bred at Von Forell, Kris\u2019s kennel. Dr Kern trained with Kris\u2019s system and mentoring, and feeds Performadog.')]



def igp_badge(cls='igp-badge'):
    # Original medal design (not an official IGP / FCI mark)
    teeth = ''.join(f'<polygon points="100,6 {100 + 9},{20} {100 - 9},{20}" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 15))
    return f'''<svg class="{cls}" viewBox="0 0 200 250" role="img" aria-label="IGP 3 title badge">
<defs><linearGradient id="igpg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7a823"/><stop offset=".55" stop-color="#ee7a1f"/><stop offset="1" stop-color="#d9302b"/></linearGradient>
<linearGradient id="igpr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b52f16"/><stop offset="1" stop-color="#7f1f0e"/></linearGradient>
<path id="igpt" d="M100,100 m-66,0 a66,66 0 1,1 132,0"/><path id="igpb" d="M100,100 m-74,0 a74,74 0 0,0 148,0"/></defs>
<path d="M62 150 L44 244 L72 228 L88 250 L100 168Z" fill="url(#igpr)"/><path d="M138 150 L156 244 L128 228 L112 250 L100 168Z" fill="url(#igpr)"/>
<g fill="url(#igpg)">{teeth}</g><circle cx="100" cy="100" r="86" fill="url(#igpg)"/>
<circle cx="100" cy="100" r="78" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="1.5"/>
<circle cx="100" cy="100" r="56" fill="#1a1714"/><circle cx="100" cy="100" r="51" fill="none" stroke="#f7a823" stroke-width="1.2" stroke-dasharray="2 3"/>
<text font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="11" letter-spacing="2.6" fill="#1a1714"><textPath href="#igpt" startOffset="50%" text-anchor="middle">HIGHEST TITLE</textPath></text>
<text font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="10" letter-spacing="2.2" fill="#1a1714" dy="9"><textPath href="#igpb" startOffset="50%" text-anchor="middle">WORKING DOG SPORT</textPath></text>
<text x="100" y="94" text-anchor="middle" font-family="Anton, Archivo, Arial, sans-serif" font-weight="900" font-size="26" letter-spacing="2" fill="#fff">IGP</text>
<text x="100" y="134" text-anchor="middle" font-family="Anton, Archivo, Arial, sans-serif" font-weight="900" font-size="46" fill="#f7a823">3</text>
<g fill="#f7a823"><circle cx="58" cy="100" r="2.4"/><circle cx="142" cy="100" r="2.4"/></g></svg>'''

def igp_band():
    cards = ''.join(f'<div class="igp-c"><p class="igp-k">0{i + 1}</p><h3>{h}</h3><p>{t}</p></div>' for i, (h, t) in enumerate(IGP_FACTS))
    return f'''<section class="sec igp"><div class="wrap pad stack-l">
<div class="igp-top">{igp_badge()}<div class="stack" style="gap:12px"><p class="mono steel">What IGP 3 means</p><h2 class="d d-md">The highest title in working dog sport.</h2>
<p class="muted igp-lead">Caesar, a Von Forell Dobermann handled by Dr Michael Kern, earned his IGP 3. He was the first Dobermann in Australia to reach it since the late 1980s.</p>
<a class="link" href="{KERN_URL}">Read Dr Kern's interview →</a></div></div>
<div class="igp-g">{cards}</div></div></section>'''


def kern_snip(p):
    pb = p['slug'] == 'purple-boost'
    q = "The \u2018Purple Boost\u2019 product is incredible." if pb else "Caesar is thriving on this food."
    im = IMG.get('t-kern')
    return f'''<section class="sec kern-snip"><div class="wrap pad"><div class="ks">
<div class="ks-img">{f'<img src="{im["src"]}" alt="Dr Michael Kern with Caesar" loading="lazy">' if im else ''}{igp_badge("ks-medal")}</div>
<div class="ks-body"><p class="mono steel">Proven at the top of the sport</p>{stars()}
<blockquote class="ks-q">\u201c{q}\u201d</blockquote>
<p class="ks-who"><b>Dr Michael Kern</b> · Neurosurgeon, Perth · handler of Caesar, Von Forell Dobermann</p>
<ul class="ks-facts"><li><b>IGP 3</b><span>the highest title in working dog sport</span></li><li><b>1st</b><span>Dobermann in Australia to reach it since the late 1980s</span></li><li><b>~1 hr</b><span>with our nutritionist before he switched</span></li></ul>
<p class="disclose">Disclosure: Caesar was bred by Von Forell, Kris's kennel.</p>
<a class="link" href="{KERN_URL}">Read the full interview →</a></div></div></div></section>'''

def featured_review(t, side='left', theme=''):
    im = IMG.get('t-' + t['id'])
    img = f'<div class="fr-img"><img src="{im["src"]}" alt="{E(t["dog"])}" loading="lazy"></div>' if im else ''
    rel = f'<p class="disclose">Disclosure: {E(t["rel"])}</p>' if t.get('rel') else ''
    return f'''<section class="sec fr {theme}"><div class="wrap pad"><div class="fr-grid{' fr-flip' if side == 'right' else ''}">{img}
<figure class="fr-body">{stars()}<blockquote class="fr-q">“{E(t["q"])}”</blockquote>
<figcaption><b>{E(t["name"])}</b><span>{E(t["role"])} · {E(t["dog"])}</span></figcaption>{rel}
<a class="link" href="reviews.html">Read all {len(T)} reviews →</a></figure></div></div></section>'''


def tcard(t, photo=True):
    im = IMG.get('t-' + t['id'])
    ava = (f'<img src="{im["src"]}" alt="{E(t["name"])}\'s dog" loading="lazy">' if im else
           f'<span class="ava" aria-hidden="true">{E(t["name"][0])}</span>')
    big = (f'<div class="tphoto"><img src="{im["src"]}" alt="{E(t["dog"])}" loading="lazy"></div>' if (im and photo and im.get('big')) else '')
    rel = f'<p class="disclose">Disclosure: {E(t["rel"])}</p>' if t.get('rel') else ''
    return f'''<article class="tcard" data-tags="{t["tags"]}">{big}{stars()}
<blockquote>“{E(t["q"])}”</blockquote>
<div class="who">{ava}<div><p style="font-weight:700">{E(t["name"])}</p><p class="small muted">{E(t["role"])}</p><p class="mono steel" style="font-size:10.5px;margin-top:2px">{E(t["dog"])}</p></div></div>{rel}
</article>'''


def dogcard(t, name, tag, vid):
    im = IMG.get('t-' + t['id'])
    img = f'<img src="{im["src"]}" alt="{E(t["dog"])}" loading="lazy">' if im else '<span class="need">PHOTO / VIDEO NEEDED</span>'
    return f'''<article class="dogcard"><div class="vid">{img}<div class="over"><p class="mono" style="color:#f0643a">{tag}</p>
<div><p class="name">{name}</p><p class="mono" style="color:#c3c8bf;margin-top:10px;display:flex;gap:10px;align-items:center"><span class="play" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M4 2l10 6-10 6z" fill="#121412"/></svg></span>{vid}</p></div></div></div>
{stars()}<blockquote style="margin:0;font-size:19px;line-height:1.35;font-weight:600">“{E(t["q"])}”</blockquote>
<p class="mono muted">{E(t["name"])} · {E(t["role"])}</p></article>'''


PD_BASIS = {'dog': (180, '30 kg adult'), 'puppy': (205, '15 kg pup, 4–6 mo'), 'supplement': (3, '20 kg dog'), 'cat': (80, '4 kg cat, est.')}
CART_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 3.5h2.6l2.3 11.2a1.6 1.6 0 0 0 1.6 1.3h8.6a1.6 1.6 0 0 0 1.6-1.2l1.6-7.3H6.1"/><circle cx="9.5" cy="20" r="1.4"/><circle cx="17.5" cy="20" r="1.4"/></svg>'


def ico(d):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'


I_TRUCK = ico('<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>')
I_SHIELD = ico('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>')
I_STAR = ico('<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.5 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>')
I_CLOCK = ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_REPEAT = ico('<path d="M4 12a8 8 0 0 1 14-5.3L20 8M20 4v4h-4M20 12a8 8 0 0 1-14 5.3L4 16M4 20v-4h4"/>')
NEEDS = [('turkey-grain-free.html', 'Working &amp; sport', 'Turkey Grain Free', ico('<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>')),
         ('puppy-lamb-and-fish.html', 'Growing puppies', 'Puppy Lamb &amp; Fish', ico('<circle cx="6.5" cy="9" r="1.8"/><circle cx="10" cy="5.5" r="1.8"/><circle cx="14" cy="5.5" r="1.8"/><circle cx="17.5" cy="9" r="1.8"/><path d="M8 17.5c0-3 1.8-5.5 4-5.5s4 2.5 4 5.5c0 1.6-1.8 2.5-4 2.5s-4-.9-4-2.5z"/>')),
         ('ocean-fish.html', 'Sensitive gut &amp; skin', 'Ocean Fish', ico('<path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19l7-7"/>')),
         ('feeding-guide.html?goal=family', 'Active family dogs', 'Find the right food', ico('<path d="M3 11l9-7 9 7v9H3z"/><path d="M9 20v-6h6v6"/>')),
         ('purple-boost.html', 'Gut support', 'Purple Boost', ico('<rect x="6" y="8" width="12" height="13" rx="2"/><path d="M8 3h8v5H8z"/>')),
         ('shop.html#cats', 'Cats', 'iPurr range', ico('<path d="M5 4l3 4h8l3-4v9a7 7 0 0 1-14 0z"/><circle cx="9.5" cy="13" r=".8"/><circle cx="14.5" cy="13" r=".8"/>'))]


def usp_bar():
    items = [(I_TRUCK, 'Free metro delivery', f'on orders over ${FREE_SHIP}'), (I_REPEAT, 'Subscribe &amp; save', 'skip or cancel anytime'),
             (I_SHIELD, 'Palatability guarantee', 'or your money back'), (I_STAR, 'Australian made', '97.2% Aussie ingredients')]
    li = ''.join(f'<li class="{"on" if i == 0 else ""}">{ic}<span><b>{a}</b> {c}</span></li>' for i, (ic, a, c) in enumerate(items))
    return f'<div class="usp tone"><div class="wrap"><ul data-usp>{li}</ul></div></div>'


def needs_block():
    tiles = ''.join(f'<a class="need" href="{h}"><span class="need-ic tone">{ic}</span><span class="need-t">{t}</span><span class="need-s">{s} →</span></a>' for h, t, s, ic in NEEDS)
    return plain_section(f'<div class="row between" style="margin-bottom:24px;align-items:baseline"><h2 class="d d-md">Shop by need</h2><a class="link" href="shop.html">See the full range →</a></div><div class="needs">{tiles}</div>', 'alt', 'pad-s')


TL_DETAIL = {
    '1980': ('First Dobermann', 'At 16, after the family home was broken into, Kris bought his first Dobermann and started training dogs.', 'kris'),
    '1982': ('Von Forell begins', 'A dog let him down in a real situation. Training wasn\'t enough, so Kris turned to genetics and started breeding under the Von Forell name.', 'kennel'),
    '1984': ('Working dogs for hire', 'Kris sets up a dog security company in Melbourne, putting his dogs to work every day.', None),
    '1993': ('Raising the standard', 'Joins the National Dog Trainers Federation and starts a frozen semen bank to protect the best bloodlines.', None),
    '2000': ('Detector Dogs Australia', 'Co-founds Detector Dogs Australia. Its teams now search venues like the MCG and the Port of Melbourne.', 'dda1'),
    '2003': ('National champion', 'Von Forell Vilco wins the National Australian Schutzhund Championship. Kris is made a Life Member of the NDTF.', 'training'),
    '2015': ('Performadog in the kennel', 'After his sponsor\'s food changed and his dogs lost condition, Kris starts trialling his own formula on the Von Forell dogs.', 'range'),
    '2018': ('Bill Wiadrowski joins', 'Animal nutritionist Bill Wiadrowski, formulating diets since 1986, joins to refine the range.', None),
}


def timeline(years=None):
    ys = [y for y, _ in TIMELINE if (years is None or y in years)]
    btns = ''.join(f'<button class="tl-y" type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}"><span class="tl-dot"></span>{y}</button>' for i, y in enumerate(ys))
    panels = ''
    for i, y in enumerate(ys):
        h, txt, img = TL_DETAIL[y]
        media = pic(img, '', 'ratio-43', eager=True) if img and IMG.get(img) else f'<div class="tl-big tone"><span>{y}</span></div>'
        panels += f'<div class="tl-p" role="tabpanel" data-i="{i}" {"" if i == 0 else "hidden"}>{media}<div class="stack"><p class="mono steel">{y}</p><h3 class="h2">{h}</h3><p class="muted">{txt}</p></div></div>'
    return f'''<div class="tline" data-tline><div class="tl-head"><div class="tl-ys" role="tablist" aria-label="Timeline">{btns}</div>
<div class="tl-nav"><button class="tl-arr" type="button" data-tl-prev aria-label="Previous">←</button><button class="tl-arr" type="button" data-tl-next aria-label="Next">→</button></div></div>
<div class="tl-rail"><span class="tl-fill" data-tl-fill></span></div><div class="tl-ps">{panels}</div></div>'''


def basis(p):
    if p['slug'] == 'puppy-lamb-and-fish':
        return PD_BASIS['puppy']
    return PD_BASIS[p['kind']]


def pday(p, kg, price):
    g, _ = basis(p)
    return price / (kg * 1000 / g)



def _min_pd():
    best = None
    for p in PRODUCTS:
        if p['kind'] != 'dog' or p['slug'] == 'puppy-lamb-and-fish':
            continue
        for label, kg, price in p['sizes']:
            if price:
                v = round(pday(p, kg, price), 2)
                if best is None or v < best[0]:
                    best = (v, f'{p["name"]}, {basis(p)[1]}, {label} bag')
    return best

def default_size(p):
    priced = [s for s in p['sizes'] if s[2]]
    return next((s for s in priced if s[0] in ('15 kg', '1.08 kg')), priced[-1])


def buy_box(p, compact=True):
    d = default_size(p)
    sz = ''
    for label, kg, price in p['sizes']:
        if not price:
            continue
        on = 'true' if label == d[0] else 'false'
        sz += f'<button class="sz" type="button" aria-pressed="{on}" data-size="{label}" data-price="{price}" data-pd="{pday(p, kg, price):.2f}">{label}</button>'
    one = len([s for s in p['sizes'] if s[2]]) == 1
    return f'''<div class="buy" data-buy data-id="{p["slug"]}" data-name="{E(p["name"])}" data-img="assets/img/product/{p["img"]}">
{'' if one else f'<div class="szs" role="group" aria-label="Bag size">{sz}</div>'}{sz if one else ''}
<div class="buy-price"><span class="bp" data-bp>{money(d[2])}</span><span class="bpd"><b data-bpd>{money(round(pday(p, d[1], d[2]), 2))}</b>/day<span class="bpx"> · {basis(p)[1]}</span></span></div>
<div class="buy-ctas"><button class="btn btn-ember" type="button" data-add>{CART_SVG}Add to cart</button><a class="btn btn-line" href="{p["slug"]}.html">View product</a></div>
</div>'''


def feed_card(p):
    stat = (f'<p class="big">{p["protein"]}<small>%</small></p><p class="mono muted" style="padding-bottom:10px">Protein<br>{p["fat"]}% fat</p>' if p.get('protein') else
            '<p class="big">9<small>×</small></p><p class="mono muted" style="padding-bottom:10px">Probiotic strains<br>+ prebiotic</p>')
    return f'''<article class="feed">
<div style="display:flex;justify-content:space-between;align-items:baseline"><p class="mono">{p["code"]}</p><p class="mono muted">{p["job"]}</p></div>
<a class="pack tone" href="{p["slug"]}.html"><img src="assets/img/product/{p["img"]}" alt="{E(p["full"])} bag" loading="lazy"></a>
<div class="row" style="align-items:flex-end;gap:14px">{stat}</div>
<h3 class="h2" style="font-size:26px"><a href="{p["slug"]}.html" style="text-decoration:none">{E(p["name"])}</a></h3>
<p class="muted" style="font-size:15px">{E(p["blurb"])}</p>
{buy_box(p)}
</article>'''


def pcard(p):
    lo = min(s[2] for s in p['sizes'] if s[2])
    badge = {'turkey-grain-free': 'Best seller', 'ocean-fish': 'Most reviewed', 'purple-boost': 'Add-on'}.get(p['slug'], '')
    return f'''<article class="pcard" data-tags="{p["tags"]}">
<a class="pimg tone" href="{p["slug"]}.html">{f'<span class="badge">{badge}</span>' if badge else ''}<img src="assets/img/product/{p["img"]}" alt="{E(p["full"])}" loading="lazy"></a>
<div class="pbody"><span class="tag">{E(p["job"])}</span><h3 class="h3" style="font-size:22px"><a href="{p["slug"]}.html" style="text-decoration:none">{E(p["name"])}</a></h3>
<p class="muted small">{E(p["blurb"])}</p>
{buy_box(p)}</div></article>'''


def lab_sheet():
    rows = ''.join(f'<tr><td>{m} <span style="color:#565a54">({u})</span></td><td style="color:#565a54">TBC</td><td style="color:#565a54">TBC</td><td class="after">TBC</td></tr>' for m, u, _ in MARKERS)
    return f'''<div class="sheet"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;border-bottom:2px solid #121412;padding-bottom:12px">
<p class="mono">Haematology &amp; biochemistry</p><p class="mono" style="color:#565a54">{tbc("[Lab]")} · {tbc("[Date 1]")} → {tbc("[Date 2]")}</p></div>
<div style="overflow-x:auto"><table><thead><tr><th>Marker</th><th>Ref. range</th><th>Before</th><th>After 12 mo</th></tr></thead><tbody>{rows}</tbody></table></div>
<p style="margin-top:14px;font-size:12px;color:#565a54">Figures go in from the two lab reports. One dog's documented results. Individual results vary.</p></div>'''


# ---- pages --------------------------------------------------------------------
def home():
    global MIN_PD
    MIN_PD = _min_pd()
    t = {x['id']: x for x in T}
    hero = IMG.get('hero')
    if hero:
        hero_cls = 'shot'
        hero_inner = ('<span class="stock-tag br">Stock, to replace</span>' if hero.get('stock') else '') + f'<img src="{hero["src"]}" alt="{E(hero["alt"])}"' + (f' style="object-position:{hero["pos"]}"' if hero.get('pos') else '') + '>'
    else:
        hero_cls = 'shot ph'
        hero_inner = '<p class="mono" style="position:absolute;left:16px;top:44px">Von Forell Dobermann mid-track, low sun, handler in frame</p>'
    ticker_items = ['Caesar · Dobermann · <span class="ember">IGP 3</span>', 'Tasmania K9 Search &amp; Rescue',
                    'Swift &amp; Rolex · Rottweilers · <span class="ember">20 km endurance test</span>', 'Koda · medical alert dog',
                    '4 New Zealand German Shepherd kennels', 'Core Canine · board &amp; train']
    tick = ''.join(f'<span>{x}</span><span class="sep">/</span>' for x in ticker_items) * 2
    feeds = ''.join(feed_card(BY_SLUG[s]) for s in ('turkey-grain-free', 'ocean-fish', 'puppy-lamb-and-fish', 'purple-boost'))
    tl = ''.join(f'<li><p class="yr">{y}</p><p class="small muted" style="margin-top:6px">{x}</p></li>' for y, x in TIMELINE if y in ('1980', '1982', '2000', '2003', '2015', '2018'))
    strip = ''.join(f'<figure>{pic(s, "", "ratio-43")}<figcaption class="mono muted">{c}</figcaption></figure>' for s, c in (('dda1', 'MCG · corporate box search'), ('dda2', 'Port of Melbourne · truck search'), ('dda3', 'Vehicle search'), ('dda4', 'Rubble search')))
    dogs = (dogcard(t['craig'], 'SAR team', 'Search &amp; rescue', 'James Craig · video to film') +
            dogcard(t['allgemein'], 'Rolex', 'Rottweiler · 20 km endurance', 'Allgemein Rottweilers · video to film') +
            dogcard(t['wilson'], 'Koda', 'Labrador · medical alert', 'Derek Wilson · video to film'))
    body = f'''
<section class="sec hero"><div class="wrap">
<div class="hero2">
<div class="hero-copy">
<a class="hero-rating" href="reviews.html">{stars()}<span><b>5.0</b> from {len(T)} reviews<span class="hr-x"> · Rated 9/10 by Petfood Reviews</span></span></a>
<h1 class="d d-xl"><span>Bred &amp; fed</span><span class="ember">for performance.</span></h1>
<p class="lead">Australian-made dog food, built by a breeder of working dogs and an animal nutritionist. Fed to sport, working and family dogs since 2015.</p>
<div class="hero-pd"><span class="hero-pd-k">Feed your dog from as little as</span><span class="hero-pd-row"><span class="hero-pd-n">{money(MIN_PD[0])}</span><span class="hero-pd-t"><b>per day</b>{MIN_PD[1]}</span></span></div>
<div class="row" style="gap:18px;align-items:center"><a class="btn btn-ember btn-lg" href="shop.html">Shop now</a><a class="link" href="feeding-guide.html">Find my dog's food →</a></div>

</div>
<div class="{hero_cls} hero-shot">{hero_inner}
<svg class="track" viewBox="0 0 800 450" preserveAspectRatio="none" aria-hidden="true"><path d="M-10 420 C 120 400, 160 330, 260 340 S 420 380, 500 290 S 640 150, 820 120" fill="none" stroke="#f0643a" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/></svg>
</div>
</div></div>
</section>
{usp_bar()}

{rail_section(1, 'Shop the formula', f"""<div class="row between" style="margin-bottom:40px"><h2 class="d d-md">Four products. One job each.</h2>
<p class="muted" style="max-width:28em">Formulated with Bill Wiadrowski, animal nutritionist since 1986. 97.2% Australian ingredients. Real meat first. Price per day is worked out from the feeding table printed on the bag. Bigger bags work out cheaper.</p></div>
<div class="feeds">{feeds}</div>""", theme='', sid='formula')}
{igp_band()}
{featured_review(t['kern'])}
{needs_block()}
{calc_block('<div class="calc-head"><p class="mono steel">Feeding calculator</p><h2 class="d d-md">Take out the guesswork.</h2><p class="muted">Four questions. Which food, how much a day, how long a bag lasts and what it costs.</p></div>').replace('<section class="sec">', '<section class="sec" id="calculator">', 1)}

{rail_section(2, 'Origin', f"""<div class="split split-wide" style="align-items:end"><h2 class="d d-md">A dog let him down when it counted.</h2>
<div class="stack"><p class="muted">Training wasn't enough, so Kris turned to breeding. Decades on, he'd learned two things make a performance dog: breeding and nutrition. When his sponsor's food changed and his dogs lost condition, he built his own.</p>
<a class="link" href="story.html">Read Kris's story →</a></div></div>
<div class="mt">{timeline()}</div>""", theme='alt')}

{rail_section(3, 'Evidence', f"""<div class="split"><div class="stack-l"><h2 class="d d-md">Don't take our word for it. Take the lab's.</h2>
<p class="muted lead">One working dog. The same blood panel, twelve months apart, on nothing but Performadog. Every number published, and labelled for what it is: one dog's results.</p>
<a class="btn btn-ember" href="case-study.html" style="align-self:flex-start">Read the full report</a></div>
{lab_sheet()}</div>""", theme='tone')}
{featured_review(t['jones-walker'], 'right', 'alt')}

<section class="sec" style="border-top:1px solid var(--hair)"><div class="wrap"><div class="rail pad"><span class="node" style="top:80px"></span>
<p class="mono file steel">File 04 · The dogs</p>
<div class="row between" style="margin-bottom:40px"><h2 class="d d-md">Fed to dogs with a job to do.</h2><a class="link" href="reviews.html">Read all {len(T)} →</a></div>
<div class="g3">{dogs}</div>
</div></div></section>

{rail_section(5, 'The difference', f"""<h2 class="d d-md" style="margin-bottom:32px">What sets it apart from supermarket "premium"</h2>
<div class="tbl-wrap"><table class="tbl stk"><thead><tr><th></th><th>Performadog</th><th>Typical supermarket premium</th></tr></thead><tbody>
<tr><td><strong>Built for</strong></td><td class="us" data-l="Performadog">Working dogs first. Fed in the Von Forell kennel since 2015</td><td data-l="Typical supermarket premium">The average pet</td></tr>
<tr><td><strong>Who formulated it</strong></td><td class="us" data-l="Performadog">Bill Wiadrowski, animal nutritionist since 1986</td><td data-l="Typical supermarket premium">Usually unnamed</td></tr>
<tr><td><strong>Where it comes from</strong></td><td class="us" data-l="Performadog">97.2% Australian ingredients · Australian made &amp; owned</td><td data-l="Typical supermarket premium">Often imported</td></tr>
<tr><td><strong>First ingredient</strong></td><td class="us" data-l="Performadog">Turkey, lamb or wild-caught tuna</td><td data-l="Typical supermarket premium">Often meat meal or by-products</td></tr>
<tr><td><strong>Preserved with</strong></td><td class="us" data-l="Performadog">Vitamin E and rosemary oil</td><td data-l="Typical supermarket premium">Varies</td></tr>
<tr><td><strong>Results on record</strong></td><td class="us" data-l="Performadog">Published lab panel + {len(T)} named owners</td><td data-l="Typical supermarket premium">Rarely published</td></tr>
</tbody></table></div>""", theme='')}

{cta_band()}'''
    return page('index.html', 'Performadog | Bred & fed for performance', 'Performance dog food built by a working-dog breeder and an animal nutritionist. Australian made.', body)


def shop():
    dog = ''.join(pcard(p) for p in PRODUCTS)
    body = page_head('Shop', ['The range'], 'Three dog foods, each with one job. A gut-support topper. And iPurr for the cats in the house. All Australian made.',
                     aside='<a class="link" href="feeding-guide.html">Not sure which? Build your dog\'s plan →</a>') + plain_section(f'''
<div class="chips" data-filter-group data-target="#grid" style="margin-bottom:28px">
<button class="chip" data-filter="all" aria-pressed="true">All</button><button class="chip" data-filter="working" aria-pressed="false">Working &amp; sport</button>
<button class="chip" data-filter="sensitive" aria-pressed="false">Sensitive</button><button class="chip" data-filter="puppy" aria-pressed="false">Puppy</button>
<button class="chip" data-filter="supplement" aria-pressed="false">Supplements</button><button class="chip" data-filter="cat" aria-pressed="false" id="cats">Cats (iPurr)</button></div>
<div class="g3" id="grid">{dog}</div>
<figure class="mt-l">{pic('range', '', 'ratio-169')}<figcaption class="mono muted mt-s">The full Performadog and iPurr range</figcaption></figure>
<div class="tbc-block mt"><p class="mono">Pending from Kris</p><p class="small">Bundles (which foods, sizes and price) and the 20 kg bag price. Both are built into the store and waiting on numbers.</p></div>''') + compare_block() + cta_band()
    return page('shop.html', 'Shop | Performadog', 'Performadog dog food, Purple Boost and iPurr cat food.', body, 'shop.html')


def compare_block():
    a = [BY_SLUG[s] for s in ('turkey-grain-free', 'ocean-fish', 'puppy-lamb-and-fish')]
    th = ''.join(f'<th>{E(p["name"])}</th>' for p in a)
    rows = [('Best for', [p['job'] for p in a]), ('Protein / fat', [f'{p["protein"]}% / {p["fat"]}%' for p in a]),
            ('Main protein', ['Turkey + lamb', 'Wild tuna + lamb', 'Lamb + wild tuna']),
            ('Grain free', ['Yes', 'No (rice, oat groats)', 'No (rice, oat groats)']), ('Chicken free', ['Yes (poultry oil)', 'Yes', 'Yes']),
            ('15 kg bag', [money(p['sizes'][2][2]) for p in a])]
    body = ''.join(f'<tr><td><strong>{k}</strong></td>' + ''.join(f'<td data-l="{E(p["name"])}">{E(v)}</td>' for p, v in zip(a, vals)) + '</tr>' for k, vals in rows)
    return plain_section(f'<h2 class="h2" style="margin-bottom:24px">Compare the dog foods</h2><div class="tbl-wrap"><table class="tbl stk"><thead><tr><th></th>{th}</tr></thead><tbody>{body}</tbody></table></div>', 'alt')


def product(p):
    sizes = ''
    first = True
    for label, kg, price in p['sizes']:
        if price is None:
            sizes += f'<button class="size" type="button" disabled aria-pressed="false"><b>{label}</b><span>Price {tbc("TBC")}</span></button>'
            continue
        on = 'true' if (len([s for s in p['sizes'] if s[2]]) == 1 or label in ('15 kg', '1.08 kg')) else 'false'
        sizes += f'<button class="size" type="button" aria-pressed="{on}" data-p="{price}" data-kg="{kg}" data-pd="{pday(p, kg, price):.2f}" data-size="{label}"><b>{label}</b><span>{money(price)} · {money(round(pday(p, kg, price), 2))}/day</span></button>'
    default = next((s for s in p['sizes'] if s[0] in ('15 kg', '1.08 kg')), p['sizes'][0])
    is_dog = p['kind'] == 'dog'
    pd = per_day(default[2], 15) if (is_dog and p['slug'] != 'puppy-lamb-and-fish') else None
    perday = f'<p class="small muted center">Works out at <strong class="ember" data-pdp-pd>{money(round(pday(p, default[1], default[2]), 2))}/day</strong> for a {basis(p)[1]}, from the feeding table on the bag</p>'
    analysis = ''.join(f'<div class="kv-i"><span>{k}</span><b>{v}</b></div>' for k, v in p['analysis'])
    an_note = f'<p class="small mt-s">{tbc("Figures from the current website. Kris to confirm against the bag")}</p>' if p.get('analysis_tbc') else ''
    ings = ''
    if p.get('ings'):
        li = ''.join(f'<li class="{"top" if i < 5 else ""}">' + (f'<a href="{ing_link(x)}">{E(x)}</a>' if ing_link(x) else E(x)) + '</li>' for i, x in enumerate(p['ings']))
        ings = f'''<div class="ic-head"><div class="stack" style="gap:6px"><p class="mono steel">What's in it</p><h2 class="h3">Real ingredients, in order</h2></div><p class="small muted">Tap any ingredient to see what it does. Main ingredients in order, then a full vitamin and mineral premix. Preserved naturally with vitamin E and rosemary oil.</p></div>
<div class="ingcs">{ing_circles(p)}</div>{('<p class="small">' + tbc('Order to confirm against the current bag') + '</p>') if p.get('ings_tbc') else ''}<a class="link" href="ingredients.html">See every ingredient and where it comes from →</a>'''
    feeding = ''
    if is_dog:
        rows = ''.join(f'<div class="kv-i kv-feed"><span>{w}</span><b>{g}</b><small>a day</small></div>' for w, g in BAG_TABLE)
        feeding = f'''<div class="stack"><div class="ic-head"><h2 class="h3">How much to feed</h2><p class="small muted">From the table printed on the bag. Split it into two meals. Add about 15% on heavy work days; ease off for a lighter dog.</p></div>
<div class="kv kv-5">{rows}</div>
<a class="link" href="feeding-guide.html">Work it out for your dog →</a></div>'''
    elif p['slug'] == 'purple-boost':
        feeding = '<div class="stack"><h2 class="h3">How to use it</h2><p class="muted">One 3 g scoop per 20 kg of dog, once a day, sprinkled over the food. Cats: a pinch. Start with half for the first few days when changing food.</p></div>'
    else:
        feeding = f'<div class="stack"><h2 class="h3">How much to feed</h2><p class="muted">From about 30–45 g a day for a 1–2 kg cat up to 110–130 g for a 6–7 kg cat. {tbc("Full table to confirm from the bag")}</p></div>'
    for_who = ''.join(f'<li>{E(x)}</li>' for x in p['for_who'])
    rel = {'turkey-grain-free': ['kern', 'craig', 'allgemein'], 'ocean-fish': ['jones-walker', 'talty', 'carrington'],
           'puppy-lamb-and-fish': ['wright', 'walker', 'blackburn'], 'purple-boost': ['eadweards'],
           'ipurr-kangaroo': ['mariettakis'], 'ipurr-ocean-fish': []}[p['slug']]
    tmap = {x['id']: x for x in T}
    pool = rel + [i for i in ('kern', 'craig', 'jones-walker', 'carrington', 'mahoney', 'doward', 'wright', 'kawecki') if i not in rel]
    revs = ''.join(tcard(tmap[i], photo=False) for i in pool[:6])
    note_kern = f'<p class="small">{tbc("Kris: confirm which food each of these dogs eats")}</p>' if p['slug'] == 'turkey-grain-free' else ''
    reviews = f'''<div class="stack-l"><div class="rv-head"><div class="stack" style="gap:10px"><p class="mono steel">Reviews</p><h2 class="d d-md">What owners say about Performadog</h2>
<p class="muted">Reviews of Performadog across the whole range, from handlers, breeders and family owners.</p></div>
<div class="rv-score"><p class="rv-n">5.0</p>{stars()}<p class="small muted">{len(T)} reviews</p><a class="btn btn-line" href="reviews.html">Read all reviews</a></div></div><div class="g3">{revs}</div></div>'''
    sub_block = ''
    if p['kind'] != 'supplement' or True:
        sub_block = f'''<div class="stack" style="gap:8px">
<button class="opt" type="button" aria-pressed="true" data-mode="sub"><span class="top"><span>Subscribe &amp; save {tbc("[X]%")}</span></span><span class="small muted">Free metro delivery on every order · skip, pause or cancel online</span></button>
<button class="opt" type="button" aria-pressed="false" data-mode="once"><span class="top"><span>One-time purchase</span><span data-once-price>{money(default[2])}</span></span></button></div>'''
    big_spec = ''
    if is_dog or p['kind'] == 'cat':
        hl = [(p["analysis"][0][1], 'Crude protein', 'minimum'), (p["analysis"][1][1], 'Crude fat', 'minimum'), (p["analysis"][4][1], 'Calcium', 'for bone and joint'),
              ("97.2%" if is_dog else "Taurine", "Australian ingredients" if is_dog else "Added for cats", "made and owned here" if is_dog else "for heart and eyes"), ('0', 'Chicken', 'none in the bag')]
        big_spec = ''.join(f'<div class="hl"><p class="hl-n">{n}</p><p class="hl-t">{t}</p><p class="hl-s">{s_}</p></div>' for n, t, s_ in hl)
    body = f'''<section class="sec"><div class="wrap" style="padding-top:28px;padding-bottom:72px">
<p class="mono muted" style="margin-bottom:20px"><a href="shop.html">Shop</a> / {E(p["job"])}</p>
<div class="pdp" data-pdp>
<div class="pdp-left"><div class="pdp-media tone"><img src="assets/img/product/{p["img"]}" alt="{E(p["full"])} bag"></div>
<ul class="pdp-trust pdp-trust-d"><li>{I_SHIELD}<span><b>Not eaten? Money back</b>Palatability guarantee</span></li><li>{I_TRUCK}<span><b>Free metro delivery</b>on orders over ${FREE_SHIP}</span></li><li>{I_STAR}<span><b>Australian made</b>and family owned</span></li></ul></div>
<div class="stack-l">
<div class="stack"><span class="tag tag-ember" style="align-self:flex-start">{E(p["job"])}</span>
<h1 class="d d-lg" style="font-size:clamp(44px,6vw,80px)">{E(p["name"])}</h1>
<a class="rating" href="#reviews">{stars()}<span><b>5.0</b> · {len(T)} reviews</span></a>
<p>{E(p["long"])}</p>
<p class="small" style="display:flex;gap:8px;align-items:center"><span style="width:8px;height:8px;border-radius:50%;background:var(--steel);display:inline-block"></span>Formulated with animal nutritionist Bill Wiadrowski</p></div>
<div class="stack" style="gap:10px"><p class="lbl">Size</p><div class="sizes">{sizes}</div><p class="small muted"><span data-per>{money(round(default[2] / default[1], 2))}/kg</span> on this size</p></div>
{sub_block}
<div class="stack" style="gap:8px"><button class="btn btn-ember btn-block" type="button" data-atc data-id="{p["slug"]}" data-name="{E(p["name"])}" data-img="assets/img/product/{p["img"]}">{CART_SVG}<span data-atc-label>Add to cart · subscribe</span></button>{perday}
<p class="small muted center">Secure checkout · free metro delivery over ${FREE_SHIP}</p></div>
<ul class="pdp-trust pdp-trust-m"><li>{I_SHIELD}<span><b>Not eaten? Money back</b>Palatability guarantee</span></li><li>{I_TRUCK}<span><b>Free metro delivery</b>on orders over ${FREE_SHIP}</span></li><li>{I_STAR}<span><b>Australian made</b>and family owned</span></li></ul>
<div class="ship-box" data-postcode><label class="lbl" for="pc">Delivery to your postcode</label>
<div class="field"><input id="pc" inputmode="numeric" maxlength="4" placeholder="e.g. 3757"><button class="btn btn-ink" type="button" style="min-height:48px">Check</button></div>
<p class="small" data-postcode-out>Metro: free over ${FREE_SHIP}. Regional: freight shown before you pay.</p></div>

</div></div></div></section>
<div class="sticky-atc" data-sticky-atc hidden><div class="wrap"><img src="assets/img/product/{p["img"]}" alt=""><div class="sa-txt"><b>{E(p["name"])}</b><span data-sa-price>{money(default[2])} · {default[0]}</span></div><button class="btn btn-ember" type="button" data-sa-add>Add to cart</button></div></div>
<section class="sec pdp-info"><div class="wrap pad stack-l">
{f'<div class="stack"><p class="mono steel">At a glance</p><div class="hls">{big_spec}</div></div>' if big_spec else ''}
{f'<div class="info-card">{ings}</div>' if ings else ''}
<div class="info-2">
<div class="info-card"><h2 class="h3">Who it's for</h2><ul class="ticks who-ticks">{for_who}</ul>{'' if ings else feeding}</div>
<div class="info-card"><div class="stack" style="gap:8px"><h2 class="h3">{"Typical analysis" if p["kind"] != "supplement" else "What's in a scoop"}</h2>{"<p class='small muted'>Formulated to meet Australian and AAFCO nutrient standards. " + tbc("Kris: confirm the exact AAFCO / AS 5812 statement") + "</p>" if p["kind"] != "supplement" else ""}</div>
<div class="kv">{analysis}</div>{an_note}</div>
</div>
{f'<div class="info-card">{feeding}</div>' if ings else ''}
</div></section>
<dialog class="ingd" data-ingd aria-labelledby="ingd-t"><div class="ingd-in"><button class="ingd-x" type="button" data-ingd-close aria-label="Close">✕</button>
<div class="ingd-c" data-ingd-c></div><h3 class="h3" id="ingd-t" data-ingd-t></h3><p class="ingd-p" data-ingd-p></p>
<div class="ingd-links"><a class="btn btn-ember" data-ingd-a href="#">Read more about it</a><a class="btn btn-line" href="ingredients.html">See every ingredient</a></div></div></dialog>
{kern_snip(p) if p["kind"] != "cat" else ""}
<section class="sec alt kris-band"><div class="wrap pad"><div class="kris-grid">
<div class="kris-img"><img src="{IMG['kris']['src']}" alt="Kris Kotsopoulos with a Von Forell Dobermann" loading="lazy"></div>
<div class="stack-l"><div class="stack"><p class="mono steel">Who makes it</p><h2 class="d d-md">Built by a performance breeder and dog nutritionist.</h2>
<p class="muted">Kris Kotsopoulos has bred and trained working dogs for over 45 years. When his sponsor's food changed and his dogs lost condition, he built his own with animal nutritionist Bill Wiadrowski. Every bag is fed in his Von Forell kennel first.</p></div>
<ol class="kris-tl"><li><b>1980</b><span>First Dobermann</span></li><li><b>2000</b><span>Co-founds Detector Dogs Australia</span></li><li><b>2015</b><span>Performadog fed in the kennel</span></li></ol>
<a class="btn btn-line" href="story.html">Read Kris &amp; Performadog's full story</a></div>
</div></div></section>
<section class="sec" id="reviews" style="border-top:1px solid var(--hair)"><div class="wrap pad">{reviews}</div></section>
{('' if p['slug'] == 'purple-boost' else plain_section(f"""<div class="row between info-card upsell" style="align-items:center;flex-direction:row"><div class="row" style="align-items:center;gap:20px"><img src="assets/img/product/purple_boost_3-cut.webp" alt="Purple Boost" style="height:120px;width:auto"><div class="stack" style="gap:6px"><p class="mono steel">Add to this bowl</p><h2 class="h2">Purple Boost</h2><p class="muted small">Purple carrot, 9-strain probiotic and prebiotic. From $43.</p></div></div><div class="row" style="gap:10px"><button class="btn btn-ember" type="button" data-quick-add data-id="purple-boost" data-name="Purple Boost" data-size="180 g" data-price="43" data-img="assets/img/product/purple_boost_3-cut.webp">{CART_SVG}Add · $43</button><a class="btn btn-line" href="purple-boost.html">View product</a></div></div>""", '', 'pad-s'))}
{faq_block(product_faqs(p))}
{cta_band()}'''
    return page(f'{p["slug"]}.html', f'{p["full"]} | Performadog', p['blurb'], body, 'shop.html')


def product_faqs(p):
    base = [('How do I switch my dog over?', 'Over about 10 days. Start with 10% Performadog mixed into the old food and add roughly 10% more each day until it is the whole meal. Dogs with a sensitive gut can take a few days longer.'),
            ('Why do I feed less than my last food?', 'The food is dense, so most owners feed less by weight than their previous brand. Start from the bag table and adjust to your dog\'s body condition.'),
            ('What if my dog won\'t eat it?', 'Return the bag at least 80% full with your invoice and we\'ll refund you. That\'s the palatability guarantee.'),
            ('Do you deliver to me?', f'Australia-wide. Metro orders over ${FREE_SHIP} ship free; regional freight is shown before you pay. Most orders leave within 24 hours.')]
    if p['kind'] == 'cat':
        base[0] = ('How do I switch my cat over?', 'Mix it into the old food over 7–10 days. Cats can be fussy, so go slower if needed.')
    return base


def faq_block(items, title='Questions'):
    acc = ''.join(f'<details class="acc"><summary>{E(q)}</summary><div class="body"><p>{a}</p></div></details>' for q, a in items)
    return plain_section(f'<div class="split split-narrow"><h2 class="d d-md">{title}</h2><div>{acc}</div></div>', '')


def story():
    tl = ''.join(f'<li><p class="yr">{y}</p><p class="small muted" style="margin-top:6px">{x}</p></li>' for y, x in TIMELINE)
    chapters = [('01', 'A dog let him down when it counted', 'Kris had trained the dog well. In a real situation it still didn\'t have the courage or robustness the job needed. Training alone wasn\'t enough, and that sent him into genetics and breeding in 1982.'),
                ('02', 'Two pillars make a performance dog', 'Years of breeding taught him that selection and nutrition carry a performance animal. If we ask dogs to work like athletes, we have to feed them like athletes.'),
                ('03', 'No food met the standard', 'Pro Plan sponsored his kennel for six years. When production moved, his dogs started losing condition, and nothing else on the shelf did what he needed.'),
                ('04', 'So he built it', 'With animal nutritionist Bill Wiadrowski, Kris developed the food he wanted for his own dogs and fed it to his kennel from 2015. It worked, the trainers and breeders around him asked for it, and Performadog became available to everyone.')]
    ch = ''.join(f'''<article class="row" style="gap:20px 48px;align-items:flex-start"><p class="d ember" style="font-size:72px;flex:0 0 110px">{n}</p>
<div class="stack" style="flex:1 1 420px;min-width:0"><h2 class="h2">{h}</h2><p class="muted">{b}</p></div></article>''' for n, h, b in chapters)
    body = f'''<section class="sec alt"><div class="wrap" style="padding-top:56px;padding-bottom:72px"><div class="split split-wide" style="align-items:end">
<div class="stack-l"><p class="mono steel">Our story</p><h1 class="d d-lg">The food a breeder built for his own dogs.</h1>
<p class="lead muted">Kris Kotsopoulos has trained working dogs since 1980 and bred them since 1982. Performadog came out of one lesson learned the hard way: you can't train or breed your way past poor nutrition.</p></div>
{pic('kris', 'Portrait: Kris and Tonia with a Von Forell Dobermann at Pheasant Creek', 'ratio-45')}</div></div></section>
<section class="sec"><div class="wrap pad"><div class="stack-l" style="max-width:920px;gap:56px">{ch}
<blockquote class="d d-sm" style="margin:0;border-top:2px solid var(--ink);padding-top:24px;text-transform:none;font-weight:700;font-size:clamp(28px,3.4vw,44px);line-height:1.05">“If we are asking dogs to perform at a high level, we are essentially asking them to function like athletes.”<span class="mono muted" style="display:block;margin-top:14px;font-weight:500">Kris Kotsopoulos · {tbc("confirm wording")}</span></blockquote>
</div></div></section>
<section class="sec alt"><div class="wrap pad"><div class="split split-wide" style="align-items:center"><div class="stack-l"><p class="mono steel">Detector Dogs Australia</p><h2 class="d d-md">Dogs that work where it matters</h2>
<p class="muted">Kris co-founded Detector Dogs Australia in 2000. Its teams search venues like the MCG and Marvel Stadium, the Port of Melbourne, hospitals and major events. Kris has been interviewed by SBS and Channel 9 about the work.</p>
<p class="small muted">{tbc("NFL letter (Shannon Bodley, NFL Security) goes here once Kris has written permission")}</p></div>{pic('kris_sbs', '', 'ratio-11')}</div>
<div class="strip mt-l">{''.join(f'<figure>{pic(s, "", "ratio-43")}<figcaption class="mono muted">{c}</figcaption></figure>' for s, c in (('dda1', 'MCG'), ('dda2', 'Port of Melbourne'), ('dda5', 'Grand Slam Oval'), ('dda4', 'Rubble search')))}</div></div></section>
{rail_section(1, '45 years with working dogs', f'<h2 class="d d-md" style="margin-bottom:32px">From one Dobermann to Detector Dogs Australia</h2>{timeline()}<p class="small muted mt">{tbc("Kris to sign off every date")}, his own sites give 1980 and 1981 for the first Dobermann.</p>')}
<section class="sec"><div class="wrap pad"><div class="g2">
<article class="stack">{pic('bill', 'Photo: Bill Wiadrowski', 'ratio-43')}<p class="mono steel">The nutritionist</p><h2 class="h2">Bill Wiadrowski</h2>
<p class="muted">Animal nutritionist designing dog and cat diets since 1986, and the mind behind Nutrient Ramping. Kris and Bill have built Performadog together since 2018. {tbc("Qualifications")}</p><a class="link" href="science.html#bill">Watch Bill answer 41 questions →</a></article>
<article class="stack">{pic('kennel', 'Photo: Kris and Tonia', 'ratio-43')}<p class="mono steel">Kris &amp; Tonia</p><h2 class="h2">Von Forell, Kinglake Ranges</h2>
<p class="muted">Kris and Tonia run Von Forell from Pheasant Creek, 45 km north of Melbourne. Von Forell litters are raised on Performadog. Kris also co-founded Detector Dogs Australia, whose teams work venues like the MCG and Port of Melbourne.</p><a class="link" href="https://www.vonforell.com/">Visit Von Forell →</a></article>
</div>
</div></section>
{cta_band("Feed your dog the way Kris feeds his.")}'''
    return page('story.html', 'Our story | Performadog', 'Kris Kotsopoulos, 45 years of working dogs, and the food he built for his own kennel.', body, 'story.html')


def science():
    body = page_head('The science', ['Built like', 'an athlete\'s diet'], 'How the food is formulated, what it is made from, and the evidence we can actually show you, including where it stops.') + f'''
{rail_section(1, 'Nutrient Ramping', f"""<div class="split split-wide"><div class="stack"><h2 class="d d-md">Bill Wiadrowski's method</h2>
<p class="muted lead">Bill has designed dog and cat diets since 1986. Nutrient Ramping is the approach behind every Performadog formula. {tbc("Bill: a plain-English definition, 2–3 sentences")}</p></div>
<div class="stack">{video_card(VIDEOS[0]) if VIDEOS else pic('bill', 'Video', 'ratio-169')}</div></div>
<div class="g3 mt-l">
<div class="stack" style="border-top:2px solid var(--ink);padding-top:18px"><p class="mono muted">01 · Ingredients</p><h3 class="h3">Real meat first, 97.2% Australian</h3><p class="muted">Turkey, lamb, wild-caught tuna and kangaroo from human-grade regional facilities.</p></div>
<div class="stack" style="border-top:2px solid var(--ink);padding-top:18px"><p class="mono muted">02 · Formulation</p><h3 class="h3">Dense, so you feed less</h3><p class="muted">Most owners feed less by weight than their last food. {tbc("Bill: the ramping step in one line")}</p></div>
<div class="stack" style="border-top:2px solid var(--ink);padding-top:18px"><p class="mono muted">03 · Manufacture</p><h3 class="h3">Made in Australia, HACCP &amp; GMP</h3><p class="muted">Preserved with vitamin E and rosemary. Six-layer resealable bag. {tbc("Manufacturer details Kris is happy to show")}</p></div>
</div>""")}
{rail_section(2, 'Gut health', f"""<div class="split"><div class="stack"><h2 class="d d-md">The gut does the work</h2>
<p class="muted">Kelp, yeast extract and Yucca schidigera are in every formula for intestinal health. Purple Boost adds a nine-strain probiotic (134M CFU per gram), a prebiotic yeast fraction and purple carrot: 13 kg of carrots in every kilo of powder.</p>
<a class="link" href="purple-boost.html">About Purple Boost →</a></div>
<div class="notice">We don't make disease claims for Purple Boost. The old site's cancer and weight-loss statements came from a rat study and have been left off this site on purpose.</div></div>""", theme='')}
{rail_section(3, 'Evidence', f"""<div class="split"><div class="stack-l"><h2 class="d d-md">One dog, two lab panels, one year apart</h2>
<p class="muted">The first published evidence on the site: a working dog's full blood panel before and after twelve months on Performadog. A documented case, not a clinical trial, and written up that way.</p>
<a class="btn btn-ember" href="case-study.html" style="align-self:flex-start">Read the case study</a></div>{lab_sheet()}</div>""")}
<section class="sec" id="bill"><div class="wrap pad"><div class="row between" style="margin-bottom:28px"><div class="stack"><p class="mono steel">Ask Bill</p><h2 class="h2">41 questions, answered on camera</h2></div><p class="muted" style="max-width:26em">Bill's Q&amp;A library from the current site, carried across: sourcing, manufacturing, raw vs dry, the microbiome and more.</p></div>
<div class="g4">{''.join(video_card(v) for v in VIDEOS[:8])}</div>
<a class="btn btn-line mt" href="library.html#videos">All {len(VIDEOS)} answers →</a></div></section>
{cta_band()}'''
    return page('science.html', 'The science | Performadog', 'Nutrient Ramping, gut health and the published lab case study.', body, 'science.html')


def case_study():
    rows = ''.join(f'''<div class="mrow"><div><p class="mono steel">{m} · {u}</p><p class="small muted" style="margin-top:4px">{w}</p></div>
<div class="mbar" aria-hidden="true"><div class="axis"></div><div class="rng"></div></div>
<div class="mvals"><span class="b">TBC</span><span class="muted">→</span><span class="a">TBC</span></div></div>''' for m, u, w in MARKERS)
    body = f'''<section class="sec alt"><div class="wrap" style="padding-top:56px;padding-bottom:40px">
<p class="mono steel" style="margin-bottom:20px">The science / Case study 01</p>
<h1 class="d d-lg" style="max-width:15ch">Twelve months on Performadog, in one dog's bloodwork</h1>
<p class="lead muted mt measure">{tbc("[Dog's name]")}, a {tbc("[age]")}-year-old working {tbc("[breed]")}, had a full blood panel on {tbc("[date 1]")}. After twelve months on Performadog the same panel was repeated at the same lab. Here is every result, against the lab's reference range.</p></div>
<div style="border-top:1px solid var(--hair);border-bottom:1px solid var(--hair)"><div class="wrap pad-s stats">
<div class="stat"><p class="n">1</p><span class="mono">Dog</span></div><div class="stat"><p class="n">12 mo</p><span class="mono">Between panels</span></div>
<div class="stat"><p class="n">8</p><span class="mono">Markers shown</span></div><div class="stat"><p class="n">{tbc("[Lab]")}</p><span class="mono">Laboratory</span></div></div></div>
<div class="wrap pad"><div class="row between" style="margin-bottom:12px"><h2 class="h2">The results</h2>
<p class="mono muted" style="display:flex;gap:18px;flex-wrap:wrap"><span>○ {tbc("Date 1")}</span><span>● {tbc("Date 2")}</span><span><span style="display:inline-block;width:22px;height:10px;background:var(--band);vertical-align:middle"></span> Reference range</span></p></div>
<div style="border-top:1px solid var(--hair)">{rows}</div>
<div class="tbc-block mt"><p class="mono">What we need</p><p class="small">The two lab reports (a phone photo is fine). That gives every value, unit, reference range, the lab's name and both dates. The page fills itself from there.</p></div></div></section>
<section class="sec"><div class="wrap pad"><div class="split">
<div class="stack"><p class="mono steel">What it shows, and what it doesn't</p><h2 class="h2">One dog's documented results. Not a promise for every dog.</h2>
<p class="muted">This is a single dog, not a controlled trial. Diet, training, age and health all affect bloodwork, so we can't say the food alone caused these changes. We publish the full reports so you and your vet can read them yourselves.</p></div>
<div class="stack"><p class="mono muted">Bill Wiadrowski, animal nutritionist</p><p class="h2" style="font-size:22px">{tbc("Bill's plain-English read of the results")}</p>{pic('bill', 'Video: Bill walks through the two panels', 'ratio-169')}</div>
</div>
<div class="g2 mt-l"><div class="stack"><h3 class="h3">How it was done</h3><ol class="muted" style="margin:0;padding-left:20px;display:flex;flex-direction:column;gap:8px"><li>Baseline panel taken by {tbc("[vet clinic]")}, analysed by {tbc("[lab]")}.</li><li>The dog ate Performadog {tbc("[food]")} as its only diet for 12 months, with normal training.</li><li>The same panel repeated at the same lab.</li></ol></div>
<div class="stack"><h3 class="h3">Read the reports</h3><a class="btn btn-line" href="#">Panel 1 (PDF) · {tbc("date")}</a><a class="btn btn-line" href="#">Panel 2 (PDF) · {tbc("date")}</a><p class="small muted">Got your own dog's bloodwork on Performadog? <a href="contact.html">Tell us</a>, we'd like to add more dogs.</p></div></div>
</div></section>
{cta_band("See what your dog should eat.")}'''
    return page('case-study.html', 'Lab case study | Performadog', 'One working dog, the same blood panel twelve months apart.', body, 'science.html')


def ingredients():
    blocks = ''
    for slug in ('turkey-grain-free', 'ocean-fish', 'puppy-lamb-and-fish', 'ipurr-kangaroo', 'ipurr-ocean-fish'):
        p = BY_SLUG[slug]
        li = ''.join(f'<li class="{"top" if i < 5 else ""}">' + (f'<a href="{ing_link(x)}">{E(x)}</a>' if ing_link(x) else E(x)) + '</li>' for i, x in enumerate(p['ings']))
        blocks += f'''<details class="acc" {"open" if slug == "turkey-grain-free" else ""}><summary>{E(p["full"])}</summary><div class="body" style="color:var(--ink)">
<ul class="ing">{li}</ul><p class="small muted">Plus vitamins A, C, D3, E, K, B1, B2, B6, B12, niacin, pantothenate, folic acid and biotin; minerals calcium, phosphorus, sodium, copper, zinc, iron, manganese and iodine. Preserved with vitamin E and rosemary oil.</p>
{('<p class="small">' + tbc("Order to confirm against the current bag") + '</p>') if p.get("ings_tbc") else '<p class="small muted">Order taken from the printed bag.</p>'}</div></details>'''
    sources = [('Turkey', 'Australia', 'Lean single-source protein'), ('Lamb', 'Australia · grass-fed', 'Second red-meat protein and natural fat'),
               ('Wild-caught tuna', tbc('Origin'), 'Protein and omega-3'), ('Kangaroo', 'Australia · wild', 'Novel protein for cats that react to chicken'),
               ('Sweet lupins', 'Australia', 'Slow carbohydrate and fibre'), ('Kelp', tbc('Origin'), 'Iodine and trace minerals'),
               ('Yucca schidigera', tbc('Origin'), 'Gut and stool support'), ('Vitamin & mineral premix', tbc('Origin'), 'Makes up most of the 2.8% non-Australian share')]
    rows = ''.join(f'<tr><td><strong>{a}</strong></td><td>{b}</td><td class="muted">{c}</td></tr>' for a, b, c in sources)
    body = page_head('Ingredients', ['Nothing', 'to hide'], '97.2% Australian ingredients. Human-grade meat from approved regional facilities. Here is every formula, ingredient by ingredient.') + f'''
{plain_section(f'<div class="split split-narrow"><div class="stack-l"><h2 class="d d-md">Every formula</h2>{pic("ingredients", "Flat-lay: turkey, lamb, wild tuna, lupins, kelp", "ratio-11")}</div><div>{blocks}</div></div>', '')}
{plain_section(f'<h2 class="h2" style="margin-bottom:20px">Where it comes from</h2><div class="tbl-wrap"><table class="tbl"><thead><tr><th>Ingredient</th><th>Source</th><th>Why it\'s there</th></tr></thead><tbody>{rows}</tbody></table></div><p class="small muted mt-s">{tbc("Kris: confirm origins, the more specific (state, farm), the stronger")}</p>', 'alt')}
{plain_section(f'''<div class="row between" style="margin-bottom:24px;align-items:flex-end"><div class="stack"><p class="mono steel">Ingredient guide</p><h2 class="d d-md">Why each one is in the bag</h2></div><p class="muted" style="max-width:30em">Every ingredient and nutrient in the range, explained. Tap one to read what it does and why Bill chose it.</p></div>
<div class="row" style="margin-bottom:20px;align-items:center"><label class="sr" for="iq">Search ingredients and nutrients</label><input class="input" id="iq" type="search" placeholder="Search: kelp, taurine, omega-3, zinc…" style="max-width:420px" data-lib-search="#igrid"></div>
<div class="chips" data-filter-group data-target="#igrid" style="margin-bottom:28px"><button class="chip" data-filter="all" aria-pressed="true">All ({sum(1 for a in LIB if a["kind"] in REF_KINDS)})</button><button class="chip" data-filter="ingredient" aria-pressed="false">Ingredients ({sum(1 for a in LIB if a["kind"] == "ingredient")})</button><button class="chip" data-filter="nutrient" aria-pressed="false">Nutrients ({sum(1 for a in LIB if a["kind"] == "nutrient")})</button></div>
<div class="lgrid" id="igrid">{"".join(lib_card(a) for a in LIB if a["kind"] in REF_KINDS)}</div>''', 'alt', sid='all') if LIB else ''}
{plain_section('<div class="g3"><div class="stack"><p class="mono steel">Never in it</p><h3 class="h3">No chicken in the dog range</h3><p class="muted">Turkey Grain Free uses poultry oil; the other formulas have no poultry at all.</p></div><div class="stack"><p class="mono steel">Never in it</p><h3 class="h3">No gluten, GMOs or dairy</h3><p class="muted">As printed on the bag.</p></div><div class="stack"><p class="mono steel">Never in it</p><h3 class="h3">No artificial preservatives</h3><p class="muted">Vitamin E and rosemary oil keep it fresh in a six-layer bag.</p></div></div>', '')}
{cta_band()}'''
    return page('ingredients.html', 'Ingredients | Performadog', 'Every Performadog ingredient, formula by formula.', body)


def calc_block(head=''):
    seg = lambda grp, opts: ''.join(f'<button class="chip" type="button" data-set="{grp}" data-val="{v}" aria-pressed="false">{t}</button>' for v, t in opts)
    return f'''<section class="sec"><div class="wrap pad">{head}<div class="calc" data-calc>
<div class="stack-l">
<div class="stack" style="gap:10px"><label class="lbl" for="cw">1 · Weight <span data-cw style="color:var(--ink);font-weight:600"></span></label><input id="cw" type="range" min="2" max="60" step="1" value="30"></div>
<div class="stack" style="gap:10px"><p class="lbl">2 · Age</p><div class="chips">{seg('stage', [('puppy', 'Puppy'), ('adult', 'Adult'), ('senior', 'Senior')])}</div>
<div class="chips" data-pup-row style="margin-top:4px">{seg('pup', [('3', '2–4 mo'), ('5', '4–6 mo'), ('7', '6–9 mo'), ('10', '9–12 mo')])}</div></div>
<div class="stack" style="gap:10px"><p class="lbl">3 · Workload</p><div class="chips">{seg('load', [('light', 'Light / less active'), ('active', 'Active'), ('working', 'Works or competes')])}</div></div>
<div class="stack" style="gap:10px"><p class="lbl">4 · Sensitive gut or itchy skin?</p><div class="chips">{seg('gut', [('no', 'No'), ('yes', 'Yes')])}</div></div>
<p class="small muted">Weight bands follow the bag: {", ".join(f"{w} {g}" for w, g in BAG_TABLE[:2])}… Working dogs get about 15% more, lighter dogs 15% less, seniors 10% less.</p>
</div>
<div class="calc-out" aria-live="polite">
<p class="mono" style="color:#f4a21c">Recommended</p>
<a data-o-food-link href="#" style="text-decoration:none"><p class="d d-md" data-o-food style="color:#f2eee6"></p></a>
<p class="big" data-o-g></p><p class="mono" style="margin-top:-8px">per day · <span data-o-meals></span></p>
<div class="grid"><div><p class="n" data-o-days></p><p class="mono" style="opacity:.8">15 kg bag lasts</p></div><div><p class="n" data-o-cost style="color:#f0643a"></p><p class="mono" style="opacity:.8">per day</p></div></div>
<p class="small" style="opacity:.85">Subscribe and we'll send the next bag <strong data-o-every></strong>, before this one runs out.</p>
<button class="btn btn-ember btn-block" type="button" data-calc-add>{CART_SVG}<span data-calc-add-label>Add 15 kg to cart</span></button><a class="btn btn-line btn-block" data-o-food-link href="#" style="color:#f2eee6;border-color:#c3c8bf">Shop now</a>
</div></div></div></section>'''


def feeding():
    rows = ''.join(f'<tr><td>{w}</td><td>{g}</td></tr>' for w, g in BAG_TABLE)
    seg = lambda grp, opts: ''.join(f'<button class="chip" type="button" data-set="{grp}" data-val="{v}" aria-pressed="false">{t}</button>' for v, t in opts)
    body = page_head('Feeding guide', ['Your dog\'s', 'plan'], 'Four questions. We\'ll tell you which food, how much a day, how long a bag lasts and what it costs, worked out from the table printed on the bag.') + f'''
{calc_block()}
{plain_section(f'<div class="g2"><div class="stack"><h2 class="h2">The bag table</h2><div class="tbl-wrap"><table class="tbl" style="min-width:0"><thead><tr><th>Dog weight</th><th>Per day (adult)</th></tr></thead><tbody>{rows}</tbody></table></div></div><div class="stack"><h2 class="h2">Switching over: 10 days</h2><ol class="muted" style="margin:0;padding-left:20px;display:flex;flex-direction:column;gap:10px"><li><strong style="color:var(--ink)">Days 1–3:</strong> about 25% Performadog, 75% old food.</li><li><strong style="color:var(--ink)">Days 4–6:</strong> half and half.</li><li><strong style="color:var(--ink)">Days 7–9:</strong> about 75% Performadog.</li><li><strong style="color:var(--ink)">Day 10:</strong> all Performadog. Split into two meals.</li></ol><p class="small muted">Sensitive gut? Take it slower and add Purple Boost from day one.</p></div></div>', 'alt')}
{cta_band("Feed it to your dog.")}'''
    return page('feeding-guide.html', 'Feeding guide | Performadog', 'Work out which Performadog food your dog needs, how much a day, and what it costs.', body, 'feeding-guide.html')


def reviews():
    cards = ''.join(tcard(t) for t in T)
    t = {x['id']: x for x in T}
    dogs = (dogcard(t['kern'], 'Caesar', 'Dobermann · IGP 3', 'Video to film') + dogcard(t['allgemein'], 'Rolex', 'Rottweiler · 20 km', 'Video to film') + dogcard(t['craig'], 'SAR team', 'Search &amp; rescue', 'Video to film'))
    body = page_head('Reviews', ['Handlers, breeders', '&amp; owners'], f'{len(T)} of the people feeding Performadog, in their own words, from the original website. Where someone sells the food or owns a Von Forell dog, we say so.',
                     aside='<p class="small muted">Rated 9/10 by Petfood Reviews (Turkey Grain Free, user score 4.58 from 126 votes).</p>') + f'''
{plain_section(f'<div class="row between" style="margin-bottom:28px"><div class="stack"><p class="mono steel">Long reads</p><h2 class="d d-md">Interviews with handlers</h2></div><a class="link" href="library.html">The library →</a></div><div class="lgrid">{"".join(lib_card(a) for a in LIB if a["kind"] == "interview")}</div>', '') if LIB else ''}
<section class="sec alt"><div class="wrap pad"><div class="row between" style="margin-bottom:28px"><h2 class="d d-md">On camera</h2><p class="muted" style="max-width:28em">Short phone interviews with handlers and owners, dog, job, result. {tbc("20–30 to film")}</p></div><div class="g3">{dogs}</div></div></section>
<section class="sec"><div class="wrap pad">
<div class="chips" data-filter-group data-target="#tgrid" style="margin-bottom:28px">
<button class="chip" data-filter="all" aria-pressed="true">All</button><button class="chip" data-filter="working" aria-pressed="false">Working dogs</button><button class="chip" data-filter="sport" aria-pressed="false">Sport</button>
<button class="chip" data-filter="breeder" aria-pressed="false">Breeders</button><button class="chip" data-filter="sensitive" aria-pressed="false">Sensitive gut &amp; skin</button><button class="chip" data-filter="puppy" aria-pressed="false">Puppies</button><button class="chip" data-filter="family" aria-pressed="false">Family dogs</button><button class="chip" data-filter="cat" aria-pressed="false">Cats</button></div>
<div class="masonry" id="tgrid">{cards}</div>
<div class="tbc-block mt"><p class="mono">Before launch</p><p class="small">Written OK from each person to reuse their words and photo on the new site. Most date from 2016–2020, so fresh ones from Kris's network will help.</p></div>
</div></section>
<section class="sec alt" id="share"><div class="wrap pad"><div class="split"><div class="stack-l"><p class="mono steel">Share your dog's story</p><h2 class="d d-md">Feeding Performadog? Tell us how it's going.</h2>
<p class="muted">What your dog does, what changed, and a photo if you have one. We read every one, and with your OK we'll add it here.</p></div>
<form class="stack card" style="padding:28px" data-preview>
<label class="lbl" for="sn">Your name &amp; suburb</label><input class="input" id="sn">
<label class="lbl" for="sd">Your dog (name, breed, age, job or sport)</label><input class="input" id="sd">
<label class="lbl" for="sf">Which food?</label><select class="input" id="sf"><option>Turkey Grain Free</option><option>Ocean Fish</option><option>Puppy Lamb &amp; Fish</option><option>Purple Boost</option><option>iPurr</option></select>
<label class="lbl" for="sm">What changed?</label><textarea class="input" id="sm"></textarea>
<label class="lbl" for="sp">Photo or video</label><input class="input" id="sp" type="file" accept="image/*,video/*" style="padding-top:10px">
<label class="small" style="display:flex;gap:10px;align-items:flex-start"><input type="checkbox" style="margin-top:5px"> You can publish my words and photo on the Performadog website.</label>
<button class="btn btn-ember" type="submit">Send my story</button><p class="small muted" data-form-out></p></form></div></div></section>
{cta_band()}'''
    return page('reviews.html', 'Reviews | Performadog', 'What handlers, breeders and owners say about Performadog.', body, 'reviews.html')


def where_to_buy():
    body = page_head('Where to buy', ['Online, or', 'from a stockist'], f'Order direct and we dispatch within 24 hours, Australia-wide. Or buy from a stockist near you.') + plain_section(f'''
<div class="g2"><div class="stack card" style="padding:28px"><p class="mono steel">Direct</p><h2 class="h2">Order online</h2><p class="muted">Free metro delivery over ${FREE_SHIP}. Regional freight shown before you pay. Subscribe and it arrives before you run out.</p><a class="btn btn-ember" href="shop.html" style="align-self:flex-start">Shop the range</a></div>
<div class="stack card" style="padding:28px"><p class="mono steel">Stockists</p><h2 class="h2">Near you</h2>
<div class="tbl-wrap"><table class="tbl" style="min-width:0"><thead><tr><th>Stockist</th><th>Area</th></tr></thead><tbody>
<tr><td>{tbc("Keryn Mahoney (distributor)")}</td><td>Tasmania</td></tr><tr><td>{tbc("Peter Tsamtsikas (distributor)")}</td><td>Adelaide</td></tr><tr><td>{tbc("Michelle's Dog Behaviour & Training")}</td><td>Yarra Valley VIC</td></tr><tr><td>{tbc("New Zealand importer")}</td><td>New Zealand</td></tr></tbody></table></div>
<p class="small">{tbc("Kris: send the current stockist list, or say it's direct only and this table comes out")}</p></div></div>
<div class="tbc-block mt"><p class="mono">For breeders, kennels &amp; trainers</p><p class="small">Bulk and kennel pricing for breeders and trainers who feed several dogs or puppy packs for new owners. {tbc("Kris: is there a trade price?")}</p></div>''', '') + cta_band()
    return page('where-to-buy.html', 'Where to buy | Performadog', 'Buy Performadog online or from a stockist.', body)


def delivery():
    body = page_head('Delivery, subscriptions &amp; guarantee', ['No surprises', 'at checkout'], f'Free metro delivery over ${FREE_SHIP}. Regional freight shown up front. Dispatched within 24 hours.') + plain_section(f'''
<div class="g2">
<div class="stack-l"><h2 class="d d-md">Delivery</h2>
<div class="tbl-wrap"><table class="tbl stk" style="min-width:0"><thead><tr><th>Where</th><th>Cost</th><th>Typical time</th></tr></thead><tbody>
<tr><td><strong>Metro</strong> (capital cities)</td><td data-l="Cost">Free over ${FREE_SHIP} · otherwise {tbc("$[flat rate]")}</td><td data-l="Typical time">2–4 business days</td></tr>
<tr><td><strong>Regional</strong></td><td data-l="Cost">{tbc("Surcharge by zone")} · shown before you pay</td><td data-l="Typical time">5–7 business days</td></tr>
<tr><td><strong>Subscriptions</strong></td><td data-l="Cost">Free metro delivery on every order</td><td data-l="Typical time">Timed to your dog</td></tr></tbody></table></div>
<p class="muted small">Orders leave within 24 hours by Australia Post or courier. PO Boxes are fine. Australia only.</p></div>
<div class="ship-box" data-postcode style="align-self:start"><label class="lbl" for="pc2">Check your postcode</label><div class="field"><input id="pc2" inputmode="numeric" maxlength="4" placeholder="e.g. 4000"><button class="btn btn-ink" type="button" style="min-height:48px">Check</button></div><p class="small" data-postcode-out>We'll tell you if you're metro or regional.</p><p class="small muted">Preview logic, the real zones are set in Shopify.</p></div>
</div>''', '') + plain_section(f'''<div class="split"><div class="stack-l"><p class="mono steel">Subscribe &amp; save</p><h2 class="d d-md">The next bag arrives before the last one runs out.</h2></div>
<ul class="stack" style="margin:0;padding:0;list-style:none">
<li><strong>{tbc("[X]%")} off every bag.</strong> <span class="muted">Timed to your dog's daily amount. The feeding guide works it out.</span></li>
<li><strong>Free metro delivery</strong> <span class="muted">on every subscription order.</span></li>
<li><strong>Skip, pause or cancel online.</strong> <span class="muted">No lock-in, no fees, no phone call needed.</span></li>
<li><strong>Change food or bag size</strong> <span class="muted">between orders.</span></li></ul></div>''', 'alt', sid='subscribe') + plain_section(f'''<div class="split"><div class="stack-l"><p class="mono steel">The guarantee</p><h2 class="d d-md">If your dog won't eat it, you get your money back.</h2></div>
<div class="stack"><p class="muted">Return the bag at least 80% full, with your invoice, and we'll refund you. {tbc("Kris: confirm the window (e.g. 30 days) and whether it covers repeat orders")}</p><p class="small muted">Your rights under Australian Consumer Law apply on top of this guarantee.</p></div></div>''', '', sid='guarantee') + cta_band()
    return page('delivery.html', 'Delivery, subscriptions & guarantee | Performadog', 'Delivery costs, subscriptions and the palatability guarantee.', body)


def faq():
    groups = [('The food', [('Is it only for working dogs?', 'No. It was built to working-dog standards and plenty of active family dogs eat it. The feeding guide sets the right food and amount for your dog.'),
                            ('Which food should I choose?', 'Turkey Grain Free for dogs that work, train or compete. Ocean Fish for itchy skin, allergies or a sensitive stomach. Puppy Lamb &amp; Fish while they grow.'),
                            ('Is it complete and balanced?', f'Yes. Formulated to meet Australian and AAFCO nutrient standards. {tbc("Exact statement to confirm")}'),
                            ('Is there chicken in it?', 'The dog range has no chicken. Turkey Grain Free contains poultry oil. iPurr Kangaroo was made for cats that react to chicken.'),
                            ('Who makes it?', f'It is made in Australia under HACCP and GMP. {tbc("Manufacturer details Kris is happy to show")}')]),
              ('Feeding', [('How much do I feed?', 'Start from the bag table, or use the feeding guide. Most owners feed less by weight than their last food.'),
                           ('How do I switch over?', 'Over about 10 days: 25%, then half, then 75%, then all Performadog.'),
                           ('Can I add raw meat or bones?', f'Many of our handlers do. {tbc("Bill: one line of guidance")}')]),
              ('Ordering &amp; delivery', [('How much is delivery?', f'Metro orders over ${FREE_SHIP} ship free. Regional freight is shown before you pay.'),
                                         ('How fast is it?', 'Dispatched within 24 hours. Metro usually 2–4 business days, regional 5–7.'),
                                         ('How do subscriptions work?', 'Pick the food and how often. We send it before you run out. Skip, pause or cancel online.'),
                                         ('What if my dog won\'t eat it?', 'Return the bag at least 80% full with your invoice for a refund.')])]
    inner = ''
    for g, items in groups:
        acc = ''.join(f'<details class="acc"><summary>{q}</summary><div class="body"><p>{a}</p></div></details>' for q, a in items)
        inner += f'<div class="split split-narrow" style="margin-bottom:56px"><h2 class="h2">{g}</h2><div>{acc}</div></div>'
    body = page_head('FAQ', ['Questions'], 'The ones we get asked most. Anything else, call Kris on ' + PHONE + '.') + plain_section(inner, '') + cta_band()
    return page('faq.html', 'FAQ | Performadog', 'Common questions about Performadog food, feeding and delivery.', body)


def contact():
    body = page_head('Contact', ['Talk to us'], f'Questions about your dog\'s diet are welcome. That\'s how most of our customers started. Call {PHONE} or send a message.') + plain_section(f'''
<div class="split"><div class="stack-l">
<div class="stack"><p class="mono steel">Phone</p><p class="d d-md">{PHONE}</p><p class="muted small">{tbc("Hours")}</p></div>
<div class="stack"><p class="mono steel">Post</p><p>PO Box 372<br>Whittlesea VIC 3757</p></div>
<div class="stack"><p class="mono steel">Email</p><p>{tbc("[store email]")}</p></div></div>
<form class="stack card" style="padding:28px" data-preview>
<label class="lbl" for="n">Name</label><input class="input" id="n" autocomplete="name">
<label class="lbl" for="e">Email</label><input class="input" id="e" type="email" autocomplete="email">
<label class="lbl" for="d">Your dog (breed, age, what they do)</label><input class="input" id="d">
<label class="lbl" for="m">Message</label><textarea class="input" id="m"></textarea>
<button class="btn btn-ember" type="submit">Send</button><p class="small muted" data-form-out></p></form></div>''', '')
    return page('contact.html', 'Contact | Performadog', 'Contact Performadog.', body)


REMAP = {}
REF_KINDS = ('ingredient', 'nutrient')


def build():
    global LIB, VIDEOS
    LIB = load_library()
    for a in LIB:
        if a['kind'] in ('ingredient', 'nutrient'):
            new = f"{a['kind']}-{a['slug']}.html"
            REMAP[a['file']] = new
            a['file'] = new
    VIDEOS = json.load(open(os.path.join(os.path.dirname(__file__), 'videos.json'))) if os.path.exists(os.path.join(os.path.dirname(__file__), 'videos.json')) else []
    pages = [home(), shop(), story(), science(), case_study(), ingredients(), feeding(), reviews(), where_to_buy(), delivery(), faq(), contact()]
    pages += [product(p) for p in PRODUCTS]
    pages += library_pages(LIB, VIDEOS)
    print(len(pages), 'pages')



# ---- library: the original site's articles, repackaged -------------------------
from markdown_it import MarkdownIt
import re, shutil, glob
MD = MarkdownIt('commonmark', {'html': False, 'linkify': False}).enable('table')
CONTENT = '/tmp/claude-0/-home-claude/d3614f29-b622-5364-ad71-b3bf29072599/scratchpad/content'
LIB_JSON = os.path.join(os.path.dirname(__file__), 'library.json')
KIND = {'ingredient': ('Ingredients', 'ingredient'), 'nutrient': ('Nutrients', 'nutrient'), 'interview': ('Handlers & breeders', 'interview'),
        'nutritionist': ('Ask Bill', 'nutritionist'), 'health': ('Dog health', 'health'), 'brand': ('Kris & the brand', 'brand'), 'product': ('Products', 'product')}


ING_MAP = {'turkey': 'turkey-meat', 'poultry oil': 'poultry-oil', 'lamb': 'lamb', 'australian lamb': 'lamb', 'grass-fed lamb': 'lamb', 'lamb fat': 'lamb',
           'field peas': 'field-peas', 'chickpeas': 'chick-peas', 'lentils': 'lentils', 'sweet lupins': 'lupins', 'egg': 'eggs', 'carrots': 'carrots',
           'spinach': 'spinach', 'parsley': 'parsley', 'kelp': 'kelp', 'tapioca': 'tapioca', 'yeast extract': 'yeast-extract', 'wild-caught tuna': 'tuna-wild-caught',
           'fish oil': 'fish-oil', 'rice': 'rice', 'oat groats': 'groats', 'alfalfa': 'alfalfa', 'garlic': 'garlic', 'methionine': 'methionine',
           'yucca schidigera': 'yucca-schidigera', 'wild kangaroo': 'wild-kangaroo'}
ING_EXTRA = {'taurine': 'An amino acid cats cannot make enough of on their own, so it is added to every iPurr bag for heart and eye health.'}


def ing_article(name):
    slug = ING_MAP.get(name.lower())
    return next((a for a in LIB if a['slug'] == slug), None) if slug else None


def ing_link(name):
    a = ing_article(name)
    return a['file'] if a else None


def ing_blurb(name):
    import re as _re
    if name.lower() in ING_EXTRA:
        return ING_EXTRA[name.lower()]
    a = ing_article(name)
    if not a:
        return ''
    paras = [p.strip() for p in a['body'].split('\n\n') if p.strip() and not p.strip().startswith(('#', '!', '|', '-', '*', '>'))]
    txt = _re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', paras[0] if paras else a['summary'])
    txt = _re.sub(r'[*_`]', '', txt)
    if len(txt) > 260:
        cut = txt[:260]
        txt = cut[:cut.rfind('. ') + 1] if '. ' in cut else cut.rsplit(' ', 1)[0] + '…'
    return txt


ING_FALLBACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19l7-7"/></svg>'


def ing_circles(p):
    out = ''
    for i, x in enumerate(p['ings']):
        a = ing_article(x)
        img = a['img'] if a and a.get('img') else ''
        art = a['file'] if a else ''
        face = f'<img src="{img}" alt="" loading="lazy">' if img else f'<span class="ingc-fb">{ING_FALLBACK}</span>'
        out += (f'<button class="ingc{" top" if i < 5 else ""}" type="button" data-ing="{E(x)}" data-ing-img="{img}" data-ing-txt="{E(ing_blurb(x))}" data-ing-url="{art}">'
                f'<span class="ingc-c">{face}</span><span class="ingc-n">{E(x)}</span></button>')
    return out


def load_library():
    if not os.path.exists(LIB_JSON):
        return []
    return json.load(open(LIB_JSON))


def lib_card(a, big=False):
    img = f'<div class="limg"><img src="{a["img"]}" alt="" loading="lazy"></div>' if a.get('img') else f'<div class="limg lph"><span>{E(a["title"][:1])}</span></div>'
    return f'''<a class="lcard" href="{a["file"]}" data-tags="{a["kind"]}" data-title="{E(a["title"].lower())}">{img}
<div class="lbody"><p class="mono steel">{KIND.get(a["kind"], ("Notes",))[0]}{(" · " + a["year"]) if a.get("year") else ""}</p><h3 class="h3">{E(a["title"])}</h3><p class="small muted">{E(a.get("summary", ""))}</p></div></a>'''


def library_pages(lib, videos):
    if not lib:
        return []
    out = []
    journal = [a for a in lib if a['kind'] not in REF_KINDS]
    by_kind = {}
    for a in journal:
        by_kind.setdefault(a['kind'], []).append(a)
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All</button>' + ''.join(
        f'<button class="chip" data-filter="{k}" aria-pressed="false">{v[0]} ({len(by_kind.get(k, []))})</button>' for k, v in KIND.items() if by_kind.get(k))
    cards = ''.join(lib_card(a) for a in journal)
    vids = ''
    if videos:
        vids = plain_section(f'''<div class="row between" style="margin-bottom:28px"><div class="stack"><p class="mono steel">Ask Bill</p><h2 class="d d-md">{len(videos)} questions, answered on camera</h2></div><p class="muted" style="max-width:26em">Bill Wiadrowski, animal nutritionist since 1986, on sourcing, manufacturing, raw vs dry, the microbiome and more.</p></div>
<div class="g4">{"".join(video_card(v) for v in videos)}</div>''', 'alt', sid='videos')
    body = page_head('Journal', ['Stories, advice', 'and answers'], f'{len(journal)} articles from the original Performadog site: handler and breeder interviews, Ask Bill, dog health and Kris\u2019s story. Looking for an ingredient? <a href="ingredients.html#all">See the ingredient guide</a>.') + f'''
<section class="sec"><div class="wrap pad">
<div class="row" style="margin-bottom:24px;align-items:center"><label class="sr" for="lq">Search the journal</label><input class="input" id="lq" type="search" placeholder="Search: puppies, joints, Rottweilers, Bill…" style="max-width:420px" data-lib-search="#lgrid"></div>
<div class="chips" data-filter-group data-target="#lgrid" style="margin-bottom:28px">{chips}</div>
<div class="lgrid" id="lgrid">{cards}</div></div></section>{vids}{cta_band()}'''
    out.append(page('library.html', 'Journal | Performadog', 'Handler interviews, Bill Wiadrowski\'s Q&A, dog health and the Performadog story.', body, 'library.html'))
    for a in lib:
        out.append(article(a, lib))
    return out


def video_card(v):
    return f'''<button class="vcard" type="button" data-yt="{E(v["id"])}" aria-label="Play: {E(v["title"])}"><span class="vthumb"><img src="https://i.ytimg.com/vi/{E(v["id"])}/hqdefault.jpg" alt="" loading="lazy"><span class="play" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M4 2l10 6-10 6z" fill="#121412"/></svg></span></span><span class="vtitle">{E(v["title"])}</span></button>'''


def related_products(a):
    text = (a['title'] + ' ' + a.get('body', '')).lower()
    hits = []
    for p in PRODUCTS:
        for word in p.get('ings', []) + [p['name']]:
            w = word.lower().replace('wild-caught ', '').replace('australian ', '').replace('grass-fed ', '')
            if len(w) > 3 and w in a['title'].lower():
                hits.append(p); break
    return hits[:3] or [BY_SLUG['turkey-grain-free'], BY_SLUG['ocean-fish']]


def article(a, lib):
    import re as _re
    body_html = _re.sub(r'\*\*', '', MD.render(_re.sub(r'\*\*(\s*[?.,!:;]\s*)\*\*', r'\1', a.get('body', ''))))
    hero = f'<div class="shot ratio-169" style="margin-top:32px"><img src="{a["img"]}" alt="" ></div>' if a.get('img') else ''
    extra = ''.join(f'<figure style="margin:32px 0"><div class="shot ratio-43"><img src="{s}" alt="" loading="lazy"></div></figure>' for s in a.get('more_imgs', [])[:3])
    yt = ''.join(f'<div class="vembed"><iframe src="https://www.youtube-nocookie.com/embed/{E(y)}" title="Video" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>' for y in a.get('yt', [])[:2])
    rel = [x for x in lib if x['kind'] == a['kind'] and x['file'] != a['file']][:3]
    prods = related_products(a)
    pcards = ''.join(f'<a class="mini" href="{p["slug"]}.html"><img src="assets/img/product/{p["img"]}" alt=""><span><b>{E(p["name"])}</b><span class="small muted">From {money(min(s[2] for s in p["sizes"] if s[2]))} · {money(round(pday(p, default_size(p)[1], default_size(p)[2]), 2))}/day</span><span class="mono ember" style="font-size:11px;margin-top:4px">View product →</span></span></a>' for p in prods)
    words = len(a.get('body', '').split())
    claims = ''  # claims notes go to Kris by email, not in the preview
    body = f'''<section class="sec alt"><div class="wrap" style="padding-top:48px;padding-bottom:48px"><div style="max-width:880px">
<p class="mono steel">{('<a href="ingredients.html#all" style="text-decoration:none">Ingredient guide</a>' if a["kind"] in REF_KINDS else '<a href="library.html" style="text-decoration:none">Journal</a>')} / {KIND.get(a["kind"], ("Notes",))[0]}</p>
<h1 class="d d-lg" style="margin-top:18px;font-size:clamp(40px,5.6vw,80px)">{E(a["title"])}</h1>
<p class="lead muted mt-s">{E(a.get("summary", ""))}</p>
<p class="mono muted mt-s">{E(a.get("date_h", ""))}{" · " if a.get("date_h") else ""}{max(1, round(words / 220))} min read</p>{hero}</div></div></section>
<section class="sec"><div class="wrap pad"><div class="art">
<article class="prose">{claims}{body_html}{extra}{yt}
<p class="small muted" style="margin-top:40px;border-top:1px solid var(--hair);padding-top:16px">First published on performadog.com.au{(" in " + a["year"]) if a.get("year") else ""}. Lightly edited for the new site. This is general information, not veterinary advice.</p></article>
<aside class="stack-l"><div class="stack"><p class="mono steel">Feed it</p>{pcards}</div>
{('<div class="stack read-next"><p class="mono steel">Read next</p>' + "".join(f'<a class="link" href="{r["file"]}">{E(r["title"])}</a>' for r in rel) + '</div>') if rel else ''}</aside>
</div></div></section>{cta_band()}'''
    return page(a['file'], f'{a["title"]} | Performadog {"ingredient guide" if a["kind"] in REF_KINDS else "journal"}', a.get('summary', '')[:155], body, 'ingredients.html' if a['kind'] in REF_KINDS else 'library.html')


if __name__ == '__main__':
    build()
