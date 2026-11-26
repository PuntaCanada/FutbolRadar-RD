import html
from pathlib import Path
import json
D=json.loads((Path(__file__).resolve().parents[1]/'data/women.json').read_text())
L={
'es':['Fútbol femenino','Clasificación mundialista Brasil 2027','Fecha del informe','Rival','Resultado RD','Fuente','Segundo lugar: 8 puntos; invicta, pero eliminada.','Formación y competiciones juveniles','Clubes juveniles documentados; no implica inscripción pública.'],
'en':['Women’s football','Brazil 2027 World Cup qualifying','Report date','Opponent','DR score','Source','Second place: 8 points; unbeaten but eliminated.','Youth competitions and development','Documented youth clubs; public enrolment is not implied.'],
'de':['Frauenfußball','WM-Qualifikation Brasilien 2027','Berichtsdatum','Gegner','Ergebnis RD','Quelle','Zweiter Platz: 8 Punkte; ungeschlagen, aber ausgeschieden.','Nachwuchswettbewerbe und Talentförderung','Dokumentierte Nachwuchsvereine; öffentliche Anmeldung nicht bestätigt.'],
'fr':['Football féminin','Qualifications au Mondial Brésil 2027','Date du rapport','Adversaire','Score RD','Source','Deuxième : 8 points ; invaincue mais éliminée.','Compétitions et formation des jeunes','Clubs de jeunes documentés ; inscription publique non confirmée.'],
'it':['Calcio femminile','Qualificazioni al Mondiale Brasile 2027','Data del resoconto','Avversario','Risultato RD','Fonte','Secondo posto: 8 punti; imbattuta ma eliminata.','Competizioni e sviluppo giovanile','Club giovanili documentati; iscrizione pubblica non confermata.']}
def render_women(lang):
 t=L[lang];e=html.escape
 def link(url):return '<a href="'+e(url,quote=True)+'">'+e(t[5])+'</a>'
 rows=''.join('<tr><td>'+e(m['report'])+'</td><td>'+e(m['opponent'][lang])+'</td><td>'+str(m['gf'])+':'+str(m['ga'])+'</td><td>'+link(m['source'])+'</td></tr>' for m in D['matches'])
 youth=''.join('<article><h3>'+e(x['title'][lang])+'</h3><p>'+e(x['text'][lang])+'</p><p>'+e(x['date'])+' · '+link(x['source'])+'</p></article>' for x in D['youth'])
 return '<div id="women-football"><h2>'+e(t[1])+'</h2><p>'+e(t[6])+' '+link(D['matches'][-1]['source'])+'</p><div style="overflow-x:auto"><table><thead><tr>'+''.join('<th scope="col">'+e(v)+'</th>' for v in t[2:6])+'</tr></thead><tbody id="women-results">'+rows+'</tbody></table></div><h2>'+e(t[7])+'</h2>'+youth+'<p>'+e(t[8])+'</p></div>'
