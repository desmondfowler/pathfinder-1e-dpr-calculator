import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

# Change the below flag to True if you want to consider mythic monsters.
# By default, it is False, since mythic monsters 
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
try:
    if not os.path.exists("enemies"):
        os.makedirs("enemies")
except OSError:
    print("Error: Failed to create directory 'enemies'")
    exit(1)

# Enemies list
allEnemies = []

# Download each page's HTML
for url in prdUrls:
    try:
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        tableElements = soup.select("#main table tr td:first-child a")
        
        for element in tableElements:
            
            href = element.get("href")
            encoded = quote(href, safe='=?/()')

            enemy = urljoin("https://aonprd.com/", encoded)
            
            allEnemies.append(enemy)

            
    except requests.exceptions.RequestException as e:
        print(url)
        print(type(e).__name__ + ": " + str(e))

# Sort and remove duplicates
allEnemies = list(set(allEnemies))
allEnemies = sorted(allEnemies)

# Write to output file
try:
    with open("enemies/enemy_pages.txt", "w") as f:
        f.write("\n".join(allEnemies))
except OSError:
    print("Error: Failed to write to file 'enemies/enemy_pages.txt'")
    exit(1)
