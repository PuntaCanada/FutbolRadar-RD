import json,html
from pathlib import Path
D=json.loads((Path(__file__).resolve().parents[1]/'data/ldf.json').read_text())
T={
'es':['Temporada','Clubes','Formato','Partidos por club','Partidos de fase regular','Semifinalistas','Ida y vuelta en eliminatorias','Calendario y resultados','Clasificación','Campeones desde 2015','Dónde ver','Canal oficial de la LDF','Datos externos: consulta la fuente. No disponemos de una licencia confirmada para republicar los resultados y las tablas.','Participante de la temporada','Fuentes','Dos torneos independientes, cada uno con fase regular y eliminatorias.','Volver a la liga','No se confirma la emisión de cada partido.'],
'en':['Season','Clubs','Format','Matches per club','Regular phase matches','Semifinalists','Two-legged knockout rounds','Fixtures and results','Standings','Champions since 2015','Where to watch','Official LDF channel','External data: consult the source. We have no confirmed license to republish results or standings.','Season participant','Sources','Two independent tournaments, each with a regular phase and knockouts.','Back to league','Broadcast of individual matches is not confirmed.'],
'de':['Saison','Vereine','Format','Spiele je Verein','Spiele der Ligaphase','Halbfinalisten','K.-o.-Runden mit Hin- und Rückspiel','Spielplan und Ergebnisse','Tabelle','Meister seit 2015','Übertragungen','Offizieller LDF-Kanal','Externe Daten: siehe Quelle. Eine Lizenz zur Wiederveröffentlichung von Ergebnissen und Tabellen ist nicht bestätigt.','Saisonteilnehmer','Quellen','Zwei eigenständige Turniere mit jeweils Ligaphase und K.-o.-Runden.','Zurück zur Liga','Keine bestätigte Übertragung einzelner Spiele.'],
'fr':['Saison','Clubs','Format','Matchs par club','Matchs de phase régulière','Demi-finalistes','Élimination directe aller-retour','Calendrier et résultats','Classement','Champions depuis 2015','Diffusions','Chaîne officielle LDF','Données externes : consultez la source. Aucune licence confirmée pour republier résultats et classements.','Participant de la saison','Sources','Deux tournois indépendants avec phase régulière et élimination directe.','Retour à la ligue','La diffusion de chaque match reste à confirmer.'],
'it':['Stagione','Club','Formato','Partite per club','Partite della fase regolare','Semifinalisti','Eliminazione diretta con andata e ritorno','Calendario e risultati','Classifica','Campioni dal 2015','Trasmissioni','Canale ufficiale LDF','Dati esterni: consultare la fonte. Nessuna licenza confermata per ripubblicare risultati e classifiche.','Partecipante alla stagione','Fonti','Due tornei indipendenti, ciascuno con fase regolare ed eliminazione diretta.','Torna alla lega','La trasmissione delle singole partite non è confermata.']}
FACT_LABELS={
'es':['Ciudad','Estadio documentado','Fundación','Sin confirmar','Títulos de LDF desde 2015','Títulos internacionales documentados','El estadio corresponde a la temporada indicada, no necesariamente al próximo partido.','Las sanciones oficiales pueden modificar los puntos.'],
'en':['City','Documented stadium','Founded','Unconfirmed','LDF titles since 2015','Documented international titles','The stadium refers to the stated season, not necessarily the next match.','Official sanctions may change points.'],
'de':['Heimatort','Dokumentiertes Stadion','Gründung','Nicht bestätigt','LDF-Titel seit 2015','Dokumentierte internationale Titel','Die Stadionangabe gilt für die genannte Saison, nicht zwingend für das nächste Spiel.','Offizielle Sanktionen können den Punktestand verändern.'],
'fr':['Ville','Stade documenté','Fondation','Non confirmé','Titres LDF depuis 2015','Titres internationaux documentés','Le stade correspond à la saison indiquée, pas nécessairement au prochain match.','Les sanctions officielles peuvent modifier les points.'],
'it':['Città','Stadio documentato','Fondazione','Non confermato','Titoli LDF dal 2015','Titoli internazionali documentati','Lo stadio si riferisce alla stagione indicata, non necessariamente alla prossima partita.','Le sanzioni ufficiali possono modificare i punti.']}
def render_ldf(lang,club=None):
 t=T[lang]; e=html.escape; s=D['sources']
 def link(key,label): return '<a href="'+e(s[key],quote=True)+'">'+e(label)+'</a>'
 if club:
  labels=FACT_LABELS[lang]
  slug=next(slug for slug,name in D['clubs'] if name==club)
  fact=D['clubFacts'][slug]
  years=[y for y,name in D['champions'] if name==club]
  values=[fact['city'],fact['stadium']+' ('+D['stadiumReferenceSeason']+')',str(fact.get('founded',labels[3])),str(len(years))+(' · '+', '.join(years) if years else ''),' · '.join(y+' '+name for y,name in fact.get('international',[])) or labels[3]]
  details='<dl id="club-facts">'+''.join('<dt>'+e(label)+'</dt><dd>'+e(value)+'</dd>' for label,value in zip(labels,values))+'</dl><p>'+e(labels[6])+'</p>'
  details+='<h2>'+e(t[14])+'</h2><ul>'+''.join('<li><a href="'+e(url,quote=True)+'">'+e(url.split('/')[2])+' ('+str(i+1)+')</a></li>' for i,url in enumerate(fact['sources']))+'</ul>'
  details+='<p>'+link('champions',t[9])+'</p>'
  return details+ f'<p>{e(t[13])} · {D["season"]}</p><p>{link("format",t[14])}</p><p>{link("fixtures",t[7])} · {link("standings",t[8])}</p><p>{e(t[12])}</p><p><a href="/{lang}/liga/">{e(t[16])}</a></p>'
 clubs=''.join(f'<a data-club="{slug}" href="/{lang}/liga/{slug}/">{e(name)}</a>' for slug,name in D['clubs'])
 winners=''.join(f'<li>{e(y)} — {e(n)}</li>' for y,n in D['champions'])
 return f'<div id="ldf-season"><h2>{e(t[0])} {D["season"]}</h2><p>{e(t[15])}</p><h3>{e(t[2])}</h3><p>Apertura 2026 · Clausura 2027</p><ul><li>{e(t[3])}: {D["regularMatchesPerClub"]}</li><li>{e(t[4])}: {D["regularMatches"]}</li><li>{e(t[5])}: {D["semifinalists"]}</li><li>{e(t[6])}</li></ul><p>{link("format",t[14])} · {link("calendar",t[0])}</p><h2>{e(t[1])}</h2><div class="tiles">{clubs}</div><h2>{e(t[7])}</h2><p>{link("fixtures",t[7])}</p><h2>{e(t[8])}</h2><p>{link("standings",t[8])}</p><p>{e(FACT_LABELS[lang][7])} · {link("sanctions",t[14])}</p><p>{e(t[12])}</p><h2>{e(t[9])}</h2><ol id="ldf-champions">{winners}</ol><p>{link("champions",t[14])} · {link("championOfficial","Fedofútbol")}</p><h2>{e(t[10])}</h2><p>{link("broadcast",t[11])}</p><p>{e(t[17])}</p></div>'
