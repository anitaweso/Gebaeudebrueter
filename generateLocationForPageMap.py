import geopandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import folium
from geopy.exc import GeocoderTimedOut
from tqdm import tqdm

df = pd.read_file('nabupage.csv', encoding='utf8')

locator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# df = df[1:10]
plz = df['PLZ'].copy()
df['ADDRESS'] = df['Strasse'].str.cat(plz, sep=', ')
df['ADDRESS'] = df['ADDRESS'].str.cat(['Berlin, Deutschland'] * len(df['ADDRESS']), sep=', ')
tqdm.pandas()
df['location'] = df['ADDRESS'].progress_apply(geocode,timeout=10)
df['point'] = df['location'].progress_apply(lambda loc: tuple(loc.point) if loc else (None,None,None))
df[['latitude', 'longitude', 'altitude']] = pd.GeoDataFrame(df['point'].tolist(), index=df.index)

df.to_csv('nabupage_longlat.csv', index=False, header=True)
df.to_excel('nabupage_longlat.xlsx', index=False)


#
#
# map1 = folium.Map(
#     location=[52.5163,13.3777],
#     tiles='cartodbpositron',
#     zoom_start=12,
# )
#
# df.apply(lambda row:folium.Marker(location=[row["lat"], row["long"]],
#                                   popup= folium.Popup('<b>Adresse</b><br/>' + str(row['Straße']) + ', ' + str(row['Bezirk']) +
#                                          '<br/><br/><b>Meldung</b><br/>' + row['Meldung'] +
#                                          '<br/><br/><b>Datum der Meldung</b><br/>' + row['Datum der Meldung'] +
#                                          '<br/><br/><b>Bemerkung</b><br/>' + row['Bemerkung'] +
#                                          '<br/><br/><b>Melder</b><br/>' + row['Melder'] +
#                                          '<br/><br/><b>Melderangaben</b><br/>' + row['Melderangaben'] +
#                                          '<br/><br/><b>Kontrollangaben</b><br/>' + row['Kontrollangaben'] +
#                                          '<br/><br/><b>Kontrollperson</b><br/>' + row['Kontrollperson']
#                                                      ,max_width=450 ) ,
#                                   tooltip='Details').add_to(map1), axis=1)
#
#
# map1.save('GebaeudebrueterMeldungen.html')


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
