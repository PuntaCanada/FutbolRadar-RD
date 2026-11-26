import json,html
from pathlib import Path
D=json.loads((Path(__file__).resolve().parents[1]/'data/legionarios.json').read_text())
P=D['players']
CAREERS=json.loads((Path(__file__).resolve().parents[1]/'data/player-careers.json').read_text())
CAREER_LABELS={'es':'Trayectoria documentada','en':'Documented career','de':'Dokumentierte Karriere','fr':'Parcours documenté','it':'Carriera documentata'}
L={
'es':['Legionarios dominicanos','Nombre','País','Posición','Todos','Portero','Defensa','Centrocampista','Delantero','Club documentado','Fecha de referencia','Fuente','Competición documentada','Sin confirmar','Volver al listado','La afiliación corresponde a la fecha indicada; no es un registro de traspasos en directo.'],
'en':['Dominicans abroad','Name','Country','Position','All','Goalkeeper','Defender','Midfielder','Forward','Documented club','Reference date','Source','Documented competition','Unconfirmed','Back to list','Club affiliation refers to the stated date, not a live transfer register.'],
'de':['Dominikaner im Ausland','Name','Land','Position','Alle','Tor','Abwehr','Mittelfeld','Angriff','Dokumentierter Verein','Bezugsdatum','Quelle','Dokumentierter Wettbewerb','Nicht bestätigt','Zurück zur Übersicht','Die Vereinszugehörigkeit gilt zum angegebenen Datum; keine Live-Transferdaten.'],
'fr':['Dominicains à l’étranger','Nom','Pays','Poste','Tous','Gardien','Défenseur','Milieu','Attaquant','Club documenté','Date de référence','Source','Compétition documentée','Non confirmé','Retour à la liste','Le club correspond à la date indiquée ; pas de registre des transferts en direct.'],
'it':['Dominicani all’estero','Nome','Paese','Ruolo','Tutti','Portiere','Difensore','Centrocampista','Attaccante','Club documentato','Data di riferimento','Fonte','Competizione documentata','Non confermato','Torna alla lista','Il club si riferisce alla data indicata; non è un registro dei trasferimenti in tempo reale.']}
C={'US':['Estados Unidos','United States','USA','États-Unis','Stati Uniti'],'ES':['España','Spain','Spanien','Espagne','Spagna'],'CY':['Chipre','Cyprus','Zypern','Chypre','Cipro'],'NL':['Países Bajos','Netherlands','Niederlande','Pays-Bas','Paesi Bassi'],'PT':['Portugal']*5,'BO':['Bolivia','Bolivia','Bolivien','Bolivie','Bolivia'],'PL':['Polonia','Poland','Polen','Pologne','Polonia'],'RU':['Rusia','Russia','Russland','Russie','Russia'],'MD':['Moldavia','Moldova','Moldau','Moldavie','Moldavia'],'UY':['Uruguay']*5}
def render_players(lang,player=None):
 t=L[lang]; e=html.escape; idx=list(L).index(lang)
 def country(p): return C[p['country']][idx]
 def pos(p): return t[5+['gk','df','mf','fw'].index(p['position'])]
 def facts(p):
  src=D['sources'][p['source']]
  return '<dl>'+''.join('<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>' for k,v in [(t[9],p['club']),(t[2],country(p)),(t[3],pos(p)),(t[10],src['date']),(t[12],p['competition'] or t[13])])+'</dl><p><a href="'+e(src['url'],quote=True)+'">'+e(t[11])+'</a></p>'
 if player:
  career=CAREERS['profiles'].get(player['id'])
  extra=''
  if career:
   extra='<section id="player-career"><h2>'+e(CAREER_LABELS[lang])+'</h2><p>'+e(career['text'][lang])+'</p><p>'+e(t[10])+': '+e(CAREERS['checked'])+'</p><ul>'+''.join('<li><a href="'+e(url,quote=True)+'">'+e(t[11])+' '+str(i+1)+'</a></li>' for i,url in enumerate(career['sources']))+'</ul></section>'
  return '<div id="player-profile">'+facts(player)+extra+'<p>'+e(t[15])+'</p><a href="/'+lang+'/legionarios/">'+e(t[14])+'</a></div>'
 def options(items): return '<option value="">'+e(t[4])+'</option>'+''.join('<option value="'+e(k)+'">'+e(v)+'</option>' for k,v in items)
 filters='<div class="national-filters"><label>'+e(t[1])+'<input id="player-name" type="search"></label><label>'+e(t[2])+'<select id="player-country">'+options([(k,C[k][idx]) for k in sorted({p['country'] for p in P})])+'</select></label><label>'+e(t[3])+'<select id="player-position">'+options(list(zip(['gk','df','mf','fw'],t[5:9])))+'</select></label></div>'
 cards=''.join(f'<article class="player-card" data-name="{e(p["name"],quote=True)}" data-country="{p["country"]}" data-position="{p["position"]}"><h3><a href="/{lang}/legionarios/{p["id"]}/">{e(p["name"])}</a></h3>{facts(p)}</article>' for p in P)
 return '<p>'+e(t[15])+'</p>'+filters+'<output id="player-count" aria-live="polite">'+str(len(P))+'</output><div class="player-grid">'+cards+'</div><script defer src="/players.js"></script>'
