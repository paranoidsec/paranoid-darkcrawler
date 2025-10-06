#!/usr/bin/env python3

import os, re, csv, json, argparse, requests, time
from urllib.parse import urljoin, urlparse
from collections import deque
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

# Check if the URL is on the same host
def is_same_host(start_url, new_url):
    return urlparse(start_url).hostname == urlparse(new_url).hostname

# Check if infinite crawl
def unbounded(x: int) -> bool:
    return x < 0

# Check if connected to TOR network
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

# From a given domain extract other domains different than the current
# one
def extract_domains_from_links(links):
    # Return just the netloc (host:port) from each link.
    domains = set()
    for link in links:
        try:
            parsed = urlparse(link)
            if parsed.hostname and parsed not in domains:
                domains.add(parsed.hostname)
        except:
            continue
    return domains

# Get the content of a webpage
def fetch_page(url, timeout=30):
    # Fetch a single page via TOR
    try:
        r = session.get(url, timeout=timeout)
        return r.text
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")
        return ""

def save_state(state_file, visited, queue, results):
    # Save current crawl state to JSON file.
    try:
        data = {
            "visited": list(visited),
            "queue": list(queue),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[!] Failed to save state: {e}")

def load_state(state_file):
    # Load crawl state from JSON file.
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        visited = set(data.get("visited", []))
        queue = deque(data.get("queue", []))
        print(f"[*] Resumed state from {state_file} ({len(visited)} visited, {len(queue)} queued).")
        return visited, queue
    except Exception as e:
        print(f"[!] Failed to load state: {e}")
        return set(), deque()

# Crawl the webpage to find links and extract metadata from those links
def crawl(start_url, depth, max_pages, delay, max_runtime_minutes, mode="content", state_file=None):
    # Set the timer
    start_ts = time.time()
    max_runtime_seconds = None if unbounded(max_runtime_minutes) else max_runtime_minutes * 60

    # Domains Discovered
    discovered_domains = set()

    # Load previous state if exists
    visited, queue, results = set(), deque(), []
    if state_file and os.path.exists(state_file):
        visited, queue = load_state(state_file)
    if not queue:
        queue.append((start_url, 0))

    try:
        while queue:
            # stop if max-pages reached (unless unbounded)
            if not unbounded(max_pages) and len(visited) >= max_pages:
                print("[*] Reached --max-pages limit, stopping.")
                break

            # stop if runtime budget spent (unless unbounded)
            if max_runtime_seconds is not None and (time.time() - start_ts) >= max_runtime_seconds:
                print("[*] Reached --max-runtime budget, stopping.")
                break

            url, level = queue.popleft()

            # depth gate (skip only when depth is bounded)
            if not unbounded(depth) and level > depth:
                continue
            if url in visited:
                continue

            visited.add(url)
            print(f"[*] ({level}/{depth if not unbounded(depth) else '∞'}) Fetching: {url}")

            html = fetch_page(url)
            if html:
                meta = extract_metadata(html, url)
                results.append(meta)

                # Get new domains
                if mode == "domains":
                    new_domains = extract_domains_from_links(meta["links"])
                    discovered_domains.update(new_domains)

                if unbounded(depth) or level < depth:
                    # enqueue same-host links
                    for link in get_absolute_links(start_url, meta["links"]):
                        if is_same_host(start_url, link) and link not in visited:
                            queue.append((link, level + 1))

            # save state after each page (if requested)
            if state_file:
                save_state(state_file, visited, queue, results)

            time.sleep(delay)

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Writing partial results…")
        if state_file:
            save_state(state_file, visited, queue, results)
            print(f"[*] State saved to {state_file}")

    return discovered_domains if mode == "domains" else results

# Get the absolute links for each link retrieved
def get_absolute_links(base_url, links):
    absolute_links = []
    for link in links:
        if link.startswith("#") or link.lower().startswith("javascript:"):
            continue
        absolute = urljoin(base_url, link)
        absolute_links.append(absolute)
    return absolute_links

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
    parser.add_argument("--depth", type=int, default=0, help="Crawl depth (0 = only target, positive N = levels deep, -1 = unlimited)")
    parser.add_argument("--max-pages", type=int, default=50, help="Max pages to fetch (positive), or -1 for unlimited")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests (default 2 sec)")
    parser.add_argument("--max-runtime", type=int, default=-1, help="Max runtime in minutes (-1 = unlimited)")
    parser.add_argument("--state-file", default=None, help="Path to save/load crawl state (JSON). Use to resume long runs.")
    parser.add_argument("--mode", choices=["content","domains"], default="content",help="Crawl mode: 'content' = fetch pages & metadata, 'domains' = only collect domains/hosts")
    args = parser.parse_args()

    print("=== Paranoid DarkCrawler ===")

    if args.check_tor:
        test_tor_connection()
    elif args.target:
        # Check if the results folder exits
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        if test_tor_connection():
            if unbounded(args.depth) and unbounded(args.max_pages) and unbounded(args.max_runtime):
                print("[!] WARNING: depth, max-pages, and max-runtime are all unlimited.")
                print("    This may run indefinitely. Consider setting --max-runtime or --max-pages and keep --delay >= 2s.")
            path = os.path.join(results_folder, args.out)
            if args.state_file:
                state = os.path.join(results_folder, args.state_file)
                results = crawl(args.target, args.depth, args.max_pages, args.delay, args.max_runtime, args.mode, state)
            else:
                results = crawl(args.target, args.depth, args.max_pages, args.delay, args.max_runtime, args.mode)
            if args.mode == "domains":
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(sorted(list(results)), f, indent=2)
                    if args.csv:
                        with open(path.replace(".json", ".csv"), "w", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(["domain"])
                            for d in sorted(list(results)):
                                writer.writerow([d])
            else:
                save_results(results, path, csv_mode=args.csv)
        else:
            print("[!] Aborting fetch due to Tor failure.")
    else:
        parser.print_help()
