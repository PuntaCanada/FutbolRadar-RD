import json, html, os
from national_view import render
from academies_view import render_academies, A
from players_view import render_players, P, L as PLAYER_LABELS
from ldf_view import render_ldf, D as LDF
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'public'; out.mkdir(exist_ok=True)
langs=json.loads((root/'data/translations.json').read_text()); sources=json.loads((root/'data/sources.json').read_text()); sponsor=json.loads((root/'data/sponsorship.json').read_text())
assert sponsor['enabled'] is False and not sponsor['placements'] and not sponsor['affiliateLinks']
sections=['','seleccion','liga','academias','fuentes','patrocinio']; base=os.getenv('SITE_URL','').rstrip('/')
if base and not base.startswith('https://'): raise ValueError('HTTPS SITE_URL required')
urls=[]
for lang,t in langs.items():
 for i,section in list(enumerate(sections))+[(2,'liga/'+slug) for slug,name in LDF['clubs']]+[(0,'legionarios')]+[(0,'legionarios/'+p['id']) for p in P]+[(3,'academias/'+a['id']) for a in A]:
  path=f'/{lang}/'+(section+'/' if section else ''); dest=out/path.strip('/');dest.mkdir(parents=True,exist_ok=True)
  nav=''.join(f'<a href="/{lang}/{s+"/" if s else ""}">{html.escape(t[j])}</a>' for j,s in enumerate(sections))
  nav+=f'<a href="/{lang}/legionarios/">{html.escape(PLAYER_LABELS[lang][0])}</a>'
  switch=' '.join(f'<a hreflang="{l}" href="/{l}/{section+"/" if section else ""}">{l.upper()}</a>' for l in langs)
  alternate=''.join(f'<link rel="alternate" hreflang="{l}" href="{base}/{l}/{section+"/" if section else ""}">' for l in langs) if base else ''
  canonical=f'<link rel="canonical" href="{base}{path}">' if base else '<meta name="robots" content="noindex">'
  content=html.escape(t[8] if i==5 else t[7]); title=html.escape(t[i])
  if i==1: content=render(lang) or content
  if i==2:
   club=next((name for slug,name in LDF['clubs'] if section=='liga/'+slug),None)
   content=render_ldf(lang,club)
   if club: title=html.escape(club)
  if i==3:
   academy=next((a for a in A if section=='academias/'+a['id']),None)
   content=render_academies(lang,academy)
   if academy:title=html.escape(academy['name'])
  if i==4: content='<ul>'+''.join(f'<li><a href="{html.escape(s["url"],quote=True)}">{html.escape(s["id"])}</a> — {html.escape(s["status"])}</li>' for s in sources)+'</ul>'
  if i==0: content += '<div class="tiles">'+''.join(f'<a href="/{lang}/{s}/">{html.escape(t[j])}</a>' for j,s in enumerate(sections) if j in (1,2,3))+'</div>'
  if section=='legionarios' or section.startswith('legionarios/'):
   player=next((p for p in P if section=='legionarios/'+p['id']),None)
   title=html.escape(player['name'] if player else PLAYER_LABELS[lang][0]); content=render_players(lang,player)
  (dest/'index.html').write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | FútbolRadar RD</title><meta name="description" content="{html.escape(t[6],quote=True)}">{canonical}{alternate}<link rel="stylesheet" href="/style.css"><script defer src="/theme.js"></script></head><body><header><a class="brand" href="/{lang}/">⚽ FútbolRadar <b>RD</b></a><div>{switch} <button id="theme" aria-label="Light / dark">◐</button></div></header><nav>{nav}</nav><main><div class="hero"><p>FÚTBOLRADAR RD</p><h1>{title}</h1><p>{html.escape(t[6])}</p></div><section>{content}</section></main><footer>FútbolRadar RD · <a href="/{lang}/fuentes/">{html.escape(t[4])}</a></footer></body></html>',encoding='utf-8')
  urls.append(base+path)
(out/'index.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=/es/"><a href="/es/">FútbolRadar RD</a></html>')
(out/'robots.txt').write_text('User-agent: *\nDisallow: /\n' if not base else 'User-agent: *\nAllow: /\nSitemap: '+base+'/sitemap.xml\n')
if base: (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(u)+'</loc></url>' for u in urls)+'</urlset>')
elif (out/'sitemap.xml').exists(): (out/'sitemap.xml').unlink()
