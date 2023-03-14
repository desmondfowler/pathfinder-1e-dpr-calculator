# This script scrapes monster data from the Pathfinder Roleplaying Game
# website (aonprd.com). It uses the BeautifulSoup and requests libraries
# to parse HTML and make HTTP requests, and the tqdm library to display
# a progress bar. Assumptions: the website structure and content will
# not change, and the script will be run on a machine with internet
# access and Python 3.x installed.

import json
import logging
import os
import re
import sys
import time
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Limit requests to AoNPRD so we don't blow them up
MAX_REQUEST_RATE = 5
# Number of monsters to iterate through - for testing
NUM_MONSTERS_TO_SCRAPE = 5
# Change the below flag to True if you want to consider mythic monsters.
# By default, it is False, since mythic monsters tend to be outliers
USE_MYTHIC_MONSTERS = True
DATA_PATH = "data"
ENEMY_PAGES_FILE = "data/enemy_pages.json"
ENEMY_INFO_FILE = "data/enemy_info.json"

logging.basicConfig(filename='scrape.log', level=logging.DEBUG)
# AoN urls for all monsters, npcs
PRD_URLS = ["https://www.aonprd.com/Monsters.aspx?Letter=All",
            "https://www.aonprd.com/NPCs.aspx?SubGroup=All"]


def writeToJson(filename: str, data: dict) -> None:
    """
    Writes a dictionary to a JSON file.

    :param filename: the filename to write to
    :param data: the dictionary to write
    :raises ValueError: if filename is empty or None
    """
    if not filename:
        raise ValueError("filename must not be empty or None")

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        logging.error(
            f"Failed to write to file '{filename}'\nError: {str(e)}")
        raise


def addMythicUrls(urls: list[str], includeMythic: bool):
    """
    Adds the URL for mythic monsters to the list of URLs if 'include_mythic'
    is True.

    Args:
        urls (list[str]): A list of URLs.
        include_mythic (bool): A flag indicating whether mythic monsters
        should be included.

    Returns:
        list[str]: The updated list of URLs.
    """
    if includeMythic:
        urls.append("https://www.aonprd.com/MythicMonsters.aspx?Letter=All")
    return urls


def createDirectories():
    """
    Creates the 'data' directory if it doesn't exist, and exits the
    program with an error message if it can't be created or if it
    exists but is not a directory.
    """
    try:
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
    except OSError as e:
        logging.error(f"Failed to create directory 'data'\nError: {str(e)}")
        sys.exit(1)

    if not os.path.isdir(DATA_PATH):
        logging.error("Error: 'data' is not a directory")
        sys.exit(1)


def createEnemyURLs(urlList: list):
    """
    Creates a list of URLs for enemy pages to scrape by parsing the main
    pages of the PRD website.

    :param urlList: a list of URLs for the main pages of the PRD website
    :return: a list of URLs for enemy pages to scrape
    """
    enemyURLs = []

    if os.path.isfile(ENEMY_PAGES_FILE):
        print("Are you sure you want to scrape again?")
        print("This will take time.")
        print("It is not required if you already have the data.\n")
        confirmation = input("y/n")

        if confirmation.strip() != "y":
            sys.exit(1)
        logging.info(
            "URL List found, skipping creation of URL list.")
        with open(os.path.abspath(ENEMY_PAGES_FILE), "r") as f:
            print(f"Contents of file: {f.read()}")
            f.seek(0)  # Reset file pointer to beginning of file
            enemyURLs = json.load(f)
    else:
        logging.info(
            "No URL list found, proceeding to create URL list.")
        for url in urlList:
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
                logging.error(f"Failed to scrape URL: {url}\nError: {str(e)}")
                sys.exit(1)
        # Write to output file
        writeToJson(ENEMY_PAGES_FILE, enemyURLs)
    return enemyURLs


def cleanUpHTML(htmlText: str):
    # Clean up HTML
    htmlText = re.sub(r'\s+', ' ', htmlText.replace('\xad', '').
                      replace('&ndash;', '-').replace('&mdash;', '-'))
    htmlText = re.sub(r'<br/?\s*/?>', '<br/>', htmlText)
    htmlText = re.sub(r'<(/)?b>', '', htmlText)
    return htmlText


def getMonsterAttributes(soup: BeautifulSoup, attributeDict: dict, name: str):
    for h3 in soup.find_all('h3', {'class': 'framing'}):
        if h3.text.startswith('Defense'):
            acMatch = re.search(r'AC\s+(\d+)', h3.next_sibling)
            touchMatch = re.search(r'touch.*?(\d+)', h3.next_sibling)
            ffMatch = re.search(r'flat-footed.*?(\d+)', h3.next_sibling)
            hpTag = h3.next_sibling.next_sibling.next_sibling
            if hpTag.name == 'br':
                hpTag = hpTag.next_sibling
            hpMatch = re.search(r'\s*(\d+)\s*', hpTag)
            if acMatch:
                if "AC" in attributeDict:
                    attributeDict["AC"] = int(acMatch.group(1))
            else:
                logging.error(
                    f'Error: Failed to extract AC value of {name}')
            if touchMatch:
                if "Touch" in attributeDict:
                    attributeDict["Touch"] = int(touchMatch.group(1))
            else:
                logging.error(
                    f'Error: Failed to extract Touch AC value of {name}')
            if ffMatch:
                if "Flat-footed" in attributeDict:
                    attributeDict["Flat-footed"] = int(ffMatch.group(1))
            else:
                logging.error(
                    f'Error: Failed to extract Flat-foot AC value of {name}')
            if hpMatch:
                if "HP" in attributeDict:
                    attributeDict["HP"] = int(hpMatch.group(1))
            else:
                logging.error(
                    f'Error: Failed to extract HP value of {name}')
            break
    return attributeDict


def monsterDataScraper(urlList: list, amount: int = None):
    """
    Scrapes data for each enemy page in `urlList`, extracting the
    monster's name, CR, and attributes (AC, Touch, Flat-footed, and HP).

    :param urlList: a list of URLs for enemy pages to scrape
    :param amount: the amount of monsters to scrape
    :return: a dictionary mapping CR values to a list of enemy dictionaries,
    each containing a name and attributes
    """
    if amount is None:
        amount = len(urlList)
    logging.info("Beginning scrape of individual monster pages.")
    # Start of scraping individual monster html files
    enemiesByCR = {}
    for i, url in enumerate(tqdm(urlList[:amount])):
        # Initializing monster attributes dict
        monsterAttrs = {"CR": 0,
                        "AC": 0,
                        "Touch": 0,
                        "Flat-footed": 0,
                        "HP": 0}
        currentTime = time.time()
        try:
            htmlText = requests.get(url).text
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to scrape URL: {url}\nError: {str(e)}")
            next
        timeSpent = time.time() - currentTime
        if timeSpent < 1 / MAX_REQUEST_RATE:
            time.sleep(1 / MAX_REQUEST_RATE - timeSpent)

        htmlText = cleanUpHTML(htmlText)
        # Parse the html using soup
        soup = BeautifulSoup(htmlText, 'html.parser')
        # Find the monster's title tag which houses the name and CR value
        monsterTitleTag = soup.find('h2', {'class': 'title'})
        # Extract the text
        monsterTitle = monsterTitleTag.text
        # Extract the CR value from the text
        crMatch = re.search(r'CR\s+(\d+(/(\d+))?|\d+)', monsterTitle)
        crNumberMatch = re.search(r"\d+(?:/\d+)?", monsterTitle)

        if crMatch:
            cr = crMatch.group(0)
            # Extract the monster name from the text
            monsterNameMatch = re.search(r'^(.*?)CR', monsterTitle)
            if monsterNameMatch:
                monsterName = monsterNameMatch.group(1).strip()
            else:
                monsterName = None
        else:
            cr = None
            monsterName = None

        # Extract the CR number value
        if crNumberMatch:
            crNumber = crNumberMatch.group()
            if "/" in crNumber:
                crNumber = float(eval(crNumber))
            else:
                crNumber = float(crNumber)
            monsterAttrs['CR'] = crNumber
        else:
            logging.error(
                f'Error: Failed to extract CR value of {monsterName}')
        # Get AC values and HP value
        monsterAttrs = getMonsterAttributes(soup, monsterAttrs, monsterName)
        # Add the monster to the dictionary for its CR
        if cr is not None:
            if cr not in enemiesByCR:
                enemiesByCR[cr] = []
            enemiesByCR[cr].append({monsterName: monsterAttrs})

        # Write to the json so that you get some data even if it times out
        writeToJson(ENEMY_INFO_FILE, enemiesByCR)
    return enemiesByCR


if __name__ == "__main__":
    PRD_URLS = addMythicUrls(PRD_URLS, USE_MYTHIC_MONSTERS)
    createDirectories()
    enemyURLs = createEnemyURLs(PRD_URLS)
    enemiesByCR = monsterDataScraper(enemyURLs, NUM_MONSTERS_TO_SCRAPE)
    logging.info(f"Done scraping {str(NUM_MONSTERS_TO_SCRAPE)} monsters.")
