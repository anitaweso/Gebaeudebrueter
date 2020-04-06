import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import folium
import numpy as np
from folium import plugins

df = pd.read_csv('nabupage_longlat.csv', encoding='utf8')

map1 = folium.Map(
    location=[52.5163,13.3777],
    tiles=None,
    zoom_start=12
)
folium.TileLayer('cartodbpositron', name='Maßnahme').add_to(map1)

marker_cluster = plugins.MarkerCluster(control=False)
map1.add_child(marker_cluster)
ersatz = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Ersatz')
keinersatz = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'kein Ersatz')
# sperling = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Sperling')
# schwalbe = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Schwalbe')
# fledermaus = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Fledermaus')
# star = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Star')
# andere = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Andere')

map1.add_child(ersatz)
map1.add_child(keinersatz)
# map1.add_child(sperling)
# map1.add_child(schwalbe)
# map1.add_child(fledermaus)
# map1.add_child(star)
# map1.add_child(andere)

positions = []
popups = []
colors = []
url = 'http://www.gebaeudebrueter-in-berlin.de/index.php'
for index, row in df.iterrows():
    if row['ID'] in (1214, 1598):
        continue
    color = 'orange'
    fund = 'andere Art'
    grp = keinersatz
    if row['Mauersegler']:
        color='blue'
        fund = 'Mauersegler'
    if row['Sperling']:
        color='green'
        fund = 'Sperling'
    if row['Schwalbe']:
        color='purple'
        fund = 'Schwalbe'
    if row['Fledermaus']:
        color = 'black'
        fund = 'Fledermaus'
    if row['Star']:
        color = 'darkred'
        fund = 'Star'
    if row['Ersatz']:
        grp = ersatz

    icon = folium.Icon(color=color)
    if np.isnan(row['latitude']):
        continue
    if np.isnan(row['longitude']):
        continue

    if row['Ersatz']:
        ersatztxt = 'Hier wurden Ersatzmaßnahmen errichtet'
    else:
        ersatztxt = 'Ersatzmaßnahmen nicht vorhanden'

    if row['Sanierung']:
        sanierung = 'Hier hat eine Sanierung stattgefunden'
    else:
        sanierung = 'Bisher hat keine Sanierung stattgefunden'

    besonderes  = 'Kein Eintrag' if str(row['Besonderes']) == 'nan' else row['Besonderes']

    popup = folium.Popup('<b>Fund: </b>' + fund + '<br/><br/><b>Adresse</b><br/>' + str(row['Strasse']) + ', ' + str(row['PLZ']) + ' ' + str(row['Ort']) +
                         '<br/><br/><b>Erstbeobachtung: </b>' + str(row['Erstbeobachtung']) +
                         '<br/><br/><b>Beschreibung</b><br/>' + str(row['Beschreibung']) +
                         '<br/><br/><b>Besonderes</b><br/>' + str(besonderes) +
                         '<br/><br/><b>Ersatz: </b>' + ersatztxt +
                         '<br/><br/><b>Sanierung: </b>' + sanierung +
                         '<br/><br/><b>Link zur Datenbank</b><br/><a href=' + url + '?ID=' + str(row['ID']) + '>' + str(row['ID']) + '</a>'
                         , max_width=450)

    folium.Marker(location=[row['latitude'], row['longitude']], popup=popup, tooltip=fund, icon=icon).add_to(grp)
    # folium.Marker(location=[row['latitude'], row['longitude']]).add_to(grp)

folium.LayerControl(collapsed=False, ).add_to(map1)

map1.save('GebaeudebrueterBerlinByErsatz.html')


