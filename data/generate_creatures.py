import json
import dotenv
import requests
import os
import time

# Load the .env file
dotenv.load_dotenv()

# Load in JSON data from the company_data.json file
with open('company_data.json', 'r') as f:
    company_data = json.load(f)

# Load in existing creature data
try:
    with open('creature_data.json', 'r') as f:
        existing_creature_data = json.load(f)
except FileNotFoundError:
    existing_creature_data = []

# Create a map of tickers to check for existing creature data
existing_tickers = {creature['ticker']: creature for creature in existing_creature_data}

def append_to_json(file, data):
    with open(file, 'r+') as f:
        file_data = json.load(f)
        file_data.append(data)
        f.seek(0)
        json.dump(file_data, f, indent=4)

def generate_creature_data(company):
    prompt = f"""
    Given the company name and the description of the company, generate a description of a Pokemon creature that represents the company. The creature should have a name (similar to a Pokemon name) and a description. Physical features described should directly relate to the company's business or industry, i.e., an electric company may have a creature with lightning bolt features, or a trash company may have a creature with garbage-themed features, and the company's brand colors. The only thing described should be the creature's physical appearance. The description should match some sort of creature, animal or monster. The description should NOT include the creature name.
    Creature descriptions MUST contain descriptions of anthropomorphic features, and specifically must include eyes. Below is an example for the company Intel Corporation:

    Example response:
    {{
        'name': 'Intellichip',
        'description': 'A Pokemon creature with a sleek, angular body in blue and silver, with circuit patterns across its form. Its sharp eyes glow soft blue, symbolizing data processing intelligence. With thin, wiry limbs and connector-like digits, it interfaces with computer hardware. It manipulates data streams, controlling information flow, and processes vast data, enhancing its and nearby devices' cognitive capabilities. It's in high-tech environments, aiding in computations and data analysis, communicating in binary pulses.',
    }}

    Now, generate a creature for the next company given. Ensure your response is valid JSON format.
    Company name: {company['companyName']}. Description: {company['description']}.
    """
    headers = {
        'x-api-key': os.getenv('CLAUDE_API_KEY'),
        'content-type': 'application/json',
        'anthropic-version': '2023-06-01'
    }

    data = {
        'model': 'claude-3-haiku-20240307',
        'max_tokens': 1024,
        'messages': [
            {
                'role': 'user',
                'content': prompt
            },
            {
                "role": "assistant",
                "content": "{"
            }
        ]
    }

    response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        creature_string = "{" + response_data['content'][0]['text'].replace("\n", "")
        try:
            creature_data = json.loads(creature_string)
            creature_data['ticker'] = company['ticker']
            return creature_data
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
            print("Faulty JSON string:", creature_string)
            return None
    else:
        print(f'Non-200 status code: {response.status_code}')
        print(response.text)

def main():
    start_time = time.time()

    for index, company in enumerate(company_data):
        if company['ticker'] in existing_tickers:
            # print(f"Creature data for {company['companyName']} already exists.")
            continue

        if index % 5 == 0 and index != 0:
            time_elapsed = time.time() - start_time
            if time_elapsed < 60:
                time.sleep(60 - time_elapsed)
            start_time = time.time()

        
        print(f"Generating creature data for {company['companyName']}")
        generated_creature_data = generate_creature_data(company)

        if generated_creature_data:
            append_to_json('creature_data.json', generated_creature_data)
            print(f"Saved creature data for {company['companyName']}")
        else:
            print(f"Failed to generate creature data for {company['companyName']}")

    print("Generation completed.")

if __name__ == "__main__":
    main()
