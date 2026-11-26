import json,html
from pathlib import Path
D=json.loads((Path(__file__).resolve().parents[1]/'data/academies.json').read_text())
A=D['academies']
REGIONS={'dn':'Distrito Nacional','la':'La Altagracia','st':'Santiago','lr':'La Romana'}
L={
'es':['Provincia o distrito','Todas','Edad (años)','Por confirmar','Contacto oficial','Sitio oficial','Fuentes','Fecha de consulta','Volver al listado','Confirma las condiciones y plazas directamente con la academia.','Correo','Teléfono'],
'en':['Province or district','All','Age (years)','Unconfirmed','Official contact','Official website','Sources','Checked on','Back to directory','Confirm conditions and availability directly with the academy.','Email','Phone'],
'de':['Provinz oder Distrikt','Alle','Alter (Jahre)','Nicht bestätigt','Offizieller Kontakt','Offizielle Website','Quellen','Quellenstand','Zurück zur Übersicht','Bedingungen und freie Plätze direkt bei der Akademie erfragen.','E-Mail','Telefon'],
'fr':['Province ou district','Tous','Âge (ans)','Non confirmé','Contact officiel','Site officiel','Sources','Date de consultation','Retour à la liste','Confirmez les conditions et les places auprès de l’académie.','Courriel','Téléphone'],
'it':['Provincia o distretto','Tutti','Età (anni)','Non confermato','Contatto ufficiale','Sito ufficiale','Fonti','Data di consultazione','Torna alla lista','Verificare condizioni e disponibilità direttamente con l’accademia.','Email','Telefono']}
def render_academies(lang,academy=None):
 t=L[lang];e=html.escape
 def link(url,label):return '<a href="'+e(url,quote=True)+'">'+e(label)+'</a>'
 def facts(a):
  return '<p>'+e(a['city'])+' · '+e(REGIONS[a['region']])+'</p><p>'+e(t[2])+': '+e(a['ages'] or t[3])+'</p>'
 if academy:
  a=academy
  contact='<p>'+link(a['website'],t[5])+' · '+link(a['contact'],t[4])+'</p>'
  if a.get('email'):contact+='<p>'+e(t[10])+': '+link('mailto:'+a['email'],a['email'])+'</p>'
  if a.get('phone'):contact+='<p>'+e(t[11])+': '+link('tel:'+a['phone'].replace(' ',''),a['phone'])+'</p>'
  return '<div id="academy-profile">'+facts(a)+contact+'<h2>'+e(t[6])+'</h2><ul>'+''.join('<li>'+link(u,u.split('/')[2])+'</li>' for u in a['sources'])+'</ul><p>'+e(t[7])+': '+e(D['checked'])+'</p><p>'+e(t[9])+'</p>'+link('/'+lang+'/academias/',t[8])+'</div>'
 options='<option value="">'+e(t[1])+'</option>'+''.join('<option value="'+k+'">'+e(v)+'</option>' for k,v in REGIONS.items())
 cards=''.join('<article class="academy-card" data-region="'+a['region']+'"><h3>'+link('/'+lang+'/academias/'+a['id']+'/',a['name'])+'</h3>'+facts(a)+'</article>' for a in A)
 return '<p>'+e(t[9])+'</p><label>'+e(t[0])+' <select id="academy-region">'+options+'</select></label><p><output id="academy-count" aria-live="polite">'+str(len(A))+'</output></p><div class="player-grid">'+cards+'</div><script defer src="/academies.js"></script>'
