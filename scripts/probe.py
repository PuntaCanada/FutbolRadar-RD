import urllib.request, xml.etree.ElementTree as ET, csv, io, sys
from datetime import date
feeds=['https://www.fedofutbol.do/feed/','https://www.futboltotalrd.com/feed/']
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'FutbolRadarRD source audit'}),timeout=20) as r: return r.read(20_000_000)
failed=False
for url in feeds:
 try:
  root=ET.fromstring(get(url)); items=root.findall('./channel/item'); assert items and any(x.findtext('link') for x in items); print(url,'items',len(items),'latest',items[0].findtext('pubDate'))
 except Exception as e: failed=True; print(url,type(e).__name__,str(e))
try:
 url='https://raw.githubusercontent.com/martj42/international_results/master/results.csv'; rows=list(csv.DictReader(io.StringIO(get(url).decode('utf-8-sig')))); matches=[r for r in rows if 'Dominican Republic' in (r['home_team'],r['away_team'])]; assert matches; dates=[date.fromisoformat(r['date']) for r in matches]; print('National team candidate rows:',len(matches),min(dates),max(dates)); print('Audit only; no automatic publication before license and scope validation.')
except Exception as e: failed=True; print('National dataset',type(e).__name__,str(e))
sys.exit(int(failed))
