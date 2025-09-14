import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

URL = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={POLYGON_API_KEY}'

resp = requests.get(URL)

tickers = []
data = resp.json()

if 'results' not in data:
    print(f"Error: {data}")
    exit()

for ticker in data['results']:
    print(ticker)
    tickers.append(ticker)

while 'next_url' in data:
    print('next page',data['next_url'])
    URL = data['next_url'] + f'&apiKey={POLYGON_API_KEY}'
    resp = requests.get(URL)
    data = resp.json()
    
    if 'results' not in data:
        print(f"Error on pagination: {data}")
        break

    for ticker in data['results']:
        tickers.append(ticker)

example_structure = {'ticker': 'BAYA', 
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
                    'last_updated_utc': '2025-09-13T06:11:08.182887412Z'}

# Write to CSV with same schema as example_ticker
with open('tickers.csv', 'w', newline='', encoding ='utf-8') as csvfile:
    fieldnames = list(example_structure.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tickers)

print(f"Wrote {len(tickers)} tickers to tickers.csv")

