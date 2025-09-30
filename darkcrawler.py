#!/usr/bin/env python3

import os
import requests
import argparse
from datetime import datetime

# Global variables
## session through TOR
session = requests.session()
session.proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}
## Results folder
results_folder="results"

def test_tor_connection(timeout=15):
    # Test if the Tor SOCKS5 proxy is working.
    try:
        r = session.get('http://check.torproject.org', timeout=timeout)
        if "Congratulations" in r.text:
            print("[+] Connected through Tor successfully!")
            return True
        else:
            print("[!] Connected, but Tor test page did not confirm.")
            return False
    except Exception as e:
        print(f"[!] Tor connection failed: {e}")
        return False

def fetch_page(url, out_file, timeout=30):
    # Fetch a single page via TOR and save HTML to a file.
    try:
        print(f"[*] Fetching {url}...")
        r = session.get(url, timeout=timeout)
        path = os.path.join(results_folder, out_file)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f"[+] Saved page to {path}")
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paranoid DarkCrawler")
    parser.add_argument("--check-tor", action="store_true", help="Check Tor connectivity and exit")
    parser.add_argument("--target", help="URL to fetch (default: Tor check page)")
    parser.add_argument("--out", default=f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        help="Output file for fetched page")
    args = parser.parse_args()

    print("=== Paranoid DarkCrawler ===")

    if args.check_tor:
        test_tor_connection()
    elif args.target:
        # Check if the results folder exits
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        if test_tor_connection():
            fetch_page(args.target, args.out)
        else:
            print("[!] Aborting fetch due to Tor failure.")
    else:
        parser.print_help()
