import csv
from bs4 import BeautifulSoup
import requests
import time


START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
headers = ["Brown dwarf", "Constellation", "Right ascension", "Declination", "App. mag.", "Distance (ly)", "Spectral type", "Mass (Mj)," "Radius (Rj)", "Discovery year"]

dwarf_stars = []

page = requests.get(START_URL)

soup = BeautifulSoup(page.content, "html.parser")

def scrape_table(table):
    table_on = table.find_all("tr", attrs={"align": "left", "valign": "top"})[0]
    table_on = str(table_on.find_all("strong")[0]).replace("\r", " ").split(" ")[0].split(">")[1]
    for tr_tag in table.find_all("tr", attrs={"align": "center", "valign": "center"}):
        temp_list = []
        for index, td_tag in enumerate(tr_tag.find_all("td")):
            if index == 0:
                try:
                    temp_list.append(
                        td_tag.find_all("a")[0].contents[0]
                    )
                except:
                    try:
                        temp_list.append(td_tag.find_all("strong")[0].contents[0])
                    except:
                        temp_list.append(td_tag.contents[0])
            else:
                temp_list.append(td_tag.contents[0])
        temp_list.append(table_on)
        dwarf_stars.append(temp_list)


for index, table in enumerate(soup.find_all("table")):
    if index == 0:
        continue
    else:
        scrape_table(table)

with open("main.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(dwarf_stars)