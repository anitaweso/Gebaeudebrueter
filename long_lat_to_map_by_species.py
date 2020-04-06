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
folium.TileLayer('cartodbpositron', name='Art').add_to(map1)

marker_cluster = plugins.MarkerCluster(control=False)
map1.add_child(marker_cluster)
mauersegler = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Mauersegler')
sperling = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Sperling')
schwalbe = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Schwalbe')
fledermaus = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Fledermaus')
star = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Star')
andere = folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Andere')

map1.add_child(mauersegler)
map1.add_child(sperling)
map1.add_child(schwalbe)
map1.add_child(fledermaus)
map1.add_child(star)
map1.add_child(andere)

positions = []
popups = []
colors = []
url = 'http://www.gebaeudebrueter-in-berlin.de/index.php'
for index, row in df.iterrows():
    if row['ID'] in (1214, 1598):
        continue
    color = 'orange'
    fund = 'andere Art'
    grp = andere
    if row['Mauersegler']:
        color='blue'
        fund = 'Mauersegler'
        grp = mauersegler
    if row['Sperling']:
        color='green'
        fund = 'Sperling'
        grp = sperling
    if row['Schwalbe']:
        color='purple'
        fund = 'Schwalbe'
        grp = schwalbe
    if row['Fledermaus']:
        color = 'black'
        fund = 'Fledermaus'
        grp = fledermaus
    if row['Star']:
        color = 'darkred'
        fund = 'Star'
        grp = star
    # if row['Andere']:
    #     color = 'orange'
    #     fund = 'andere Art'
    #     grp = andere
    icon = folium.Icon(color=color)
    if np.isnan(row['latitude']):
        continue
    if np.isnan(row['longitude']):
        continue

    if row['Ersatz']:
        ersatz = 'Hier wurden Ersatzmaßnahmen errichtet'
    else:
        ersatz = 'Ersatzmaßnahmen nicht vorhanden'

    if row['Sanierung']:
        sanierung = 'Hier hat eine Sanierung stattgefunden'
    else:
        sanierung = 'Bisher hat keine Sanierung stattgefunden'

    besonderes  = 'Kein Eintrag' if str(row['Besonderes']) == 'nan' else row['Besonderes']

    popup = folium.Popup('<b>Fund: </b>' + fund + '<br/><br/><b>Adresse</b><br/>' + str(row['Strasse']) + ', ' + str(row['PLZ']) + ' ' + str(row['Ort']) +
                         '<br/><br/><b>Erstbeobachtung: </b>' + str(row['Erstbeobachtung']) +
                         '<br/><br/><b>Beschreibung</b><br/>' + str(row['Beschreibung']) +
                         '<br/><br/><b>Besonderes</b><br/>' + str(besonderes) +
                         '<br/><br/><b>Ersatz: </b>' + ersatz +
                         '<br/><br/><b>Sanierung: </b>' + sanierung +
                         '<br/><br/><b>Link zur Datenbank</b><br/><a href=' + url + '?ID=' + str(row['ID']) + '>' + str(row['ID']) + '</a>'
                         , max_width=450)

    folium.Marker(location=[row["latitude"], row["longitude"]], popup=popup, tooltip=fund, icon=icon).add_to(grp)


folium.LayerControl(collapsed=False, ).add_to(map1)

    # popups.append(popup)
    # positions.append((row["latitude"], row["longitude"]))
    # colors.append(color)


# plugins.MarkerCluster(positions, popups=popups, color=colors).add_to(map1)

    # folium.Marker(location=[row["latitude"], row["longitude"]],popup=popup,tooltip=fund,icon=icon).add_to(map1)

# df['latitude'] = df['latitude'].replace(np.nan,52.4739285)
# df['longitude'] = df['longitude'].replace(np.nan,13.4553784)
# df.apply(lambda row:folium.Marker(location=[row["latitude"], row["longitude"]],
#                                   popup= folium.Popup('<b>Adresse</b><br/>' + str(row['ADDRESS']) +
#                                          '<br/><br/><b>Meldung</b><br/>' + str(row['Beschreibung']) +
#                                          '<br/><br/><b>Datum der Meldung</b><br/>' + str(row['Erstbeobachtung']) +
#                                          '<br/><br/><b>Besonderes</b><br/>' + str(row['Besonderes']) +
#                                          '<br/><br/><b>Melder</b><br/>' + str(row['Melder'])
#                                          ,max_width=450 ),
#                                   tooltip='Details').add_to(map1), axis=1)

#fg = folium.FeatureGroup(name='fund')
#map1.add_child(fg)

#g1 = plugins.FeatureGroupSubGroup(fg, 'Mauersegler')
#map1.add_child(g1)

#g2 = plugins.FeatureGroupSubGroup(fg, 'Sperling')
#map1.add_child(g2)

#g3 = plugins.FeatureGroupSubGroup(fg, 'Schwalbe')
#map1.add_child(g3)

#folium.Marker([-1, -1]).add_to(g1)
#folium.Marker([1, 1]).add_to(g1)

#folium.Marker([-1, 1]).add_to(g2)
#folium.Marker([1, -1]).add_to(g2)

#folium.LayerControl(collapsed=False).add_to(map1)

map1.save('GebaeudebrueterBerlinBySpecies.html')


# print("Latitude = {}, Longitude = {}".format(dflatitude, location.longitude))
# print(df['latitude'](0))
# 1 - conveneint function to delay between geocoding calls
# geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# 2- - create location column
# df['location'] = df['ADDRESS'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
# df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# 4 - split point column into latitude, longitude and altitude columns
# df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
