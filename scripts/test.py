import unittest,json
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
  self.assertEqual(json.loads((p/'data/national.json').read_text()),[])
if __name__=='__main__':unittest.main(verbosity=2)
