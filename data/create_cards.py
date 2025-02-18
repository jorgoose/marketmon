#!/usr/bin/env python3
"""
Creature Card Application

This module fetches company data, obtains financial metrics via the Alpha Vantage API,
generates card data, calls the Anthropic (Claude) API to generate creature descriptions,
and uses the Stability.ai API to generate creature images. Finally, the processed
card data is written to a JSON file.
"""

import os
import time
import json
import base64
import logging
from typing import Any, Dict, List, Optional, Callable

import requests
import pandas as pd
from dotenv import load_dotenv

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class CompanyDataFetcher:
    """Fetches company data from a remote CSV file."""

    DATA_URL = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"

    def fetch(self) -> pd.DataFrame:
        """
        Fetch the S&P 500 companies CSV and return a DataFrame.
        """
        df = pd.read_csv(self.DATA_URL)
        logging.info("Fetched S&P 500 company list.")
        return df


class AlphaVantageClient:
    """
    Client to fetch company financial metrics from the Alpha Vantage API.
    Due to API rate limits, the client pauses between company requests.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str, sleep_seconds: int = 15) -> None:
        self.api_key = api_key
        self.sleep_seconds = sleep_seconds

    def _get_json(self, params: Dict[str, str]) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(self.BASE_URL, params=params)
            if response.status_code != 200:
                logging.error("Error fetching data: %s (Status Code: %s)", params, response.status_code)
                return None
            return response.json()
        except Exception as e:
            logging.error("Exception during API call: %s", e)
            return None

    def fetch_company_metrics(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        For each company symbol, fetch the overview, balance sheet, and cash flow data.
        Returns a list of company metrics dictionaries.
        """
        all_metrics: List[Dict[str, Any]] = []
        # For testing, limit to first company (adjust slice as needed)
        # symbols = df["Symbol"][:5].tolist()
        # For demo, use some well recognized symbols :)
        symbols = ["NVDA", "AMD", "COST", "MCD", "CAT"]
        total = len(symbols)
        for i, symbol in enumerate(symbols):
            symbol = symbol.replace(".", "-")
            logging.info("Getting data for %s (%d/%d)", symbol, i + 1, total)

            # 1. Get Overview data
            overview_params = {
                "function": "OVERVIEW",
                "symbol": symbol,
                "apikey": self.api_key,
            }
            overview_data = self._get_json(overview_params)
            if not overview_data or "Name" not in overview_data:
                logging.warning("No valid overview data for %s. Skipping.", symbol)
                time.sleep(self.sleep_seconds)
                continue

            # 2. Get Balance Sheet data
            balance_params = {
                "function": "BALANCE_SHEET",
                "symbol": symbol,
                "apikey": self.api_key,
            }
            balance_data = self._get_json(balance_params)
            if not balance_data or "annualReports" not in balance_data or not balance_data["annualReports"]:
                logging.warning("No balance sheet data for %s. Skipping.", symbol)
                time.sleep(self.sleep_seconds)
                continue
            latest_balance = balance_data["annualReports"][0]
            shareholder_equity = latest_balance.get("totalShareholderEquity")
            if shareholder_equity is None:
                logging.warning("Missing shareholder equity for %s. Skipping.", symbol)
                time.sleep(self.sleep_seconds)
                continue
            try:
                shareholder_equity = int(shareholder_equity)
            except Exception as e:
                logging.error("Error converting shareholder equity for %s: %s", symbol, e)
                time.sleep(self.sleep_seconds)
                continue

            # 3. Get Cash Flow data
            cash_params = {
                "function": "CASH_FLOW",
                "symbol": symbol,
                "apikey": self.api_key,
            }
            cash_data = self._get_json(cash_params)
            if not cash_data or "annualReports" not in cash_data or not cash_data["annualReports"]:
                logging.warning("No cash flow data for %s. Skipping.", symbol)
                time.sleep(self.sleep_seconds)
                continue
            latest_cash = cash_data["annualReports"][0]
            free_cash_flow = latest_cash.get("freeCashFlow", "0")
            try:
                free_cash_flow = int(free_cash_flow)
            except Exception as e:
                logging.error("Error converting free cash flow for %s: %s", symbol, e)
                free_cash_flow = 0

            # 4. Convert market capitalization
            market_cap = overview_data.get("MarketCapitalization")
            if market_cap is None:
                logging.warning("Missing market cap for %s. Skipping.", symbol)
                time.sleep(self.sleep_seconds)
                continue
            try:
                market_cap = int(market_cap)
            except Exception as e:
                logging.error("Error converting market cap for %s: %s", symbol, e)
                time.sleep(self.sleep_seconds)
                continue

            earnings_growth = 0  # earningsGrowth not provided by overview

            metrics = {
                "companyName": overview_data.get("Name"),
                "ticker": symbol,
                "sector": overview_data.get("Sector"),
                "description": overview_data.get("Description"),
                "marketCap": market_cap,
                "freeCashFlow": free_cash_flow,
                "earningsGrowth": earnings_growth,
                "shareholderEquity": shareholder_equity,
            }
            all_metrics.append(metrics)

            # Sleep to respect rate limits
            time.sleep(self.sleep_seconds)

        logging.info("Collected metrics for %d companies.", len(all_metrics))
        return all_metrics


class CardDataCreator:
    """
    Creates card data from company metrics using percentile grouping.
    """

    @staticmethod
    def _find_larger_index(value: int, cutoffs: List[int]) -> int:
        """
        Return the index of the first cutoff that is greater than or equal to value.
        """
        for i, cutoff in enumerate(cutoffs):
            if cutoff >= value:
                return i
        return len(cutoffs)

    @staticmethod
    def _get_percentile_finder(data: List[int], groups: int) -> Callable[[int], int]:
        """
        Return a function that computes the percentile group index for a given value.
        """
        sorted_data = sorted(data)
        n = len(sorted_data)
        group_size = n // groups if n // groups > 0 else 1
        cutoffs = [sorted_data[i] for i in range(group_size, n, group_size)]

        def get_percentile(value: int) -> int:
            return CardDataCreator._find_larger_index(value, cutoffs)

        return get_percentile

    def create_card_data(self, company_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create card data from company metrics.
        """
        # Extract stats, ensuring non-null values
        market_caps = [item.get("marketCap", 1) or 1 for item in company_data]
        free_cash_flows = [item.get("freeCashFlow", 0) or 0 for item in company_data]
        shareholder_equities = [item.get("shareholderEquity", 1) or 1 for item in company_data]

        market_cap_grouper = self._get_percentile_finder(market_caps, 10)
        free_cash_flow_grouper = self._get_percentile_finder(free_cash_flows, 10)
        shareholder_equity_grouper = self._get_percentile_finder(shareholder_equities, 10)

        card_data = []
        # Mapping stat values
        health_values = [24, 28, 30, 35, 40, 45, 50, 55, 60, 80, 80]
        attack_values = [5, 7, 9, 11, 13, 15, 16, 17, 20, 24, 24]
        defense_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 11]

        for item in company_data:
            market_cap = item.get("marketCap", 0) or 0
            free_cash_flow = item.get("freeCashFlow", 0) or 0
            shareholder_equity = item.get("shareholderEquity", 0) or 0
            growth = item.get("earningsGrowth", 0) or 0

            health_index = market_cap_grouper(market_cap)
            attack_index = free_cash_flow_grouper(free_cash_flow)
            defense_index = shareholder_equity_grouper(shareholder_equity)

            health = health_values[min(health_index, len(health_values) - 1)]
            attack = attack_values[min(attack_index, len(attack_values) - 1)]
            defense = defense_values[min(defense_index, len(defense_values) - 1)]
            growth_stat = max(2, min(round(growth * 10) + 5, 15))

            card_entry = {
                "ticker": item.get("ticker"),
                "health": health,
                "attack": attack,
                "growth": growth_stat,
                "defense": defense,
                "name": item.get("companyName"),
                "description": item.get("description"),
                "sector": item.get("sector"),
            }
            card_data.append(card_entry)

        logging.info("Card data created from company metrics.")
        return card_data


class CreatureGenerator:
    """
    Generates creature data using the Anthropic (Claude) API.
    """

    API_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def generate(self, company: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate creature data for a company.
        """
        prompt = (
            f"Given the company name and the description of the company, generate a description "
            f"of a Pokemon creature that represents the company. The creature should have a name "
            f"(similar to a Pokemon name) and a description. Physical features described should directly "
            f"relate to the company's business or industry, i.e., an electric company may have a creature "
            f"with lightning bolt features, or a trash company may have a creature with garbage-themed features, "
            f"and the company's brand colors. The only thing described should be the creature's physical appearance. "
            f"The description should match some sort of creature, animal or monster. The description should NOT include "
            f"the creature name. Creature descriptions MUST contain descriptions of anthropomorphic features, and specifically "
            f"must include eyes. Below is an example for the company Intel Corporation:\n\n"
            f'Example response:\n{{\n    "name": "Intellichip",\n    "description": "A Pokemon creature with a sleek, angular body in blue '
            f'and silver, with circuit patterns across its form. Its sharp eyes glow soft blue, symbolizing data processing '
            f'intelligence. With thin, wiry limbs and connector-like digits, it interfaces with computer hardware. It manipulates '
            f'data streams, controlling information flow, and processes vast data, enhancing its and nearby devices\' cognitive '
            f'capabilities. It\'s in high-tech environments, aiding in computations and data analysis, communicating in binary pulses."\n}}\n\n'
            f"Now, generate a creature for the following company. Ensure your response is valid JSON format.\n"
            f"Company name: {company.get('name')}.\n"
            f"Description: {company.get('description')}.\n"
        )

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "{"},
            ],
        }

        try:
            response = requests.post(self.API_URL, headers=headers, json=data)
            if response.status_code == 200:
                response_data = response.json()
                # Clean and parse the returned JSON string.
                creature_text = response_data["content"][0]["text"].replace("\n", "")
                creature_string = "{" + creature_text
                creature_data = json.loads(creature_string)
                creature_data["ticker"] = company.get("ticker")
                return creature_data
            else:
                logging.error("Claude API returned status code %s: %s", response.status_code, response.text)
        except Exception as e:
            logging.error("Error generating creature data for %s: %s", company.get("ticker"), e)
        return None


class ImageGenerator:
    """
    Generates creature images using the Stability.ai API.
    """

    ENGINE_ID = "stable-diffusion-xl-1024-v1-0"
    BASE_URL_TEMPLATE = "https://api.stability.ai/v1/generation/{engine_id}/text-to-image"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def generate(self, creature: Dict[str, Any]) -> Optional[bytes]:
        """
        Generate an image for the given creature using the Stability.ai API.
        """
        prompt = (
            f"An anime-style drawing of a Pokemon artstation creature that is {creature.get('description')}. "
            f"The art style is 2D, semi-watercolor in a Pokemon-style theme, detailed and energetic on a plain white background."
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        json_data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 832,
            "width": 1216,
            "samples": 1,
            "steps": 40,
        }
        url = self.BASE_URL_TEMPLATE.format(engine_id=self.ENGINE_ID)
        try:
            response = requests.post(url, headers=headers, json=json_data)
            if response.status_code == 200:
                data = response.json()
                image_artifact = data["artifacts"][0]
                return base64.b64decode(image_artifact["base64"])
            else:
                logging.error("Stability API error: %s %s", response.status_code, response.text)
        except Exception as e:
            logging.error("Error generating image: %s", e)
        return None


class CreatureCardApp:
    """
    Main application class that orchestrates fetching data, processing metrics,
    generating creature information and images, and writing the final JSON output.
    """

    OUTPUT_JSON = "final_data.json"
    IMAGE_FOLDER = "creature_images"

    def __init__(
        self,
        alpha_vantage_key: str,
        claude_key: str,
        stability_key: str,
    ) -> None:
        self.alpha_vantage_client = AlphaVantageClient(alpha_vantage_key)
        self.creature_generator = CreatureGenerator(claude_key)
        self.image_generator = ImageGenerator(stability_key)
        self.data_fetcher = CompanyDataFetcher()
        self.card_creator = CardDataCreator()

    def _ensure_image_folder(self) -> None:
        """Ensure that the folder for creature images exists."""
        if not os.path.exists(self.IMAGE_FOLDER):
            os.makedirs(self.IMAGE_FOLDER)
            logging.info("Created folder for creature images: %s", self.IMAGE_FOLDER)

    def run(self) -> None:
        """
        Execute the full workflow:
          1. Fetch company data and metrics.
          2. Generate card data.
          3. Generate creature descriptions and images.
          4. Write final data to JSON.
        """
        self._ensure_image_folder()

        # Step 1: Fetch company data and metrics.
        df = self.data_fetcher.fetch()
        company_metrics = self.alpha_vantage_client.fetch_company_metrics(df)
        if not company_metrics:
            logging.error("No company metrics fetched. Exiting.")
            return

        # Step 2: Generate card data.
        card_data = self.card_creator.create_card_data(company_metrics)

        # Step 3: For each card, generate creature data and image.
        request_count = 0
        start_time = time.time()
        for i, card in enumerate(card_data):
            logging.info("Generating creature data for %s (%d/%d)", card.get("ticker"), i + 1, len(card_data))
            creature = self.creature_generator.generate(card)
            if creature:
                card["creatureName"] = creature.get("name", "")
                image_path = os.path.join(self.IMAGE_FOLDER, f"{card.get('ticker')}.png")
                if os.path.exists(image_path):
                    logging.info("Image for %s already exists.", card.get("ticker"))
                    card["creatureImage"] = image_path
                else:
                    image_bytes = self.image_generator.generate(creature)
                    if image_bytes:
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        logging.info("Saved image for %s at %s", card.get("ticker"), image_path)
                        card["creatureImage"] = image_path
                    else:
                        logging.error("Failed to generate image for %s", card.get("ticker"))
            else:
                logging.error("Failed to generate creature data for %s", card.get("ticker"))

            request_count += 1
            # Rate limiting: after 5 API calls, ensure at least 60 seconds have passed.
            if request_count >= 5:
                elapsed = time.time() - start_time
                if elapsed < 60:
                    time.sleep(60 - elapsed)
                start_time = time.time()
                request_count = 0

        # Step 4: Write final data to JSON.
        try:
            with open(self.OUTPUT_JSON, "w") as f:
                json.dump(card_data, f, indent=2)
            logging.info("Final data written to %s.", self.OUTPUT_JSON)
        except Exception as e:
            logging.error("Error writing JSON output: %s", e)


def main() -> None:
    """
    Main entry point:
      - Loads environment variables.
      - Ensures all required API keys are present.
      - Runs the CreatureCardApp.
    """
    load_dotenv()
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    stability_api_key = os.getenv("STABILITY_API_KEY")

    if not alpha_vantage_api_key:
        logging.error("ALPHA_VANTAGE_API_KEY not set in environment.")
        return
    if not claude_api_key:
        logging.error("CLAUDE_API_KEY not set in environment.")
        return
    if not stability_api_key:
        logging.error("STABILITY_API_KEY not set in environment.")
        return

    app = CreatureCardApp(alpha_vantage_api_key, claude_api_key, stability_api_key)
    app.run()


if __name__ == "__main__":
    main()
