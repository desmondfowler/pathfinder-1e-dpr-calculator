import json

ENEMY_PAGES_FILE = "data/enemy_pages.json"
ENEMY_INFO_FILE = "data/enemy_info.json"


with open(ENEMY_INFO_FILE, "r") as f:
    enemyDict = json.load(f)

print(enemyDict)
