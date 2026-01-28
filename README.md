# Pathfinder 1e DPR Calculator

A work in progress tool for analyzing Pathfinder 1e DPR (damage per round). It includes a Python data pipeline for scraping and aggregating monster stats and a simple web server stub for the eventual UI.

## Status

The data scraper is functional, aggregation is early, and the web UI is currently a placeholder while the data pipeline matures.

## Project Layout

- `src/python/pathfinder_dpr` - core Python package (scraper and analysis)
- `src/python/cli` - CLI entrypoints for repeatable data jobs
- `src/web` - web server stub (future UI)
- `data/` - generated data artifacts (gitignored)

## Data Pipeline

1. Scrape monster/NPC pages from AoNPRD
2. Normalize and aggregate data by CR
3. Use aggregated stats to inform DPR calculations in the app

## Local Usage

Web server:

```bash
npm install
npm start
```

Python data jobs (example):

```bash
PYTHONPATH=src/python python -m cli.scrape
```

## Docs

- `docs/instructions.md` - how to run the scraper and pipeline jobs
- `docs/notes.md` - project notes, design thoughts, and next steps

## License

MIT

## Legal

Pathfinder is a registered trademark of Paizo Inc.
This project is a fan-made tool and is not affiliated with or endorsed by Paizo.
