import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import folium
import numpy as np

df = pd.read_csv('nabupage_longlat.csv', encoding='utf8')

map1 = folium.Map(
    location=[52.5163,13.3777],
    tiles='cartodbpositron',
    zoom_start=12
)

for index, row in df.iterrows():
    color = 'beige'
    fund = 'Unbekannt'
    if row['Mauersegler']:
        color='blue'
        fund = 'Mauersegler'
    if row['Sperling']:
        color='green'
        fund = 'Sperling'
    if row['Schwalbe']:
        color='darkpurple'
        fund = 'Schwalbe'
    if row['Fledermaus']:
        color = 'black'
        fund = 'Fledermaus'
    if row['Star']:
        color = 'gray'
        fund = 'Star'
    if row['Andere']:
        color = 'pink'
        fund = 'Was anderes'
    icon = folium.Icon(color=color)
    if np.isnan(row['latitude']):
        continue
    if np.isnan(row['longitude']):
        continue
    popup = folium.Popup('<b>Fund: <b>' + fund + '<br/><br/><b>Adresse</b><br/>' + str(row['ADDRESS']) +
                                         '<br/><br/><b>Beschreibung</b><br/>' + str(row['Beschreibung']) +
                                         '<br/><br/><b>Erstbeobachtung</b><br/>' + str(row['Erstbeobachtung']) +
                                         '<br/><br/><b>Besonderes</b><br/>' + str(row['Besonderes']) +
                                         '<br/><br/><b>ID</b><br/>' + str(row['ID'])
                         ,max_width=450)
    folium.Marker(location=[row["latitude"], row["longitude"]],popup=popup,tooltip=fund,icon=icon).add_to(map1)

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

map1.save('GebaeudebrueterBerlin.html')


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
