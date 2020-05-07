from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sqlite3
import hashlib
import dateutil.parser as parser

def sanitize_date(date_text):
    unkown = 'unbekannt'
    if date_text == '':
        return unkown
    if date_text == 'unbekannt':
        return unkown
    if date_text == '?':
        return unkown
    if date_text == 'o.D.':
        return unkown
    if date_text == 'Salinger':
        return unkown
    if date_text == 'o.D. ':
        return unkown
    if date_text == 'Nicht angegeben':
        return unkown


    if date_text == 'Mai 2019':
        date_text = '01.05.2019'
    if date_text == 'Juni 2014, Mai 2016':
        date_text = '01.06.2014'
    if date_text == 'Juni 2019':
        date_text = '01.06.2019'
    if date_text == 'Mai 2018':
        date_text = '01.05.2018'
    if date_text == 'Mai 2016':
        date_text = '01.05.2016'
    if date_text == 'Sommer 2019':
        date_text = '21.06.2019'
    if date_text == 'Herbst 2019':
        date_text = '23.09.2019'
    if date_text == '18.06-15':
        date_text = '18.06.2015'
    if date_text == 'Juli 2019':
        date_text = '01.07.2019'
    if date_text == '004.05.2009':
        date_text = '04.05.2009'
    if date_text == '04.2018':
        date_text = '01.04.2018'
    if date_text == '28.06,16':
        date_text = '28.06.2016'
    if date_text == 'Mai 2015':
        date_text = '01.05.2015'


    try:
        date = parser.parse(date_text,dayfirst=True)
    except:
        print('Cannot convert: ' + date_text)
        # return unkown

    return date


try:
    sqliteConnection = sqlite3.connect('brueter.sqlite')
    cursor = sqliteConnection.cursor()
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

url = "http://www.gebaeudebrueter-in-berlin.de/index.php"

content = urlopen(url + "?find=%25").read()
# content = urlopen(url + "?find=%25&x=0&y=0").read()
soup = BeautifulSoup(content, features="html.parser")

ahref = soup.findAll('a', {'href': True})

index = 0
total = len(ahref)

for link in ahref:

    # if index > 8:
    #     break
    if 'ID' in link['href']:
        m = re.search('[0-9]+', link['href'])
        web_id = m.group(0)
        print("ID = {}, index = {}, total = {}".format(web_id, index, total))
        detailContent = urlopen(url + link['href']).read()
        soup2 = BeautifulSoup(detailContent, features="html.parser")
        table = soup2.findAll('table')
        table2 = table[4]
        td = table2.findChildren('td')
        bezirk = td[1].findChildren('input')[0]['value']
        mauersegler = 1 if td[2].findChildren('input', checked=True) else 0
        kontrolle = 1 if td[3].findChildren('input', checked=True) else 0
        plz = td[5].findChildren('input')[0]['value']
        sperling = 1 if td[6].findChildren('input', checked=True) else 0
        ersatz = 1 if td[7].findChildren('input', checked=True) else 0
        ort = td[9].findChildren('input')[0]['value']
        schwalbe = 1 if td[10].findChildren('input', checked=True) else 0
        wichtig = 1 if td[11].findChildren('input', checked=True) else 0
        strasse = td[13].findChildren('input')[0]['value']
        star = 1 if td[14].findChildren('input', checked=True) else 0
        sanierung = 1 if td[15].findChildren('input', checked=True) else 0
        anhang = td[17].findChildren('input')[0]['value']
        fledermaus = 1 if td[18].findChildren('input', checked=True) else 0
        verloren = 1 if td[19].findChildren('input', checked=True) else 0
        erstbeobachtung = td[21].findChildren('input')[0]['value']
        erstbeobachtung = sanitize_date(erstbeobachtung)
        andere = 1 if td[22].findChildren('input', checked=True) else 0
        table2 = table[5]
        td = table2.findChildren('td')
        beschreibung = td[1].findChildren('textarea')[0].text
        besonderes = td[3].findChildren('textarea')[0].text
        payload = (f'{web_id}{bezirk}{plz}{ort}{strasse}{anhang}{erstbeobachtung}{beschreibung}{besonderes}{mauersegler}'
                   f'{kontrolle}{sperling}{ersatz}{schwalbe}{wichtig}{star}{sanierung}{fledermaus}{verloren}{andere}')
        checksum = hashlib.sha3_224(payload.encode('utf-8')).hexdigest()
        cursor.execute('SELECT checksum from gebaeudebrueter where web_id=?', (web_id,))
        data = cursor.fetchall()
        if len(data) == 0:
            value = (web_id, bezirk, plz, ort, strasse, anhang, erstbeobachtung, beschreibung, besonderes, checksum,
                     mauersegler, kontrolle, sperling, ersatz, schwalbe, wichtig, star, sanierung, fledermaus,
                     verloren, andere)
            query = ('INSERT INTO gebaeudebrueter'
                         '(web_id, bezirk, plz, ort, strasse, anhang, erstbeobachtung, beschreibung, besonderes,'
                         'checksum, update_date, mauersegler, kontrolle, sperling, ersatz, schwalbe, wichtig,'
                         'star, sanierung, fledermaus, verloren, andere)'
                         'VALUES (?,?,?,?,?,?,?,?,?,?,DATETIME(\'now\'),?,?,?,?,?,?,?,?,?,?,?)')
            cursor.execute(query,value)
            sqliteConnection.commit()
            print('added')
        else:
            pass
    index += 1

if (sqliteConnection):
    sqliteConnection.close()
