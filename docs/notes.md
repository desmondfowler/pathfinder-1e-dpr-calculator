# Pathfinder 1e DPR Calculator Notes

This is my running thought dump for the project. I want the README to be clean and quick, and this file to be the “why” and “where I’m going.”

Other DPR calculators exist, but they always felt a little hand‑wavy to me. I want something grounded in real monster stats.

Right now the project is a Python data pipeline + a tiny web stub. The scraper worked last time I checked, aggregation is still basic, and the UI is a placeholder while I develop the data side first.

Things I care about:

- Keep the data pipeline repeatable so I can refresh when AoNPRD changes.
- Aggregate by CR in a way that’s actually useful (averages, percentiles, maybe ranges).
- Make the eventual UI clean and not bloated.
- Use Python for the heavy data work

Loose next steps:

- Break the scraper into smaller pieces (fetch, parse, IO, config).
- Decide what stats to compute for each CR (AC, HP, saves, maybe attack bonuses).
- Build a simple API layer once the data model is stable.
- Sketch UI flows for “single build DPR” and “level progression DPR.”

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
