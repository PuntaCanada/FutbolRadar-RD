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
  self.assertTrue(all(not x['publish'] for x in json.loads((p/'data/sources.json').read_text())))
  payload=json.loads((p/'data/national.json').read_text())
  if isinstance(payload,dict):
   self.assertEqual(payload['license'],'CC0-1.0'); self.assertGreaterEqual(len(payload['matches']),164)
   self.assertEqual(len({(m['date'],m['opponent']) for m in payload['matches']}),len(payload['matches']))
   for l in ['es','en','de','fr','it']:
    self.assertIn('id="national-rows"',(p/'public'/l/'seleccion/index.html').read_text())
  else: self.assertEqual(payload,[])
 def test_parser(self):
  raw=b'date,home_team,away_team,home_score,away_score,tournament,city,country,neutral\n2000-01-01,Dominican Republic,Test,1,1,Friendly,City,Country,TRUE\n'
  shoot=b'date,home_team,away_team,winner\n2000-01-01,Dominican Republic,Test,Dominican Republic\n'
  m=parse(raw,shoot)[0];self.assertEqual((m['venue'],m['gf'],m['ga'],m['shootout']),('neutral',1,1,'win'))
  with self.assertRaises(ValueError): parse(raw+raw.splitlines()[1]+b'\n',shoot)
if __name__=='__main__':unittest.main(verbosity=2)
