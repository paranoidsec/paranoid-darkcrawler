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
