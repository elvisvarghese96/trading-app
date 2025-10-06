import requests
import os
import time
from dotenv import load_dotenv
import snowflake.connector
from datetime import datetime
import datetime as dt

def fetch_and_store_tickers():
    load_dotenv()
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

    # Snowflake credentials
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")  
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE") 
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")      
    SNOWFLAKE_TABLE = os.getenv("SNOWFLAKE_TABLE")        
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
    SNOWFLAKE_AUTHENTICATOR = os.getenv("SNOWFLAKE_AUTHENTICATOR")

    BASE_URL = "https://api.polygon.io/v3/reference/tickers"
    URL = f"{BASE_URL}?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={POLYGON_API_KEY}"
    DS = datetime.now().strftime("%Y-%m-%d")

    def get_data(url, retries=5, backoff=5):
        """Fetch data with retry logic for rate limits (429)."""
        for attempt in range(retries):
            resp = requests.get(url)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                wait_time = backoff * (attempt + 1)
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

    tickers.extend(data['results'])

    # Handle pagination
    while 'next_url' in data:
        print("Fetching next page:", data['next_url'])
        next_url = data['next_url'] + f"&apiKey={POLYGON_API_KEY}"
        data = get_data(next_url)
        if not data or 'results' not in data:
            break
        tickers.extend(data['results'])

    print(f"Fetched {len(tickers)} tickers.")

    # Define schema keys
    fieldnames = [
        "ticker",
        "name",
        "market",
        "locale",
        "primary_exchange",
        "type",
        "active",
        "currency_name",
        "cik",
        "composite_figi",
        "share_class_figi",
        "last_updated_utc",
        "ds"]

    # Normalize rows (fill missing fields with None)
    normalized_tickers = []
    for t in tickers:
        row = {key: t.get(key, None) for key in fieldnames}
        row["ds"] = DS  # Add datestamp for each record
        normalized_tickers.append(row)

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE,
        role=SNOWFLAKE_ROLE
    )
    cs = conn.cursor()

    # Create table if not exists
    cs.execute(f"""
        CREATE TABLE IF NOT EXISTS {SNOWFLAKE_TABLE} (
            ticker VARCHAR,
            name VARCHAR,
            market VARCHAR,
            locale VARCHAR,
            primary_exchange VARCHAR,
            type VARCHAR,
            active BOOLEAN,
            currency_name VARCHAR,
            cik VARCHAR,
            composite_figi VARCHAR,
            share_class_figi VARCHAR,
            last_updated_utc VARCHAR,
            ds VARCHAR
        );
    """)

    # Insert tickers
    insert_sql = f"""
        INSERT INTO {SNOWFLAKE_TABLE} 
        ({", ".join(fieldnames)})
        VALUES ({", ".join([f"%({k})s" for k in fieldnames])})
    """
    cs.executemany(insert_sql, normalized_tickers)
    conn.commit()
    cs.close()
    conn.close()

    print(f"Inserted {len(normalized_tickers)} tickers into Snowflake table {SNOWFLAKE_TABLE}.")

if __name__ == "__main__":
    fetch_and_store_tickers()