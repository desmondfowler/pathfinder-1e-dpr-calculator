import os
import requests
from bs4 import BeautifulSoup

USE_MYTHIC_MONSTERS = True

# AoN urls for all monsters, npcs, and mythic monsters
MYTHIC_PRD_URLS = ["https://www.aonprd.com/Monsters.aspx?Letter=All", 
           "https://www.aonprd.com/NPCs.aspx?SubGroup=All", 
           "https://www.aonprd.com/MythicMonsters.aspx?Letter=All"]
NORMAL_PRD_URLS = ["https://www.aonprd.com/Monsters.aspx?Letter=All", 
           "https://www.aonprd.com/NPCs.aspx?SubGroup=All"]

if USE_MYTHIC_MONSTERS:
    prdUrls = MYTHIC_PRD_URLS
else :
    prdUrls = NORMAL_PRD_URLS
# Create monsters directory if it doesn't exist

if not os.path.exists("enemies"):
    os.makedirs("enemies")

# Output file
outfile = "enemies/enemy_pages.txt"

# Enemies list
allEnemies = []

# Download each page's HTML
for url in prdUrls:
    try:
        enemies = []
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        tableElements = soup.select("#main table tr td:first-child a")
        for element in tableElements:
            href = element.get("href")
            if href.startswith("https://aonprd.com/"):
                input("found one")
                enemy = "" + href
            else :
                enemy = "https://aonprd.com/" + href
            with open(outfile, "w") as f:
                f.write(enemy + '\n')
            
    except requests.exceptions.RequestException as e:
        print(url)
        print(type(e).__name__ + ": " + str(e))
    
# Now, to encode the URLs and allow them to be actually loaded

