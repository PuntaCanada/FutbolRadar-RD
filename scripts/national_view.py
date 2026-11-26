import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LABELS={
'es':['Rival','Competición','Desde','Hasta','Lugar','Todos','Local','Visitante','Neutral','Partidos','Victorias','Empates','Derrotas','Goles a favor','Goles en contra','% victorias','Fecha','Resultado','Penaltis ganados','Penaltis perdidos','Los resultados incluyen prórroga, no penaltis. Los empates por penaltis cuentan como empates. Archivo no necesariamente completo.'],
'en':['Opponent','Competition','From','To','Venue','All','Home','Away','Neutral','Matches','Wins','Draws','Losses','Goals for','Goals against','Win rate','Date','Score','Shootouts won','Shootouts lost','Scores include extra time, not shootouts. Shootout draws count as draws. Archive may be incomplete.'],
'de':['Gegner','Wettbewerb','Von','Bis','Spielort','Alle','Heim','Auswärts','Neutral','Spiele','Siege','Unentschieden','Niederlagen','Tore','Gegentore','Siegquote','Datum','Ergebnis','Elfmeterschießen gewonnen','Elfmeterschießen verloren','Ergebnisse inklusive Verlängerung, ohne Elfmeterschießen. Spiele mit Elfmeterschießen zählen als Remis. Archiv möglicherweise unvollständig.'],
'fr':['Adversaire','Compétition','Du','Au','Lieu','Tous','Domicile','Extérieur','Neutre','Matchs','Victoires','Nuls','Défaites','Buts pour','Buts contre','Taux de victoires','Date','Score','Tirs au but gagnés','Tirs au but perdus','Scores avec prolongation, sans tirs au but. Les matchs décidés aux tirs au but restent des nuls. Archives potentiellement incomplètes.'],
'it':['Avversario','Competizione','Dal','Al','Sede','Tutti','Casa','Trasferta','Neutro','Partite','Vittorie','Pareggi','Sconfitte','Gol fatti','Gol subiti','Percentuale vittorie','Data','Risultato','Rigori vinti','Rigori persi','Risultati con supplementari, senza rigori. Le partite decise ai rigori contano come pareggi. Archivio potenzialmente incompleto.']}
def render(lang):
 p=json.loads((ROOT/'data/national.json').read_text())
 if not isinstance(p,dict): return None
 assert p['license']=='CC0-1.0' and p['matches']
 t=LABELS[lang]; e=html.escape
 def options(values): return '<option value="">'+e(t[5])+'</option>'+''.join('<option value="'+e(x,quote=True)+'">'+e(x)+'</option>' for x in sorted(values))
 m=p['matches']
 filters=f'<label>{e(t[0])}<select id="opponent">{options(set(x["opponent"] for x in m))}</select></label><label>{e(t[1])}<select id="competition">{options(set(x["competition"] for x in m))}</select></label>'
 for id,i in [('from',2),('to',3)]: filters+=f'<label>{e(t[i])}<input id="{id}" type="date"></label>'
 filters+=f'<label>{e(t[4])}<select id="venue"><option value="">{e(t[5])}</option>'+''.join(f'<option value="{v}">{e(t[i])}</option>' for v,i in [('home',6),('away',7),('neutral',8)])+'</select></label>'
 cards=''.join(f'<div><span>{e(t[i])}</span><strong id="stat-{i}">—</strong></div>' for i in [9,10,11,12,13,14,15,18,19])
 rows=''.join(f'<tr data-date="{e(x["date"])}" data-opponent="{e(x["opponent"],quote=True)}" data-competition="{e(x["competition"],quote=True)}" data-venue="{x["venue"]}" data-gf="{x["gf"]}" data-ga="{x["ga"]}" data-shootout="{x["shootout"] or ""}"><td>{e(x["date"])}</td><td>{e(x["opponent"])}</td><td>{e(x["competition"])}</td><td>{e(t[{"home":6,"away":7,"neutral":8}[x["venue"]]])}</td><td>{x["gf"]}:{x["ga"]}'+(f' · {e(t[18 if x["shootout"]=="win" else 19])}' if x["shootout"] else '')+'</td></tr>' for x in reversed(m))
 heads=''.join(f'<th scope="col">{e(t[i])}</th>' for i in [16,0,1,4,17])
 return f'<p>{e(t[20])}</p><p>CC0 1.0 · <a href="{e(p["source"])}/tree/{e(p["revision"])}">International Results</a> · {len(m)} · {m[0]["date"]} – {m[-1]["date"]}</p><div class="national-filters">{filters}</div><div class="national-stats" aria-live="polite">{cards}</div><div class="national-table" tabindex="0"><table><thead><tr>{heads}</tr></thead><tbody id="national-rows">{rows}</tbody></table></div><script defer src="/national.js"></script>'
