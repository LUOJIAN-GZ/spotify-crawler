import datetime
# 打印当前时间
time1 = datetime.datetime.now()
print(time1)
from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
from datetime import date, timedelta
region={'united states': 'us', 'united kingdom': 'gb', 'united arab emirates': 'ae', 'argentina': 'ar', 'austria': 'at', 'australia': 'au', 'belgium': 'be', 'bulgaria': 'bg', 'bolivia': 'bo', 'brazil': 'br', 'canada': 'ca', 'switzerland': 'ch', 'chile': 'cl', 'colombia': 'co', 'costa rica': 'cr', 'cyprus': 'cy', 'czech republic': 'cz', 'germany': 'de', 'denmark': 'dk', 'dominican republic': 'do', 'ecuador': 'ec', 'estonia': 'ee', 'egypt': 'eg', 'spain': 'es', 'finland': 'fi', 'france': 'fr', 'greece': 'gr', 'guatemala': 'gt', 'hong kong': 'hk', 'honduras': 'hn', 'hungary': 'hu', 'indonesia': 'id', 'ireland': 'ie', 'israel': 'il', 'india': 'in', 'iceland': 'is', 'italy': 'it', 'japan': 'jp', 'korea, republic of': 'kr', 'lithuania': 'lt', 'luxembourg': 'lu', 'latvia': 'lv', 'morocco': 'ma', 'mexico': 'mx', 'malaysia': 'my', 'nicaragua': 'ni', 'netherlands': 'nl', 'norway': 'no', 'new zealand': 'nz', 'panama': 'pa', 'peru': 'pe', 'philippines': 'ph', 'poland': 'pl', 'portugal': 'pt', 'paraguay': 'py', 'romania': 'ro', 'russian federation': 'ru', 'saudi arabia': 'sa', 'sweden': 'se',
        #'singapore': 'sg',
'slovakia': 'sk', 'el salvador': 'sv', 'thailand': 'th', 'turkey': 'tr', 'taiwan': 'tw', 'ukraine': 'ua', 'uruguay': 'uy', 'viet nam': 'vn', 'south africa': 'za'}

# create empty arrays for data we're collecting
dates = []
url_list = []
final = []
url_list_dic={}
# map site

start_date = date(2017, 1, 1)
end_date = date(2022, 2, 5)

delta = end_date - start_date

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    day_string = day.strftime("%Y-%m-%d")
    dates.append(day_string)


def add_url():
    for cty in region:
        url = f"https://spotifycharts.com/regional/{region[cty]}/daily/"
        url_list_dic[cty]=[]
        for date in dates:
            c_string = url + date
            #url_list.append(c_string)
            url_list_dic[cty].append(c_string)


add_url()


# function for going through each row in each url and finding relevant song info

def song_scrape(x,day):
    pg = x
    for tr in songs.find("tbody").findAll("tr"):
        rank=tr.find("td", {"class": "chart-table-position"}).text
        artist = tr.find("td", {"class": "chart-table-track"}).find("span").text
        artist = artist.replace("by ", "").strip()
        artist=artist.replace('\"','')
        title = tr.find("td", {"class": "chart-table-track"}).find("strong").text
        title = title.replace('"', '')
        songid = tr.find("td", {"class": "chart-table-image"}).find("a").get("href")
        songid = songid.split("track/")[1]
        STREAMS=tr.find("td", {"class": "chart-table-streams"}).text
        STREAMS = STREAMS.replace('\"', '')

        RANK_DATE=dates[day]
        url_date = x.split("daily/")[1]

        final.append([rank,title, artist, songid, url_date,STREAMS,RANK_DATE])


# loop through urls to create array of all of our song info
from selenium import webdriver
driver = webdriver.Chrome('chromedriver.exe')
print(f'Logging in...')
driver.maximize_window()
# driver.get('https://spotifycharts.com/regional/sg/weekly/2022-01-21--2022-01-28/')
# html = driver.execute_script("return document.documentElement.outerHTML")
# print(html)


for k,o in url_list_dic.items():
    file_name=k
    i = 0
    j = 0
    day = 0
    for u in o:
        if i>30:
            i=0
            j+=1
            print(f'已爬取{j}月')
            final_df = pd.DataFrame(final, columns=["RANK", "Title", "Artist", "Song ID", "Chart Date", "STREAMS","RANK_DATE"])
            final = []
            with open(f"{file_name}.csv", "a+", newline='', encoding='utf-8-sig') as csvfile:
                final_df.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig', mode='a')
        try:
            read_pg = driver.get(u)
            read_pg_text=driver.execute_script("return document.documentElement.outerHTML")
            #sleep(2)
            soup = BeautifulSoup(read_pg_text, "html.parser")
            songs = soup.find("table", {"class": "chart-table"})
            #print(songs)
            song_scrape(u,day)
            day+=1
            i+=1
        except:
            day+=1
            continue
    final_df = pd.DataFrame(final, columns=["RANK", "Title", "Artist", "Song ID", "Chart Date", "STREAMS","RANK_DATE"])
    final = []
    with open(f"{file_name}.csv", "a+", newline='', encoding='utf-8-sig') as csvfile:
        final_df.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig', mode='a')


time1 = datetime.datetime.now()
print(time1)
driver.quit()

import pandas as pd
pd.Panel()
