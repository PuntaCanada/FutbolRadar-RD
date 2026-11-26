import subprocess,time
from playwright.sync_api import sync_playwright
server=subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1','--directory','public'])
try:
 time.sleep(2)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for size in [{'width':1280,'height':800},{'width':390,'height':844}]:
   page=browser.new_page(viewport=size,color_scheme='light')
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   for lang in ['es','en','de','fr','it']:
    for section in ['', 'seleccion/','liga/','academias/','fuentes/','patrocinio/']:
     response=page.goto('http://127.0.0.1:8765/'+lang+'/'+section)
     assert response.ok
     assert page.locator('html').get_attribute('lang')==lang
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
   page.locator('#theme').click()
   theme=page.locator('html').get_attribute('data-theme')
   page.reload()
   assert page.locator('html').get_attribute('data-theme')==theme
   assert not errors, errors
   page.close()
  browser.close()
 print('Chromium desktop and mobile: passed')
finally:
 server.terminate()
