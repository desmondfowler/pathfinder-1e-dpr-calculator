# Pathfinder 1e DPR Calculator

This project is intended for users to calculate their DPR (damage per round) for the Pathfinder first edition (1e) Roleplaying Game. This may help them in planning out better optimized characters, or, if you're like me, it may just be fun to play around with the data. It involves a Python script that scrapes data on in-game enemies (monsters, NPCs, excluding mythic monsters) from the Archives of Nethys website (aonprd.com) and aggregates that data based on the monsters' CR (challenge rating). It then uses that aggregated data to inform a DPR calculator app, where the user inputs their character stats and receives detailed output on their expected DPR.

Many people have created tools like this in the past, but they all seemed to be missing something in my mind. I couldn't quite put my finger on it, so I decided to try and make my own. First, a little background information.

## Important Note

Keep in mind the project is not finished. I may complete it when I have more free time, but as of today's date (July 28th, 2023) the only section that is complete is the `data_scraper.py` file, and the beginnings of an aggregate.py file where I was going to do some basic analysis of the monsters. It currently does not do this, it only prints out the dictionary. My plans were, as described in the above paragraph, to group the monsters by their 'CR' field, then do analysis on various different stats they have. For example, what the average AC was, so we could use that to calculate (also not implemented) a characters average performance vs different challenges. I also have the start of a typescript file to host the app in browser (I was going to use this project to learn typescript instead of basic JS), but it is not written either. If you're curious, you can run `npm install` to install the required packages (not many) and then `npm start` to launch the webpage, but it's an empty one with "Hello World" on it. 

## Challenge Ratings

Monsters in the Pathfinder RPG can have a wide range of challenge ratings, from as low as 1/8 to as high as 30 or more. The following is a list of possible CR values for monsters at the time of writing:

| Range           | CR  | CR  | CR  | CR  | CR  | CR  |
| --------------- | --- | --- | --- | --- | --- | --- |
| CR - to CR 1/2  | -   | 1/8 | 1/6 | 1/4 | 1/3 | 1/2 |
| CR 1 to CR 6    | 1   | 2   | 3   | 4   | 5   | 6   |
| CR 7 to CR 12   | 7   | 8   | 9   | 10  | 11  | 12  |
| CR 13 to CR 18  | 13  | 14  | 15  | 16  | 17  | 18  |
| CR 19 to CR 24  | 19  | 20  | 21  | 22  | 23  | 24  |
| CR 25 to CR 30+ | 25  | 26  | 27  | 28  | 29  | 30+ |

## First Time Setup

There is some first-time setup to use the calculator. This involves downloading the scraped data and aggregating it into JSON files that the app uses. This process need only be done once, unless you want to re-download the files, or if at any time AoN adds new monsters. I currently don't have a way to check which URLs have already been downloaded, but I plan to implement a comparison based on the `enemy_pages.json` url list file.

### Dependencies

This script requires the following dependencies:

- add dependencies as I write the code here (currently none)

You can install these dependencies using pip, like so:

```bash
pip install -r requirements.txt
```

### Data Scraping

To start the data scraping script, simply run `data_scraper.py` from the command line, like so:

```bash
python data_scraper.py
```

This will scrape the pages of monsters from the Archives of Nethys website and store it in a text file called `monster_pages.txt`. The script then parses this text file to scrape the URL of each individual monster, as each monster has its own webpage. The URLs are iterated through, and the HTML of each page is fetched, parsed, and the important information is stored in a JSON file names `monster_data.json`.

Next, this `monster_data.json` file is used to aggregate monsters based on their CR, or "Challenge Rating." This aggregated data will be pulled into a separate JSON file for each CR. For example, `cr-.json` will contain all "CR -" entries, and `cr21.json` will contain all "CR 21" entries pulled from AoNPRD. This is done by running the `aggregate.py` script like so:

```bash
python aggregate.py
```

## Main Usage

After all the data has been aggregated into the respective JSON files, you can start to use the calculator. I need to develop the above before I develop the app, but once I do that, I will fill out how to use it, along with what to expect.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. We welcome contributions of all kinds, including bug fixes, new features, and documentation improvements.

## License

This project is released under the Apache License 2.0. See the [LICENSE](./LICENSE) file for more information.

## Terms and Conditions

Please see the [LICENSE](./LICENSE) file for the full terms and conditions of use, reproduction, and distribution. Some key points are summarized below:

- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- No Warranty: The software is provided "as is", without warranty of any kind.
- Redistribution: You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications, provided that certain conditions are met.
- Use of Trademark: This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work and reproducing the content of the NOTICE file.

For more information, please see the full [LICENSE](./LICENSE) file.
