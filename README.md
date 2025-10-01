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

Fetch a single page through TOR and save the results to a file:

```bash
python3 darkcrawler.py --target http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/ --out results.json --csv
```

**Note**: You must have TOR running locally with the default SOCKS5 proxy `127.0.0.1:9050`

See [CHANGELOG](CHANGELOG.md) for recent updates.
