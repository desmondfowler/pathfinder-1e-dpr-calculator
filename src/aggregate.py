import json


# Limit requests to AoNPRD so we don't blow them up
# Number of monsters to iterate through - for testing
# Change the below flag to True if you want to consider mythic monsters.
# By default, it is False, since mythic monsters tend to be outliers
MAX_REQUESTS_PER_SECOND = 5
NUM_TEST_LOOPS = 100
USE_MYTHIC_MONSTERS = False
ENEMY_PAGES_FILE = "enemies/enemy_pages.json"
ENEMY_INFO_FILE = "enemies/enemy_info.json"


with open(ENEMY_INFO_FILE, "r") as f:
    enemyDict = json.load(f)

print(enemyDict)
