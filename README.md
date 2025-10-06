# Paranoid DarkCrawler

Paranoid DarkCrawler is a professional-oriented crawler designed for research and monitoring of darkweb content via the Tor network.

⚠️ **Disclaimer:** This tool is for authorized security research only.
Do not use it to access, download, or interact with illegal content.
All demos and examples are sanitized.

---

## Features (planned)

- Crawl darkweb sites through Tor (SOCKS5 proxy).
- Configurable depth and rate limits.
- Extract basic metadata (links, email-like strings, headers).
- Export results to JSON/CSV for analysis.

---

## Quickstart

Install the repository:

```bash
# Clone the repository
git clone https://github.com/paranoidsec/paranoid-darkcrawler.git
# Install dependencies
cd paranoid-darkcrawler
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Run a tor connectivity check:

```bash
python3 darkcrawler.py --check-tor
```

Fetch a single, or multiple pages through TOR and save the results to a file:

```bash
# Fetch a single page
python3 darkcrawler.py --target http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/ --out results.json --csv

# Start an unbounded crawl but save state every step
python3 darkcrawler.py --target http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion --depth -1 --max-pages -1 --delay 3 --state-file state.json

# Resume later (restarts where it stopped)
python3 darkcrawler.py --target http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion --depth -1 --max-pages -1 --delay 3 --state-file state.json

# Domain discovery mode
python3 darkcrawler.py --target http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion --mode domains
# Domain discovery mode and write to csv
python3 darkcrawler.py --target http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion --mode domains --csv
```

```

**Note**: You must have TOR running locally with the default SOCKS5 proxy `127.0.0.1:9050`

### CLI Flags

| Flag          | Description                               | Default |
|---------------|-------------------------------------------|---------|
| --check-tor   | Test Tor connectivity and exit             | —       |
| --target      | URL to start crawling                      | —       |
| --out         | Output JSON filename                       | page_<timestamp>.json |
| --csv         | Also export CSV alongside JSON             | off     |
| --depth       | Crawl depth (0 = only target, -1 = unlimited) | 0 |
| --max-pages   | Max pages to fetch (-1 = unlimited)        | 50 |
| --delay       | Delay between requests (sec)               | 2 |
| --max-runtime | Max runtime (minutes, -1 = unlimited)      | -1 |
| --state-file  | Save/load crawl state for resume           | none |
| --mode        | Discover more domains while crawling       | content |


## Example output (sanitized)

```json
[
  {
    "url": "http://exampleonion.onion",
    "title": "Example Onion Site",
    "description": "Sample description",
    "emails": ["contact@example.onion"],
    "links": [
      "http://exampleonion.onion/login",
      "http://exampleonion.onion/about"
    ]
  }
]
```

See [CHANGELOG](CHANGELOG.md) for recent updates.
