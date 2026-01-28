# Instructions

## First Time Setup

The data pipeline is a two-step process: scrape AoNPRD pages into JSON, then aggregate the results by CR. You only need to re-run the scraper if AoNPRD adds or updates monsters. There is currently no built-in diffing, so a rescrape will replace existing data.

## Data Scraping

Run the scraper via the CLI entrypoint:

```bash
PYTHONPATH=src/python python -m cli.scrape
```

Output files:
- `data/enemy_pages.json` (source URLs)
- `data/enemy_info.json` (raw scraped monster data)

## Aggregation

Run the aggregation step via the CLI entrypoint:

```bash
PYTHONPATH=src/python python -m cli.aggregate
```

The aggregation module currently reads `data/enemy_info.json` and prints the aggregated dictionary. More detailed analysis output will be added as the pipeline evolves.

## Main Usage

Once the data pipeline is in place, the aggregated stats will feed into the web app’s DPR calculations. The UI is still a stub, so the current focus is the data pipeline.
