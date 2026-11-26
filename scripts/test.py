import unittest,json
from import_national import parse
from pathlib import Path
p=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 def test_pages(self):
  for l in ['es','en','de','fr','it']:
   for s in ['', 'seleccion','liga','academias','fuentes','patrocinio']:
    text=(p/'public'/l/s/'index.html').read_text();self.assertIn(f'lang="{l}"',text);self.assertIn('/theme.js',text);self.assertNotIn('affiliate_id=',text)
 def test_sponsor(self):
  s=json.loads((p/'data/sponsorship.json').read_text());self.assertFalse(s['enabled']);self.assertFalse(s['affiliateLinks']);self.assertEqual(s['placements'],[]);self.assertIn('youth',s['excludedSections'])
 def test_sources(self):
  sources=json.loads((p/'data/sources.json').read_text())
  self.assertEqual([x['id'] for x in sources if x['publish']],['national'])
  payload=json.loads((p/'data/national.json').read_text())
  if isinstance(payload,dict):
   self.assertEqual(payload['license'],'CC0-1.0'); self.assertEqual(len(payload['matches']),164)
   self.assertEqual(payload['revision'],'ca84241bb3eed854a1956a2fab442fe4daad40dd')
   m=payload['matches']; self.assertEqual((sum(x['gf']>x['ga'] for x in m),sum(x['gf']==x['ga'] for x in m),sum(x['gf']<x['ga'] for x in m)),(65,26,73))
   self.assertEqual((sum(x['gf'] for x in m),sum(x['ga'] for x in m)),(274,267))
   self.assertEqual(len({(m['date'],m['opponent']) for m in payload['matches']}),len(payload['matches']))
   for l in ['es','en','de','fr','it']:
    self.assertIn('id="national-rows"',(p/'public'/l/'seleccion/index.html').read_text())
  else: self.fail('Committed national snapshot missing')
 def test_ldf(self):
  from ldf_view import D
  self.assertEqual(len(D['clubs']),8)
  self.assertEqual(len({x[0] for x in D['clubs']}),8)
  self.assertEqual(D['regularMatches'],8*14//2)
  self.assertEqual(len(D['champions']),11)
  self.assertEqual(D['matches'],[])
  self.assertEqual(D['standings'],[])
  self.assertFalse(D['embedEnabled'])
  self.assertEqual(set(D['clubFacts']),{slug for slug,name in D['clubs']})
  for fact in D['clubFacts'].values():
   self.assertTrue(fact['city'] and fact['stadium'] and fact['sources'])
   self.assertTrue(all(url.startswith('https://') for url in fact['sources']))
  for lang in ['es','en','de','fr','it']:
   overview=(p/'public'/lang/'liga/index.html').read_text()
   self.assertIn('id="ldf-season"',overview)
   for slug,name in D['clubs']:
    self.assertIn(f'/{lang}/liga/{slug}/',overview)
    profile=(p/'public'/lang/'liga'/slug/'index.html').read_text()
    self.assertIn(f'<html lang="{lang}">',profile)
    self.assertIn('id="club-facts"',profile)
    self.assertIn(D['clubFacts'][slug]['city'],profile)
    self.assertIn(D['stadiumReferenceSeason'],profile)
    self.assertNotIn('<iframe',profile)
 def test_players(self):
  from players_view import D,P
  self.assertEqual(len(P),18)
  self.assertEqual(len({x['id'] for x in P}),18)
  self.assertEqual(sum(x['source']=='fed' for x in P),17)
  for lang in ['es','en','de','fr','it']:
   page=(p/'public'/lang/'legionarios/index.html').read_text()
   self.assertEqual(page.count('class="player-card"'),18)
   for player in P:
    profile=(p/'public'/lang/'legionarios'/player['id']/'index.html').read_text()
    self.assertIn('id="player-profile"',profile)
    self.assertIn(D['sources'][player['source']]['date'],profile)
    self.assertNotIn('<img',profile)
 def test_player_careers(self):
  from players_view import CAREERS,P
  self.assertEqual(set(CAREERS['profiles']),{'junior-firpo','xavier-valdez','pablo-rosario','heinz-morschel','peter-gonzalez','noah-dollenmayer','edison-azcona','mariano-diaz'})
  for player in P:
   career=CAREERS['profiles'].get(player['id'])
   for lang in ['es','en','de','fr','it']:
    profile=(p/'public'/lang/'legionarios'/player['id']/'index.html').read_text()
    self.assertEqual('id="player-career"' in profile,bool(career))
    if career:
     self.assertEqual(set(career['text']),{'es','en','de','fr','it'})
     for url in career['sources']:
      self.assertIn(url,profile)
     self.assertIn(CAREERS['checked'],profile)
 def test_academies(self):
  from academies_view import A,D
  self.assertEqual(len(A),6)
  self.assertEqual(len({a['id'] for a in A}),6)
  for lang in ['es','en','de','fr','it']:
   overview=(p/'public'/lang/'academias/index.html').read_text()
   self.assertEqual(overview.count('class="academy-card"'),6)
   for a in A:
    self.assertIn('/'+lang+'/academias/'+a['id']+'/',overview)
    profile=(p/'public'/lang/'academias'/a['id']/'index.html').read_text()
    self.assertIn('id="academy-profile"',profile)
    self.assertIn(D['checked'],profile)
    self.assertIn(a['contact'],profile)
    self.assertNotIn('<img',profile)
 def test_parser(self):
  raw=b'date,home_team,away_team,home_score,away_score,tournament,city,country,neutral\n2000-01-01,Dominican Republic,Test,1,1,Friendly,City,Country,TRUE\n'
  shoot=b'date,home_team,away_team,winner\n2000-01-01,Dominican Republic,Test,Dominican Republic\n'
  m=parse(raw,shoot)[0];self.assertEqual((m['venue'],m['gf'],m['ga'],m['shootout']),('neutral',1,1,'win'))
  with self.assertRaises(ValueError): parse(raw+raw.splitlines()[1]+b'\n',shoot)
if __name__=='__main__':unittest.main(verbosity=2)
