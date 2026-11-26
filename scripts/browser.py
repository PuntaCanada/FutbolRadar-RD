import json as _json
from pathlib import Path as _Path
expected_national=len(_json.loads((_Path(__file__).resolve().parents[1]/'data/national.json').read_text())['matches'])
import subprocess,time
from ldf_view import D
from players_view import P
from academies_view import A
from playwright.sync_api import sync_playwright
server=subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1','--directory','public'])
try:
 time.sleep(2)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for size in [{'width':1280,'height':800},{'width':390,'height':844},{'width':320,'height':700}]:
   page=browser.new_page(viewport=size,color_scheme='light')
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   for lang in ['es','en','de','fr','it']:
    for section in ['', 'seleccion/','liga/','academias/','fuentes/','patrocinio/']+['liga/'+slug+'/' for slug,name in D['clubs']]+['legionarios/']+['legionarios/'+p['id']+'/' for p in P]+['academias/'+a['id']+'/' for a in A]+['femenino/']:
     response=page.goto('http://127.0.0.1:8765/'+lang+'/'+section)
     assert response.ok
     assert page.locator('html').get_attribute('lang')==lang
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (size, page.url)
     assert page.locator('nav a').count()==8
     assert page.locator('nav').evaluate('(n)=>n.scrollWidth<=n.clientWidth')
     if section=='':
      assert page.locator('.home-stats strong').all_text_contents()==[str(expected_national),'18','7','8']
      assert page.locator('.home-panel').count()==4
      assert page.locator('.match-line').count()==8
      assert page.locator('nav a').evaluate_all('(links)=>links.every(a=>{const r=a.getBoundingClientRect();return r.left>=0 && r.right<=innerWidth})')
      if size['width']>=1280:
       assert page.locator('nav a').evaluate_all('(links)=>new Set(links.map(a=>Math.round(a.getBoundingClientRect().top))).size===1')
     if section=='femenino/':
      assert page.locator('#women-football table').evaluate('(t)=>t.scrollWidth<=t.parentElement.clientWidth+1')
      assert page.locator('#women-results tr td:last-child a:visible').count()==4
      assert page.locator('#women-results tr').count()==4
     if section=='academias/':
      assert page.locator('.academy-card:visible').count()==7
      for region in ['dn','la','st','lr','pp']:
       page.locator('#academy-region').select_option(region)
       assert page.locator('.academy-card:visible').count()==sum(a['region']==region for a in A)
      page.locator('#academy-region').select_option('')
      assert page.locator('#academy-count').inner_text()=='7'
     elif section.startswith('academias/'):
      assert page.locator('#academy-profile').count()==1
     if section=='legionarios/':
      assert page.locator('.player-card:visible').count()==18
      page.locator('#player-country').select_option('ES')
      assert page.locator('.player-card:visible').count()==6
      assert page.locator('#player-count').inner_text()=='6'
      assert set(page.locator('.player-card:visible').evaluate_all('(rows) => rows.map(r => r.dataset.name)'))=={p['name'] for p in P if p['country']=='ES'}
      page.locator('#player-position').select_option('df')
      assert page.locator('.player-card:visible').count()==3
      page.locator('#player-name').fill('junior')
      assert page.locator('#player-count').inner_text()=='1'
      page.locator('#player-name').fill('not-a-player')
      assert page.locator('#player-count').inner_text()=='0'
     elif section.startswith('legionarios/'):
      assert page.locator('#player-profile').count()==1
     if section.startswith('liga/') and section!='liga/':
      assert page.locator('#club-facts dt').count()==5
      assert page.locator('#club-facts dd').count()==5
      assert page.locator('iframe').count()==0
     if section=='liga/':
      assert page.locator('[data-club]').count()==8
      assert page.locator('#ldf-champions li').count()==11
     if section=='seleccion/' and page.locator('#national-rows').count():
      total=page.locator('#national-rows tr').count()
      assert total==expected_national
      assert int(page.locator('#stat-9').inner_text())==total
      for field in ['opponent','competition']:
       control=page.locator('#'+field)
       value=control.locator('option').nth(1).get_attribute('value')
       assert value
       control.select_option(value)
       expected=page.locator('#national-rows tr').evaluate_all("(rows, arg) => rows.filter(r => r.dataset[arg.field] === arg.value).length",{'field':field,'value':value})
       assert 0<expected<total
       assert page.locator('#national-rows tr:visible').count()==expected
       assert int(page.locator('#stat-9').inner_text())==expected
       control.select_option('')
       assert int(page.locator('#stat-9').inner_text())==total
      page.locator('#venue').select_option('neutral')
      assert int(page.locator('#stat-9').inner_text())==page.locator('#national-rows tr[data-venue=neutral]').count()
      page.locator('#venue').select_option('')
      page.locator('#from').fill('2099-01-01')
      assert page.locator('#stat-9').inner_text()=='0'
      page.locator('#from').fill('')
      assert int(page.locator('#stat-9').inner_text())==total
   page.locator('#theme').click()
   theme=page.locator('html').get_attribute('data-theme')
   page.reload()
   assert page.locator('html').get_attribute('data-theme')==theme
   assert not errors, errors
   print('Passed viewport:', size, '205 pages and theme persistence')
   page.close()
  browser.close()
 print('Chromium desktop and mobile: passed')
finally:
 server.terminate()
