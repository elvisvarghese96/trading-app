# Stock-trading-app
## Stock Trading Data App (Polygon REST API)##

This project is a Stock trading app that connects to the Polygon.io REST API to fetch stock ticker information. It demonstrates how to work with APIs in financial applications, handle pagination, and structure market data for further analysis.

📌 Features

Connects to Polygon.io REST API
Fetches all active stock tickers
Handles pagination (retrieves multiple pages of data)
Extracts structured fields (ticker, name, market, exchange, type, etc.)
Saves results into a CSV file for analysis

Tech Stack

Python
Requests (for API calls)
dotenv (for API key management)
CSV module (to write structured data)

⚙️ How It Works

Load the Polygon API key from a .env file
Call the /v3/reference/tickers endpoint to fetch stock tickers
Store results in memory and handle pagination with next_url
Save results into tickers.csv with fields