import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import time
from tqdm import tqdm
import re

# Limit requests to AoNPRD so we don't blow them up
MAX_REQUESTS = 10
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

if not os.path.isdir("enemies"):
    print("Error: 'enemies' is not a directory")
    exit(1)

# Enemies list
enemyURLs = []

# Download each page's HTML
for url in prdUrls:
    try:
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        tableElements = soup.select("#main table tr td:first-child a")
        
        for i, element in enumerate(tableElements):
            href = element.get("href")
            encoded = quote(href, safe='=?/()')

            enemy = urljoin("https://aonprd.com/", encoded)
            
            enemyURLs.append(enemy)

            
    except requests.exceptions.RequestException as e:
        print(url)
        print(type(e).__name__ + ": " + str(e))
        
# Write to output file
try:
    with open("enemies/enemy_pages.json", "w") as f:
        json.dump(enemyURLs, f)
except OSError:
    print("Error: Failed to write to file 'enemies/enemy_pages.json'")
    exit(1)

# Start of scraping individual monster html files
enemiesByCR = {}
#testing number:
LOOPS = 500

for i, url in enumerate(tqdm(enemyURLs)):
    t = time.time()
    try:
        html = requests.get(url).text
    except requests.exceptions.RequestException as e:
        print(url)
        print(type(e).__name__ + ": " + str(e))
    tSpent = time.time() - t
    if tSpent < 1 / MAX_REQUESTS:
        time.sleep(1 / MAX_REQUESTS - tSpent)
    
    # Clean up HTML
    regex = r'(?:\r\n|\r|\xad|' + chr(10) + ')+'
    html = re.sub(r'(\s+)' + regex + r'|' + regex + r'(?=\s+)', r'\1', html) 
    html = re.sub(regex, r' ', html) 
    html = re.sub(r'(<br/?)\s*/?>', r'\1>', html) # Fix broken <br> tags
    html = re.sub(r'[−—–‐‑‒―]|&ndash;|&mdash;', "-", html) 

    #Parse the html using soup
    soup = BeautifulSoup(html, 'html.parser')
    
    #Find the monster's title tag which houses the name and CR value
    monsterTitleTag = soup.find('h2', {'class': 'title'})
    
    # Extract the text
    monsterTitle = monsterTitleTag.text
    
    # Extract the CR value from the text
    crMatch = re.search(r'CR\s+(\d+(/(\d+))?|\d+)', monsterTitle)
    if crMatch:
        cr = crMatch.group(0)
    else:
        cr = None
    
    # Extract additional monster attributes
    monsterAttrs = {}
    
    
    # Add the monster to the dictionary for its CR
    if cr is not None:
        if cr not in enemiesByCR:
            enemiesByCR[cr] = []
        enemiesByCR[cr].append(monsterTitle)
        


    # Write to output json file
    try:
        with open("enemies/enemy_info.json", "w") as f:
            json.dump(enemiesByCR, f)
    except OSError:
        print("Error: Failed to write to file 'enemies/enemy_info.json'")
        exit(1)
    
    # For testing, amount of loops:
    # if i >= LOOPS:
    #     print("Hit " + str(LOOPS) + " loops, exiting")
    #     exit()