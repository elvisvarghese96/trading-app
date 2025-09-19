import requests
import os
import csv
import time
from dotenv import load_dotenv

def fetch_and_store_tickers():
    load_dotenv()
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

    BASE_URL = "https://api.polygon.io/v3/reference/tickers"
    URL = f"{BASE_URL}?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={POLYGON_API_KEY}"

    def get_data(url, retries=5, backoff=5):
        """Fetch data with retry logic for rate limits (429)."""
        for attempt in range(retries):
            resp = requests.get(url)
        
            if resp.status_code == 200:
                return resp.json()
        
            elif resp.status_code == 429:
                wait_time = backoff * (attempt + 1)  # exponential backoff
                print(f"Rate limit hit (429). Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
        
            else:
                print(f"Request failed with status {resp.status_code}: {resp.text}")
                return None
    
        print("Max retries reached, exiting...")
        return None


    tickers = []
    data = get_data(URL)

    if not data or 'results' not in data:
        print(f"Error: {data}")
        exit()

# Extract first page
    tickers.extend(data['results'])

# Handle pagination
    while 'next_url' in data:
        print("Fetching next page:", data['next_url'])
        next_url = data['next_url'] + f"&apiKey={POLYGON_API_KEY}"
        data = get_data(next_url)
    
        if not data or 'results' not in data:
            break
    
        tickers.extend(data['results'])

# Schema
    example_structure = {
    'ticker': 'BAYA',
    'name': 'Bayview Acquisition Corp Class A Ordinary Shares',
    'market': 'stocks',
    'locale': 'us',
    'primary_exchange': 'XNAS',
    'type': 'CS',
    'active': True,
    'currency_name': 'usd',
    'cik': '0001969475',
    'composite_figi': 'BBG01KT6FX00',
    'share_class_figi': 'BBG01KT6FXV6',
    'last_updated_utc': '2025-09-13T06:11:08.182887412Z'
    }

# Write to CSV
    with open("tickers.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = list(example_structure.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickers)

    print(f"Wrote {len(tickers)} tickers to tickers.csv")

if __name__ == "__main__":
    fetch_and_store_tickers()
