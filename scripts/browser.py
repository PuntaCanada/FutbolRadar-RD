import subprocess,time
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
    for section in ['', 'seleccion/','liga/','academias/','fuentes/','patrocinio/']:
     response=page.goto('http://127.0.0.1:8765/'+lang+'/'+section)
     assert response.ok
     assert page.locator('html').get_attribute('lang')==lang
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (size, page.url)
     if section=='seleccion/' and page.locator('#national-rows').count():
      total=page.locator('#national-rows tr').count()
      assert total==164
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
   print('Passed viewport:', size, '30 pages and theme persistence')
   page.close()
  browser.close()
 print('Chromium desktop and mobile: passed')
finally:
 server.terminate()
