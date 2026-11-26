import json, re
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://github.com/martj42/international_results'
def load(path): return json.loads(path.read_text(encoding='utf-8'))
def index(payload):
 if payload['source']!=SOURCE or payload['license']!='CC0-1.0': raise ValueError('source/license')
 for k,n in [('revision',40),('sha256',64),('shootouts_sha256',64)]:
  if not re.fullmatch('[a-f0-9]{'+str(n)+'}',payload[k]): raise ValueError(k)
 out={}
 for m in payload['matches']:
  day=date.fromisoformat(m['date'])
  if day>date.today() or day.isoformat()!=m['date']: raise ValueError('date')
  if any(not isinstance(m[k],str) or not m[k].strip() for k in ('opponent','competition','city','country')): raise ValueError('text')
  if m['opponent']=='Dominican Republic' or m['venue'] not in ('home','away','neutral'): raise ValueError('team/venue')
  if any(type(m[k]) is not int or not 0<=m[k]<=99 for k in ('gf','ga')): raise ValueError('score')
  if m['shootout'] not in (None,'win','loss') or (m['shootout'] and m['gf']!=m['ga']): raise ValueError('shootout')
  key=(m['date'],m['opponent'])
  if key in out: raise ValueError('duplicate')
  out[key]=m
 if list(out)!=sorted(out): raise ValueError('order')
 return out
def preserve(old,new):
 a,b=index(old),index(new)
 if any(b.get(k)!=v for k,v in a.items()): raise ValueError('Historical deletion or change requires review')
 return len(b)-len(a)
def validate_current():
 baseline=load(ROOT/'data/national-baseline.json')
 current=load(ROOT/'data/national.json')
 preserve(baseline,current)
 sources=load(ROOT/'data/sources.json')
 active=[s for s in sources if s['publish']]
 if len(active)!=1 or active[0]['id']!='national' or active[0]['revision']!=current['revision'] or active[0]['license']!=current['license']: raise ValueError('source registry mismatch')
 return current
if __name__=='__main__': validate_current()
