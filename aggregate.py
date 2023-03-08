import os
import requests
import time
from tqdm import tqdm

# Limit requests to AoNPRD so we don't blow them up
MAX_REQUESTS = 1

urls = []

with open("enemies/enemy_pages.txt") as f:
    for entry in f:
        urls.append(entry.strip())

if not os.path.exists("enemies"):
    print("Error: Failed to find directory 'enemies'")
    exit(1)


for i, url in enumerate(tqdm(urls[:5])):
    t = time.time()
    try:
        html = requests.get(url).text
    except requests.exceptions.RequestException as e:
        print(url)
        print(type(e).__name__ + ": " + str(e))
    tSpent = time.time() - t
    
    with open(os.path.join("enemies/", str(i) + '.html'), 'w', encoding='utf-8') as fp:
        fp.write(html)
        
    if tSpent < 1 / MAX_REQUESTS:
        time.sleep(1 / MAX_REQUESTS - tSpent)