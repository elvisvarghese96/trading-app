# Stock-trading-app using Polygon REST API

This project is a Stock trading app that connects to the Polygon.io REST API to fetch stock ticker information. It demonstrates how to work with APIs in financial applications, handle pagination, and structure market data for further analysis.

##  Features

- **API Integration**: Fetches real-time stock ticker data from Polygon.io
- **Pagination Handling**: Handles pagination (retrieves multiple pages of data)
- **CSV Export**: Export data to CSV file format with consistent schema for analysis
- **Design**: Reusable function for data pipeline integration

##  Schema Design

The application exports the following fields for each stock ticker:

| Field | Description |
|-------|-------------|
| `ticker` | Stock symbol (e.g AAA, AACT etc) |
| `name` | Company name |
| `market` | Market type (stocks) |
| `locale` | Geographic region (us) |
| `primary_exchange` | Exchange code (e.g., XNAS, XNYS) |
| `type` | Security type (e.g., CS for Common Stock) |
| `active` | Trading status (true/false) |
| `currency_name` | Currency (usd) |
| `cik` | Central Index Key |
| `composite_figi` | Composite FIGI identifier |
| `share_class_figi` | Share class FIGI identifier |
| `last_updated_utc` | Last update timestamp |


⚙️ How It Works

Load the Polygon API key from a .env file.
Call the /v3/reference/tickers endpoint to fetch stock tickers.
Store results in memory and handle pagination with next_url.
Save results into tickers.csv with fields.- (Now pushed into Snowflake)

##  Installation

### Prerequisites

- Python >=3.8
- pip

### Setup

1. **Cloning the repository**
   ```bash
   git clone https://github.com/elvisvarghese96/trading-app.git
   cd trading-app.git
    ```

2. **Creating a virtual environment**
   ```bash
   python -m venv stockenv
   source stockenv/bin/activate    
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Assign environment variables**

    Add your poligon.io API key
    ```bash
    POLYGON_API_KEY='Enter_API_Key'
    ```
5. **For creating a Poligon API Key**

    - Visit [Poligon.io](https://polygon.io/)
    - Create a free account


## Running the script
```bash
Execute the python scritp.py
```
This will perform the following:

- Fetches real-time stock ticker data from Polygon.io
- Handles pagination (retrieves multiple pages of data)
- Export data to CSV file format with consistent schema for analysis
- Reusable function for data pipeline integration

## Project Structure
```
polygon-snowflake-pipeline/
├── data/                   # (Optional) Local storage for CSV exports or logs
├── src/
│   ├── __init__.py
│   └── main.py             # Your provided script (renamed for clarity)
├── .env                    # Environment variables (API keys, Snowflake creds)
├── .gitignore              # To prevent pushing sensitive .env to GitHub
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

##  Data Pipeline Integration

This project demonstrates key data pipeline concepts:

- **Data Extraction**: Fetches data from external API
- **Data Processing**: Handles pagination and data transformation
- **Data Storage**: Exports to CSV format/Snowflake Db
- **Scheduling**: Automated execution
- **Error Handling**: Robust API response handling


## CRON JOB
Scheduled the job at 9 am.

```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/trading-app.git && python script.py
```
