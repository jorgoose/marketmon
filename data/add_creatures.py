# For each creature in creature_data.json, we will attempt to add the creature information to the corresponding card_data.json entry
# Correpsponding entries are determined by matching the 'ticker' field in creature_data.json to the 'ticker' field in card_data.json
# If a match is found, the creature name should be added to the card_data.json entry as "creatureName"

import json

# Load the creature data
with open('creature_data.json', 'r') as f:
    creature_data = json.load(f)

# Load the card data
with open('card_data.json', 'r') as f:
    card_data = json.load(f)

# Loop through each creature in the creature data
for creature in creature_data:
    # Loop through each card in the card data
    for card in card_data:
        # Check if the tickers match
        print(f'Matching C{creature["ticker"]} with card {card["ticker"]}')
        if creature['ticker'] == card['ticker']:
            # Add the creature name to the card data
            card['creatureName'] = creature['name']

# Save the updated card data
with open('card_data.json', 'w') as f:
    json.dump(card_data, f, indent=2)

print("Creature information added to card data.")