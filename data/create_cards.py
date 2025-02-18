import os
import time
import json
import base64
import logging
import requests
import pandas as pd
import yfinance as yf
import dotenv

# Load environment variables from .env
dotenv.load_dotenv()

# Ensure the creature images folder exists
IMAGES_FOLDER = "creature_images"
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# ----------------------- STEP 1: Stock Data -----------------------

def fetch_stock_data():
    """
    Fetch S&P 500 company data and extract desired metrics from yfinance.
    """
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
    companies_df = pd.read_csv(url)
    logging.info("Fetched S&P 500 company CSV data.")

    all_company_metrics = []

    for i, symbol in enumerate(companies_df['Symbol']):
        # Replace dot with hyphen if needed
        symbol = symbol.replace(".", "-")
        logging.info(f"Processing {symbol} ({i+1}/{len(companies_df)})")
        ticker = yf.Ticker(symbol)

        try:
            # Get summary and balance sheet data
            company_summary = ticker.info
            company_balance_sheet = ticker.balance_sheet
            # Get latest column of balance sheet data
            balance_sheet_latest = company_balance_sheet.iloc[:, 0]
            
            # Calculate shareholder equity as total assets minus total liabilities
            shareholder_equity = (balance_sheet_latest.get("Total Assets", 0) -
                                  balance_sheet_latest.get("Total Liabilities Net Minority Interest", 0))
            
            company_metrics = {
                "companyName": company_summary.get("longName"),
                "ticker": symbol,
                "sector": company_summary.get("sector"),
                "description": company_summary.get("longBusinessSummary"),
                "marketCap": company_summary.get("marketCap"),
                "freeCashFlow": company_summary.get("freeCashflow"),
                "earningsGrowth": company_summary.get("earningsGrowth"),
                "shareholderEquity": shareholder_equity
            }
            all_company_metrics.append(company_metrics)
        except Exception as e:
            logging.error(f"Failed to get data for {symbol}: {e}")
            continue

    return all_company_metrics

# ------------------- STEP 2: Create Card Data -----------------------

def find_larger_index(value, array):
    for i, n in enumerate(array):
        if n >= value:
            return i
    return len(array)

def get_percentile_finder(data, groups):
    cutoffs = []
    data = sorted(data)
    # Adjust groups if there are fewer data points than groups
    groups = min(groups, len(data))
    group_size = len(data) // groups
    if group_size == 0:
        group_size = 1
    for i in range(group_size, len(data), group_size):
        cutoffs.append(data[i])
    
    def get_percentile(value):
        return find_larger_index(value, cutoffs)
    
    return get_percentile


def create_card_data(company_data):
    """
    Compute card stats (health, attack, defense, growth) based on company financials.
    """
    # Prepare lists with fallback values if None
    market_caps = [item['marketCap'] if item['marketCap'] is not None else 1 for item in company_data]
    free_cash_flows = [item['freeCashFlow'] if item['freeCashFlow'] is not None else 0 for item in company_data]
    shareholder_equities = [item['shareholderEquity'] if item['shareholderEquity'] is not None else 1 for item in company_data]

    market_cap_grouper = get_percentile_finder(market_caps, 10)
    free_cash_flow_grouper = get_percentile_finder(free_cash_flows, 10)
    shareholder_equity_grouper = get_percentile_finder(shareholder_equities, 10)

    card_data = []
    for item in company_data:
        # Determine percentiles for each metric
        health_percent = market_cap_grouper(item['marketCap'] if item['marketCap'] is not None else 0)
        attack_percent = free_cash_flow_grouper(item['freeCashFlow'] if item['freeCashFlow'] is not None else 0)
        defense_percent = shareholder_equity_grouper(item['shareholderEquity'] if item['shareholderEquity'] is not None else 0)
        # Scale growth; ensure within a given range
        growth = item['earningsGrowth'] if item['earningsGrowth'] is not None else 0
        growth = max(2, min(round(growth * 10) + 5, 15))

        # Map percentiles to stat values
        health =  [24, 28, 30, 35, 40, 45, 50, 55, 60, 80, 80][health_percent]
        attack =  [5,  7,  9,  11,  13, 15, 16, 17, 20, 24, 24][attack_percent]
        defense = [1,  2,  3,  4,  5,  6,  7,  8,  9,  11, 11][defense_percent]

        card_data.append({
            'ticker': item['ticker'],
            'name': item['companyName'],
            'sector': item['sector'],
            'health': health,
            'attack': attack,
            'defense': defense,
            'growth': growth
        })
    return card_data

# --------------- STEP 3: Generate Creature Data ----------------------

def generate_creature_data(company):
    """
    Uses the Anthropic (Claude) API to generate creature data for a company.
    The prompt instructs the model to create a creature name and description.
    """
    prompt = f"""
Given the company name and description, generate a description of a Pokemon-like creature that represents the company. The creature should have a name (similar to a Pokemon name) and a description. Its physical features should directly relate to the company's business or industry (for example, an electric company may have lightning features, a trash company may have garbage-themed features) and incorporate the company's brand colors. The description should focus solely on physical appearance and include anthropomorphic features (including eyes). Do not include the creature name in the description.
Below is an example for Intel Corporation:

Example:
{{
    "name": "Intellichip",
    "description": "A Pokemon creature with a sleek, angular body in blue and silver, with circuit patterns across its form. Its sharp eyes glow soft blue, symbolizing data processing intelligence. With thin, wiry limbs and connector-like digits, it interfaces with computer hardware. It manipulates data streams, controlling information flow and enhancing its and nearby devices' cognitive capabilities. It thrives in high-tech environments, aiding in computations and data analysis, communicating in binary pulses."
}}

Now, generate a creature for:
Company name: {company['companyName']}
Description: {company['description']}
Ensure the response is valid JSON.
    """

    headers = {
        'x-api-key': os.getenv('CLAUDE_API_KEY'),
        'content-type': 'application/json',
        'anthropic-version': '2023-06-01'
    }

    payload = {
        'model': 'claude-3-haiku-20240307',
        'max_tokens': 1024,
        'messages': [
            {'role': 'user', 'content': prompt},
            {'role': 'assistant', 'content': "{"}  # Starting token hint
        ]
    }

    try:
        response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=payload)
    except Exception as e:
        logging.error(f"Request error for {company['ticker']}: {e}")
        return None

    if response.status_code == 200:
        try:
            response_data = response.json()
            # Some APIs return a text snippet that needs cleaning up before loading as JSON.
            creature_string = "{" + response_data['content'][0]['text'].replace("\n", "")
            creature_data = json.loads(creature_string)
            creature_data['ticker'] = company['ticker']
            return creature_data
        except (KeyError, json.JSONDecodeError) as e:
            logging.error(f"Error parsing creature data for {company['ticker']}: {e}")
            logging.error("Faulty response text: " + response.text)
            return None
    else:
        logging.error(f"Non-200 status code for {company['ticker']}: {response.status_code}")
        logging.error(response.text)
        return None

# --------------- STEP 4: Generate Creature Images ----------------------

def generate_creature_image(creature):
    """
    Uses the Stability AI API to generate an image based on the creature description.
    The image is saved to a file and the creature dict is updated with the image file path.
    """
    prompt = f"""
An anime-style drawing of a Pokemon artstation creature that is {creature['description']}. The art style is 2D, semi-watercolor in a Pokemon-style theme, detailed and energetic on a plain white background.
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {os.getenv("STABILITY_API_KEY")}'
    }
    json_data = {
        'text_prompts': [
            {'text': prompt}
        ],
        'cfg_scale': 7,
        'height': 832,
        'width': 1216,
        'samples': 1,
        'steps': 40
    }
    engine_id = 'stable-diffusion-xl-1024-v1-0'
    url = f'https://api.stability.ai/v1/generation/{engine_id}/text-to-image'

    response = requests.post(url=url, headers=headers, json=json_data)
    if response.status_code != 200:
        raise Exception(f"Image generation failed for {creature['ticker']}: " + response.text)
    
    data = response.json()
    artifact = data["artifacts"][0]
    image_data = base64.b64decode(artifact["base64"])

    image_path = os.path.join(IMAGES_FOLDER, f"{creature['ticker']}.png")
    with open(image_path, "wb") as f:
        f.write(image_data)
    
    # Save image path in the creature data
    creature['creatureImage'] = image_path

# ------------------------- MAIN -------------------------

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Step 1: Fetch stock data from yfinance
    logging.info("Starting stock data fetch...")
    company_data = fetch_stock_data()
    logging.info(f"Fetched data for {len(company_data)} companies.")

    # Step 2: Create card data from financial metrics
    card_data = create_card_data(company_data)
    logging.info("Card data created.")

    # Step 3: Generate creature data using Anthropic API
    creature_data = []
    creature_rate_limit_start = time.time()
    for idx, company in enumerate(company_data):
        # Rate limit: after every 5 companies, pause to respect API limits
        if idx > 0 and idx % 5 == 0:
            elapsed = time.time() - creature_rate_limit_start
            if elapsed < 60:
                wait_time = 60 - elapsed
                logging.info(f"Rate limit reached. Waiting for {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            creature_rate_limit_start = time.time()

        logging.info(f"Generating creature for {company['companyName']} ({company['ticker']})")
        creature = generate_creature_data(company)
        if creature is not None:
            creature_data.append(creature)
        else:
            logging.warning(f"Creature data generation failed for {company['ticker']}.")

    logging.info(f"Generated creature data for {len(creature_data)} companies.")

    # Step 4: Generate creature images using Stability API
    image_request_count = 0
    image_rate_limit_start = time.time()
    for creature in creature_data:
        image_path = os.path.join(IMAGES_FOLDER, f"{creature['ticker']}.png")
        # Skip if image already exists
        if os.path.exists(image_path):
            creature['creatureImage'] = image_path
            logging.info(f"Image already exists for {creature['ticker']}.")
            continue

        logging.info(f"Generating image for {creature['ticker']}...")
        try:
            generate_creature_image(creature)
        except Exception as e:
            logging.error(f"Error generating image for {creature['ticker']}: {e}")
            continue

        image_request_count += 1
        # Rate limit: after 150 requests, ensure at least 10 seconds have passed
        if image_request_count >= 150:
            elapsed = time.time() - image_rate_limit_start
            if elapsed < 10:
                time.sleep(10 - elapsed)
            image_rate_limit_start = time.time()
            image_request_count = 0

    logging.info("All creature images generated.")

    # Step 5: Combine card data with creature data by matching ticker
    final_data = []
    for card in card_data:
        # Find matching creature data for this ticker (if any)
        matching_creature = next((c for c in creature_data if c.get("ticker") == card["ticker"]), None)
        if matching_creature:
            card["creatureName"] = matching_creature.get("name")
            card["creatureDescription"] = matching_creature.get("description")
            card["creatureImage"] = matching_creature.get("creatureImage")
        else:
            logging.warning(f"No creature data found for ticker {card['ticker']}.")
        final_data.append(card)

    # Step 6: Save the final combined data to one JSON file
    final_json_path = "final_data.json"
    with open(final_json_path, "w") as f:
        json.dump(final_data, f, indent=2)
    logging.info(f"Final data saved to {final_json_path}")

if __name__ == "__main__":
    main()
