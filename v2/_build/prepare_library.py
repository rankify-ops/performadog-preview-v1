#!/usr/bin/env python3
"""One-off: turn the extracted performadog.com.au content into library.json + videos.json
and copy/resize the article images. Source: scratchpad extraction (content.json)."""
import json, os, re, sys
from PIL import Image
SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_IMG = os.path.join(HERE, '..', 'assets', 'img', 'library')
os.makedirs(OUT_IMG, exist_ok=True)
KEEP = {'ingredient', 'nutrient', 'interview', 'nutritionist', 'health', 'brand'}
RIGHTS = {'taurine': 'Written by Dr Jean Hofve: needs her permission',
          'petfood-review': 'Reproduces Petfood Reviews\' text: quote and link instead'}
recs = json.load(open(os.path.join(SRC, 'content.json')))
lib, held = [], []
for r in recs:
    if r['type'] != 'post' or r['kind'] not in KEEP:
        continue
    if r['slug'] in RIGHTS or 'lifewise' in (r['slug'] + r.get('body_text', '')[:400]).lower() and r['kind'] == 'interview' and 'kotsopoulos' in r['slug']:
        held.append({'slug': r['slug'], 'title': r['title'], 'why': RIGHTS.get(r['slug'], 'Written by LifeWise Pet Nutrition, with their images: needs their permission')})
        continue
    body = r.get('body_text', '').strip()
    body = re.sub(r'^#\s+.*\n+', '', body)  # drop a duplicated H1 title
    imgs = []
    for i, im in enumerate(r.get('images', [])):
        loc = im.get('local')
        if not loc:
            continue
        p = os.path.join(SRC, loc)
        if not os.path.exists(p):
            continue
        name = os.path.splitext(os.path.basename(loc))[0] + '.jpg'
        try:
            x = Image.open(p).convert('RGB'); x.thumbnail((1400, 1400)); x.save(os.path.join(OUT_IMG, name), quality=78, optimize=True, progressive=True)
            imgs.append('assets/img/library/' + name)
        except Exception as e:
            print('skip img', p, e)
    yt = []
    for y in r.get('youtube', []) or []:
        m = re.search(r'(?:v=|embed/|youtu\.be/)([A-Za-z0-9_-]{11})', y) or re.fullmatch(r'([A-Za-z0-9_-]{11})', y)
        if m:
            yt.append(m.group(1))
    year = (r.get('date') or '')[:4]
    lib.append({'slug': r['slug'], 'file': 'library-' + r['slug'] + '.html', 'title': r['title'].strip(), 'kind': r['kind'],
                'summary': r.get('summary', ''), 'body': body, 'img': imgs[0] if imgs else '', 'more_imgs': imgs[1:4],
                'yt': yt, 'year': year, 'date_h': year, 'claims': bool(r.get('claims_risk')), 'claims_note': r.get('claims_note', ''),
                'src_url': r.get('url', '')})
order = ['ingredient', 'interview', 'nutritionist', 'nutrient', 'health', 'brand']
lib.sort(key=lambda a: (order.index(a['kind']), a['title'].lower()))
json.dump(lib, open(os.path.join(HERE, 'library.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(held, open(os.path.join(HERE, 'library-held.json'), 'w'), indent=1)
vids, seen = [], set()
for v in json.load(open(os.path.join(SRC, 'videos.json'))):
    if v['id'] in seen:
        continue
    seen.add(v['id'])
    vids.append({'id': v['id'], 'title': (v.get('question_on_page') or v['title']).strip(), 'n': v.get('position')})
json.dump(vids, open(os.path.join(HERE, 'videos.json'), 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(len(lib), Counter(a['kind'] for a in lib), 'claims', sum(a['claims'] for a in lib), 'held', held, 'videos', len(vids))
