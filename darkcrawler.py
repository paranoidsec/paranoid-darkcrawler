#!/usr/bin/env python3

import requests

def test_tor_connection(timeout=15):
    # Test if the Tor SOCKS5 proxy is working.
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
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

if __name__ == "__main__":
    print("=== Paranoid DarkCrawler ===")
    if not test_tor_connection():
        print("[!] Tor connection failed. Please start Tor (e.g., `tor` or `service tor start`).")
    else:
        print("[+] Ready to crawl! (Crawling logic coming soon...)")
