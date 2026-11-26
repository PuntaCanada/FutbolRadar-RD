"""Fetch a pinned upstream snapshot; never publish partial or unchecked data."""
import csv, io, json, hashlib, re, urllib.request, os
from datetime import date
from pathlib import Path
from national_integrity import preserve, load
TEAM='Dominican Republic'
UPSTREAM='https://github.com/martj42/international_results'
ROOT=Path(__file__).resolve().parents[1]
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'FutbolRadarRD'}),timeout=30) as r:
  data=r.read(30_000_001)
  if len(data)>30_000_000: raise ValueError('oversize')
  return data
def parse(results, shootouts):
 def rows(raw): return csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
 penalties={}
 for r in rows(shootouts):
  if TEAM not in (r['home_team'],r['away_team']): continue
  key=(r['date'],r['home_team'],r['away_team'])
  if key in penalties or r['winner'] not in key[1:]: raise ValueError('invalid shootout')
  penalties[key]=r['winner']
 seen=set(); matches=[]
 for r in rows(results):
  if TEAM not in (r['home_team'],r['away_team']): continue
  key=(r['date'],r['home_team'],r['away_team'])
  if key in seen: raise ValueError('duplicate '+str(key))
  seen.add(key)
  day=date.fromisoformat(r['date'])
  if day>date.today() or key[1]==key[2] or not all(r[k].strip() for k in ('home_team','away_team','tournament','country','city')): raise ValueError('invalid match')
  h,a=(int(r[k]) for k in ('home_score','away_score'))
  if not (0<=h<=99 and 0<=a<=99): raise ValueError('invalid score')
  neutral=r['neutral'].lower()
  if neutral not in ('true','false'): raise ValueError('invalid neutral flag')
  winner=penalties.pop(key,None)
  if winner and h!=a: raise ValueError('shootout with unequal score')
  home=key[1]==TEAM
  gf,ga=(h,a) if home else (a,h)
  matches.append(dict(date=key[0],opponent=key[2] if home else key[1],venue='neutral' if neutral=='true' else ('home' if home else 'away'),gf=gf,ga=ga,competition=r['tournament'],city=r['city'],country=r['country'],shootout=('win' if winner==TEAM else 'loss') if winner else None))
 if penalties: raise ValueError('unmatched shootouts')
 return sorted(matches,key=lambda x:(x['date'],x['opponent']))
def main():
 meta=json.loads(get('https://api.github.com/repos/martj42/international_results'))
 if meta.get('license',{}).get('spdx_id')!='CC0-1.0': raise ValueError('license not verified')
 rev=os.environ.get('NATIONAL_UPSTREAM_SHA') or json.loads(get('https://api.github.com/repos/martj42/international_results/commits/'+meta['default_branch']))['sha']
 if not re.fullmatch('[a-f0-9]{40}',rev): raise ValueError('invalid revision')
 base='https://raw.githubusercontent.com/martj42/international_results/'+rev+'/'
 license_text=get(base+'LICENSE')
 if b'CC0' not in license_text or b'1.0' not in license_text: raise ValueError('pinned license not verified')
 raw=get(base+'results.csv'); shoot=get(base+'shootouts.csv')
 matches=parse(raw,shoot)
 if len(matches)<164 or matches[0]['date']!='1949-05-14' or matches[-1]['date']<'2026-11-17': raise ValueError('snapshot below audited coverage')
 payload=dict(source=UPSTREAM,revision=rev,license='CC0-1.0',sha256=hashlib.sha256(raw).hexdigest(),shootouts_sha256=hashlib.sha256(shoot).hexdigest(),matches=matches)
 target=ROOT/'data/national.json'; temp=target.with_suffix('.tmp')
 old=load(target)
 added=preserve(old,payload)
 if not added:
  print('No new Dominican Republic results; no publication')
  return
 sources_path=ROOT/'data/sources.json'
 sources=load(sources_path)
 active=[s for s in sources if s['publish']]
 if len(active)!=1 or active[0]['id']!='national': raise ValueError('unexpected source registry')
 active[0]['revision']=rev
 source_temp=sources_path.with_suffix('.tmp')
 source_temp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 source_temp.replace(sources_path)
 temp.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(target)
 print('Validated',len(matches),matches[0]['date'],matches[-1]['date'],'revision',rev,'sha256',payload['sha256'])
if __name__=='__main__': main()
