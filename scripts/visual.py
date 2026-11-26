from pathlib import Path
import subprocess,time
from playwright.sync_api import sync_playwright
out=Path('visual-review');out.mkdir(exist_ok=True)
server=subprocess.Popen(['python3','-m','http.server','8766','--bind','127.0.0.1','--directory','public'])
try:
 time.sleep(2)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for device,size in [('desktop',{'width':1440,'height':1000}),('mobile',{'width':390,'height':844})]:
   for theme in ['light','dark']:
    page=browser.new_page(viewport=size,color_scheme=theme)
    for name,path in [('home',''),('national','seleccion/'),('league','liga/'),('players','legionarios/'),('profile','legionarios/junior-firpo/'),('academies','academias/'),('women','femenino/'),('sponsorship','patrocinio/')]:
     response=page.goto('http://127.0.0.1:8766/es/'+path)
     assert response.ok
     page.evaluate("(theme)=>document.documentElement.dataset.theme=theme",theme)
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
     page.screenshot(path=str(out/f'{device}-{theme}-{name}.png'),animations='disabled')
    page.close()
  browser.close()
 print('32 actual Chromium screenshots captured')
finally:
 server.terminate()
