import yfinance as yf
from yfinance import Ticker
import pandas as pd
import json
import logging

# Get the CSV of S&P 500 companies
url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
data = pd.read_csv(url)

# Show head to check data
print(data.head())

# Initialize an array to store the company metrics
all_company_metrics = []

# Loop through each company symbol in the data
for symbol in data['Symbol']:

    # Replace the dot in the symbol with a hyphen
    symbol = symbol.replace(".", "-")

    # Log the current symbol
    print(f"Getting data for {symbol}")
    print(f"{len(all_company_metrics)} / {len(data['Symbol'])}")

    ticker = yf.Ticker(symbol)

    # Get the company's summary and balance sheet data
    try:
        company_summary = ticker.info
        company_balance_sheet = ticker.balance_sheet
        balance_sheet_latest_year = company_balance_sheet.iloc[:, 0]

        # Extract the desired metrics
        company_metrics = {
            "companyName": company_summary.get("longName"),
            "ticker": symbol,
            "sector": company_summary.get("sector"),
            "marketCap": company_summary.get("marketCap"),
            "freeCashFlow": company_summary.get("freeCashflow"),
            "earningsGrowth": company_summary.get("earningsGrowth"),
            "shareholderEquity": balance_sheet_latest_year.get("Total Assets") - balance_sheet_latest_year.get("Total Liabilities Net Minority Interest")
        }

        # Add the company metrics to the list
        all_company_metrics.append(company_metrics)
    except Exception as e:
        print(f"Failed to get data for {symbol}: {e}")

# Print the first few metrics to check
print(all_company_metrics[:5])

# Save the data to a JSON file
with open('company_data.json', 'w') as f:
    json.dump(all_company_metrics, f)
