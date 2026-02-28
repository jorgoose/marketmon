#!/usr/bin/env python3
"""
Marketmon Card Generator

Fetches S&P 500 financial data, transforms it into game card stats,
generates creature descriptions via Claude, and creature images via Gemini Imagen.
"""

import io
import os
import json
import re
import logging

import anthropic
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image as PILImage

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SP500_CSV = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"

OUTPUT_JSON = "final_data.json"
IMAGE_FOLDER = "creature_images"

HEALTH_VALUES = [24, 28, 30, 35, 40, 45, 50, 55, 60, 80, 80]
ATTACK_VALUES = [5, 7, 9, 11, 13, 15, 16, 17, 20, 24, 24]
DEFENSE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 11]


# --- Yahoo Finance ---

def fetch_company_metrics(symbols):
    metrics = []
    for i, symbol in enumerate(symbols):
        symbol = symbol.replace(".", "-")
        logging.info("Fetching %s (%d/%d)", symbol, i + 1, len(symbols))

        try:
            tk = yf.Ticker(symbol)
            info = tk.info

            if not info or not info.get("shortName"):
                logging.warning("No data for %s, skipping", symbol)
                continue

            raw_growth = info.get("earningsQuarterlyGrowth")
            try:
                earnings_growth = float(raw_growth)
            except (ValueError, TypeError):
                earnings_growth = 0.0

            shareholder_equity = 0
            bs = tk.balance_sheet
            if bs is not None and not bs.empty:
                for label in ["Stockholders Equity", "Common Stock Equity",
                              "Total Equity Gross Minority Interest"]:
                    if label in bs.index:
                        val = bs.loc[label].iloc[0]
                        if pd.notna(val):
                            shareholder_equity = int(val)
                            break

            entry = {
                "companyName": info.get("shortName") or info.get("longName"),
                "ticker": symbol,
                "sector": info.get("sector"),
                "description": info.get("longBusinessSummary"),
                "marketCap": int(info.get("marketCap") or 0),
                "freeCashFlow": int(info.get("freeCashflow") or 0),
                "shareholderEquity": shareholder_equity,
                "earningsGrowth": earnings_growth,
            }
            metrics.append(entry)

        except Exception as e:
            logging.error("Failed to fetch %s: %s", symbol, e)

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


def generate_creature(client, card):
    prompt = CREATURE_PROMPT.format(name=card.get("name"), description=card.get("description"))
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text
        text = re.sub(r"^```(?:json)?\s*", "", text.strip())
        text = re.sub(r"\s*```$", "", text.strip())
        data = json.loads(text)
        data["ticker"] = card.get("ticker")
        return data
    except Exception as e:
        logging.error("Creature generation failed for %s: %s", card.get("ticker"), e)
    return None


# --- Gemini Imagen image generation ---

def generate_image(gemini_client, creature):
    prompt = (
        f"An anime-style drawing of a Pokemon artstation creature that is {creature.get('description')}. "
        "The art style is 2D, semi-watercolor in a Pokemon-style theme, detailed and energetic on a plain white background."
    )
    try:
        response = gemini_client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="4:3",
            ),
        )
        if response.generated_images:
            raw = response.generated_images[0].image
            return PILImage.open(io.BytesIO(raw.image_bytes))
        logging.error("No images returned from Gemini")
    except Exception as e:
        logging.error("Image generation failed: %s", e)
    return None


# --- Main pipeline ---

def run(anthropic_key, gemini_key):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    claude = anthropic.Anthropic(api_key=anthropic_key)
    gemini = genai.Client(api_key=gemini_key)

    # 1. Fetch S&P 500 list
    df = pd.read_csv(SP500_CSV)
    logging.info("Fetched S&P 500 company list")

    # 2. Get financial metrics
    symbols = df["Symbol"].tolist()
    company_metrics = fetch_company_metrics(symbols)
    if not company_metrics:
        logging.error("No metrics fetched, exiting")
        return

    # 3. Create card stats
    cards = create_card_data(company_metrics)

    # 4. Generate creatures + images
    for i, card in enumerate(cards):
        ticker = card.get("ticker")
        logging.info("Generating creature for %s (%d/%d)", ticker, i + 1, len(cards))

        creature = generate_creature(claude, card)
        if not creature:
            logging.error("Failed creature generation for %s", ticker)
            continue

        card["creatureName"] = creature.get("name", "")
        image_path = os.path.join(IMAGE_FOLDER, f"{ticker}.webp")

        if os.path.exists(image_path):
            logging.info("Image already exists for %s", ticker)
        else:
            img = generate_image(gemini, creature)
            if img:
                img.save(image_path, "webp")
                logging.info("Saved image for %s", ticker)
            else:
                logging.error("Failed image generation for %s", ticker)


    # 5. Write output (strip fields not needed by frontend)
    for card in cards:
        card.pop("description", None)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(cards, f, indent=2)
    logging.info("Written %d cards to %s", len(cards), OUTPUT_JSON)


if __name__ == "__main__":
    load_dotenv()

    keys = {
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    }
    missing = [k for k, v in keys.items() if not v]
    if missing:
        logging.error("Missing env vars: %s", ", ".join(missing))
    else:
        run(keys["ANTHROPIC_API_KEY"], keys["GEMINI_API_KEY"])
