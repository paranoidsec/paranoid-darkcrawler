#!/usr/bin/env python3

import os, re, csv, json, argparse, requests
from datetime import datetime
from bs4 import BeautifulSoup

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

# Get the content of a webpage
def fetch_page(url, out_file, timeout=30):
    # Fetch a single page via TOR and save HTML to a file.
    try:
        print(f"[*] Fetching {url}...")
        r = session.get(url, timeout=timeout)
        path = os.path.join(results_folder, out_file)

        # Extract the metadata from the html content
        metadata = extract_metadata(r.text, url)
        save_results([metadata], path, csv_mode=args.csv)
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")

# Extract metadata from the webpage html code
def extract_metadata(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else ""
    desc = ""
    if soup.find("meta", attrs={"name": "description"}):
        desc = soup.find("meta", attrs={"name": "description"})["content"]

    links = [a.get("href") for a in soup.find_all("a", href=True)]
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)
    return {
        "url": url,
        "title": title,
        "description": desc,
        "links": links,
        "emails": emails
    }

# Save metadata in a file by default in json
def save_results(results, out_file, csv_mode=False):
    if csv_mode:
        with open(out_file.replace(".json", ".csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["url","title","description","emails","links"])
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "url": r["url"],
                    "title": r["title"],
                    "description": r["description"],
                    "emails": ";".join(r["emails"]),
                    "links": ";".join(r["links"])
                })
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paranoid DarkCrawler")
    parser.add_argument("--check-tor", action="store_true", help="Check Tor connectivity and exit")
    parser.add_argument("--target", help="URL to fetch (default: Tor check page)")
    parser.add_argument("--out", default=f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", help="Output file for fetched page")
    parser.add_argument("--csv", action="store_true", help="Also exports the results to CSV")
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
