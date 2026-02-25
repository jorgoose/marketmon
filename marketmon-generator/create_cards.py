#!/usr/bin/env python3
"""
Marketmon Card Generator

Fetches S&P 500 financial data, transforms it into game card stats,
generates creature descriptions via Claude, and creature images via Stability AI.
"""

import os
import time
import json
import base64
import logging

import requests
import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SP500_CSV = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
CLAUDE_URL = "https://api.anthropic.com/v1/messages"
STABILITY_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

OUTPUT_JSON = "final_data.json"
IMAGE_FOLDER = "creature_images"

HEALTH_VALUES = [24, 28, 30, 35, 40, 45, 50, 55, 60, 80, 80]
ATTACK_VALUES = [5, 7, 9, 11, 13, 15, 16, 17, 20, 24, 24]
DEFENSE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 11]


# --- Alpha Vantage ---

def av_get(api_key, **params):
    params["apikey"] = api_key
    try:
        r = requests.get(ALPHA_VANTAGE_URL, params=params)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        logging.error("Alpha Vantage request failed: %s", e)
        return None


def fetch_company_metrics(api_key, symbols, sleep=15):
    metrics = []
    for i, symbol in enumerate(symbols):
        symbol = symbol.replace(".", "-")
        logging.info("Fetching %s (%d/%d)", symbol, i + 1, len(symbols))

        overview = av_get(api_key, function="OVERVIEW", symbol=symbol)
        if not overview or "Name" not in overview:
            logging.warning("No overview for %s, skipping", symbol)
            time.sleep(sleep)
            continue

        balance = av_get(api_key, function="BALANCE_SHEET", symbol=symbol)
        annual = (balance or {}).get("annualReports", [])
        if not annual:
            logging.warning("No balance sheet for %s, skipping", symbol)
            time.sleep(sleep)
            continue

        cash = av_get(api_key, function="CASH_FLOW", symbol=symbol)
        cash_annual = (cash or {}).get("annualReports", [])
        if not cash_annual:
            logging.warning("No cash flow for %s, skipping", symbol)
            time.sleep(sleep)
            continue

        try:
            entry = {
                "companyName": overview.get("Name"),
                "ticker": symbol,
                "sector": overview.get("Sector"),
                "description": overview.get("Description"),
                "marketCap": int(overview.get("MarketCapitalization", 0)),
                "freeCashFlow": int(cash_annual[0].get("freeCashFlow", 0)),
                "shareholderEquity": int(annual[0].get("totalShareholderEquity", 0)),
            }
        except (ValueError, TypeError) as e:
            logging.error("Bad numeric data for %s: %s", symbol, e)
            time.sleep(sleep)
            continue

        metrics.append(entry)
        time.sleep(sleep)

    logging.info("Collected metrics for %d companies", len(metrics))
    return metrics


# --- Card stats ---

def make_percentile_fn(values, groups=10):
    s = sorted(values)
    step = max(len(s) // groups, 1)
    cutoffs = [s[i] for i in range(step, len(s), step)]

    def get_group(val):
        for i, c in enumerate(cutoffs):
            if c >= val:
                return i
        return len(cutoffs)

    return get_group


def create_card_data(company_data):
    caps = [d.get("marketCap", 1) or 1 for d in company_data]
    flows = [d.get("freeCashFlow", 0) or 0 for d in company_data]
    equities = [d.get("shareholderEquity", 1) or 1 for d in company_data]

    cap_group = make_percentile_fn(caps)
    flow_group = make_percentile_fn(flows)
    eq_group = make_percentile_fn(equities)

    cards = []
    for d in company_data:
        hi = min(cap_group(d.get("marketCap", 0) or 0), len(HEALTH_VALUES) - 1)
        ai = min(flow_group(d.get("freeCashFlow", 0) or 0), len(ATTACK_VALUES) - 1)
        di = min(eq_group(d.get("shareholderEquity", 0) or 0), len(DEFENSE_VALUES) - 1)

        cards.append({
            "ticker": d.get("ticker"),
            "health": HEALTH_VALUES[hi],
            "attack": ATTACK_VALUES[ai],
            "defense": DEFENSE_VALUES[di],
            "growth": max(2, min(15, round((d.get("earningsGrowth", 0) or 0) * 10) + 5)),
            "name": d.get("companyName"),
            "description": d.get("description"),
            "sector": d.get("sector"),
        })

    logging.info("Created card data for %d companies", len(cards))
    return cards


# --- Claude creature generation ---

CREATURE_PROMPT = (
    "Given the company name and the description of the company, generate a description "
    "of a Pokemon creature that represents the company. The creature should have a name "
    "(similar to a Pokemon name) and a description. Physical features described should directly "
    "relate to the company's business or industry, i.e., an electric company may have a creature "
    "with lightning bolt features, or a trash company may have a creature with garbage-themed features, "
    "and the company's brand colors. The only thing described should be the creature's physical appearance. "
    "The description should match some sort of creature, animal or monster. The description should NOT include "
    "the creature name. Creature descriptions MUST contain descriptions of anthropomorphic features, and "
    "specifically must include eyes. Below is an example for the company Intel Corporation:\n\n"
    'Example response:\n{{\n    "name": "Intellichip",\n    "description": "A Pokemon creature with a sleek, '
    "angular body in blue and silver, with circuit patterns across its form. Its sharp eyes glow soft blue, "
    "symbolizing data processing intelligence. With thin, wiry limbs and connector-like digits, it interfaces "
    "with computer hardware. It manipulates data streams, controlling information flow, and processes vast data, "
    "enhancing its and nearby devices' cognitive capabilities. It's in high-tech environments, aiding in "
    'computations and data analysis, communicating in binary pulses."\n}}\n\n'
    "Now, generate a creature for the following company. Ensure your response is valid JSON format.\n"
    "Company name: {name}.\nDescription: {description}.\n"
)


def generate_creature(api_key, card):
    prompt = CREATURE_PROMPT.format(name=card.get("name"), description=card.get("description"))
    try:
        r = requests.post(CLAUDE_URL, headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }, json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "{"},
            ],
        })
        if r.status_code == 200:
            text = r.json()["content"][0]["text"].replace("\n", "")
            data = json.loads("{" + text)
            data["ticker"] = card.get("ticker")
            return data
        logging.error("Claude API %s: %s", r.status_code, r.text)
    except Exception as e:
        logging.error("Creature generation failed for %s: %s", card.get("ticker"), e)
    return None


# --- Stability AI image generation ---

def generate_image(api_key, creature):
    prompt = (
        f"An anime-style drawing of a Pokemon artstation creature that is {creature.get('description')}. "
        "The art style is 2D, semi-watercolor in a Pokemon-style theme, detailed and energetic on a plain white background."
    )
    try:
        r = requests.post(STABILITY_URL, headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }, json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 832,
            "width": 1216,
            "samples": 1,
            "steps": 40,
        })
        if r.status_code == 200:
            return base64.b64decode(r.json()["artifacts"][0]["base64"])
        logging.error("Stability API %s: %s", r.status_code, r.text)
    except Exception as e:
        logging.error("Image generation failed: %s", e)
    return None


# --- Main pipeline ---

def run(alpha_key, claude_key, stability_key):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    # 1. Fetch S&P 500 list
    df = pd.read_csv(SP500_CSV)
    logging.info("Fetched S&P 500 company list")

    # 2. Get financial metrics (hardcoded test symbols for now)
    symbols = ["NVDA", "AMD", "COST", "MCD", "CAT"]
    # symbols = df["Symbol"].tolist()  # uncomment for full run
    company_metrics = fetch_company_metrics(alpha_key, symbols)
    if not company_metrics:
        logging.error("No metrics fetched, exiting")
        return

    # 3. Create card stats
    cards = create_card_data(company_metrics)

    # 4. Generate creatures + images
    req_count, start = 0, time.time()
    for i, card in enumerate(cards):
        ticker = card.get("ticker")
        logging.info("Generating creature for %s (%d/%d)", ticker, i + 1, len(cards))

        creature = generate_creature(claude_key, card)
        if not creature:
            logging.error("Failed creature generation for %s", ticker)
            continue

        card["creatureName"] = creature.get("name", "")
        image_path = os.path.join(IMAGE_FOLDER, f"{ticker}.png")

        if os.path.exists(image_path):
            logging.info("Image already exists for %s", ticker)
        else:
            img = generate_image(stability_key, creature)
            if img:
                with open(image_path, "wb") as f:
                    f.write(img)
                logging.info("Saved image for %s", ticker)
            else:
                logging.error("Failed image generation for %s", ticker)

        card["creatureImage"] = image_path

        # Rate limit: 5 requests per 60s
        req_count += 1
        if req_count >= 5:
            elapsed = time.time() - start
            if elapsed < 60:
                time.sleep(60 - elapsed)
            start, req_count = time.time(), 0

    # 5. Write output
    with open(OUTPUT_JSON, "w") as f:
        json.dump(cards, f, indent=2)
    logging.info("Written %d cards to %s", len(cards), OUTPUT_JSON)


if __name__ == "__main__":
    load_dotenv()

    keys = {
        "ALPHA_VANTAGE_API_KEY": os.getenv("ALPHA_VANTAGE_API_KEY"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "STABILITY_API_KEY": os.getenv("STABILITY_API_KEY"),
    }
    missing = [k for k, v in keys.items() if not v]
    if missing:
        logging.error("Missing env vars: %s", ", ".join(missing))
    else:
        run(keys["ALPHA_VANTAGE_API_KEY"], keys["CLAUDE_API_KEY"], keys["STABILITY_API_KEY"])
