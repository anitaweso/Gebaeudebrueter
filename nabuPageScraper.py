from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd
import re
import openpyxl

url = "http://www.gebaeudebrueter-in-berlin.de/index.php"

content = urlopen(url + "?find=%25&x=0&y=0").read()
soup = BeautifulSoup(content, features="html.parser")

ahref = soup.findAll('a', {'href':True})
# print(ahref)

df = pd.DataFrame(columns=['ID','Bezirk','Mauersegler','Kontrolle','PLZ','Sperling',
                   'Ersatz','Ort','Schwalbe','Wichtig','Strasse','Star',
                   'Sanierung','Anhang','Fledermaus','Verloren','Erstbeobachtung',
                   'Andere','Melder','Beschreibung','Besonderes'])
# df = pd.DataFrame()
index=0
total = len(ahref)
for link in ahref:
    # if i>8:
    #     break
    if 'ID' in link['href']:
        m = re.search('[0-9]+',link['href'])
        id = m.group(0)
        print("ID = {}, index = {}, total = {}".format(id, index, total))
        detailContent = urlopen(url + link['href']).read()
        # detailContent = urlopen(url + '?ID=1451').read()
        soup2 = BeautifulSoup(detailContent, features="html.parser")
        table = soup2.findAll('table')
        table2 = table[4]
        td = table2.findChildren('td')
        bezirk = td[1].findChildren('input')[0]['value']
        mauersegler = 1 if td[2].findChildren('input',checked=True) else 0
        kontrolle = 1 if td[3].findChildren('input',checked=True) else 0
        plz = td[5].findChildren('input')[0]['value']
        sperling = 1 if td[6].findChildren('input',checked=True) else 0
        ersatz = 1 if td[7].findChildren('input',checked=True) else 0
        ort = td[9].findChildren('input')[0]['value']
        schwalbe = 1 if td[10].findChildren('input',checked=True) else 0
        wichtig = 1 if td[11].findChildren('input',checked=True) else 0
        strasse = td[13].findChildren('input')[0]['value']
        star = 1 if td[14].findChildren('input',checked=True) else 0
        sanierung = 1 if td[15].findChildren('input',checked=True) else 0
        anhang = td[17].findChildren('input')[0]['value']
        fledermaus = 1 if td[18].findChildren('input',checked=True) else 0
        verloren = 1 if td[19].findChildren('input',checked=True) else 0
        erstbeobachtung = td[21].findChildren('input')[0]['value']
        andere = 1 if td[22].findChildren('input',checked=True) else 0
        melder = td[24].findChildren('input')[0]['value']
        table2 = table[5]
        td = table2.findChildren('td')
        beschreibung = td[1].findChildren('textarea')[0].text
        besonderes = td[3].findChildren('textarea')[0].text
        row_df = pd.DataFrame({'ID':id,'Bezirk':bezirk,'Mauersegler':mauersegler,
                               'Kontrolle':kontrolle,'PLZ':plz,'Sperling':sperling,
                               'Ersatz':ersatz,'Ort':ort,'Schwalbe':schwalbe,'Wichtig':wichtig,
                               'Strasse':strasse,'Star':star,'Sanierung':sanierung,'Anhang':anhang,
                               'Fledermaus':fledermaus,'Verloren':verloren,'Erstbeobachtung':erstbeobachtung,
                               'Andere':andere,'Melder':melder,'Beschreibung':beschreibung,'Besonderes':besonderes},index=[0])
        df = pd.concat([row_df,df])
        # print(td)
        # print(td[4])
    index+=1

# print(df)
df.to_csv('nabupage.csv', index=False, header=True)
df.to_excel('nabupage.xlsx', index=False)