## [v0.1.1] - 2025-09-29

### Added

- Initial Tor connectivity check built into the main CLI.
  - Verifies if Tor SOCKS5 proxy is running before starting crawl.

## [v0.1.2] - 2025-09-30

### Added

- CLI flags: `--check-tor`, `--target`, `--out`
- Basic single-page fetch via Tor and save to file

## [v0.2.0] - 2025-10-01

### Added

- Metadata extraction: title, description, links, email-like strings
- JSON export (default) and optional CSV export (--csv)

## [v0.3.2] - 2025-10-02

### Added

- `--depth` option: crawl depth on the same target
- `--delay` option: delay between requests
- `--max-pages` option: maximum pages to crawl
- `--max-runtime` option: define the maximum runtime for the crawler
- `--state-file` option: save progress and resume long/unbounded crawls safely

## [v0.4.0] - 2025-10-04

### Added

- New `--mode domains` to collect hostnames/domains while crawling

## [v0.5.0] - 2025-10-07

### Added

- `--threads` option to fetch multiple pages in parallel (default=1)
- `--mode both` to fetch new domains with their metadata

## [v0.5.0] - 2025-10-17

### Issues

Known issue: memory usage on continuous crawls
