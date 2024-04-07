import json


def find_larger_index(value, array):
    for i, n in enumerate(array):
        if n >= value:
            return i
    return len(array)


def get_percentile_finder(data, groups):
    cutoffs = []
    data.sort()
    for i in range(len(data) // groups, len(data), len(data) // groups):
        cutoffs.append(data[i])

    def get_percentile(value):
        return find_larger_index(value, cutoffs)

    return get_percentile


with open('company_data.json', 'r') as file:
    data = json.load(file)

market_caps = [item['marketCap'] if item['marketCap'] is not None else 1 for item in data]
free_cash_flows = [item['freeCashFlow'] if item['freeCashFlow'] is not None else 0 for item in data]
shareholder_equities = [item['shareholderEquity'] if item['shareholderEquity'] is not None else 1 for item in data]

market_cap_grouper = get_percentile_finder(market_caps, 10)
free_cash_flow_grouper = get_percentile_finder(free_cash_flows, 10)
shareholder_equity_grouper = get_percentile_finder(shareholder_equities, 10)

converted_data = []
for item in data:
    health = market_cap_grouper(item['marketCap'] if item['marketCap'] is not None else 0)
    attack = free_cash_flow_grouper(item['freeCashFlow'] if item['freeCashFlow'] is not None else 0)
    defense = shareholder_equity_grouper(item['shareholderEquity'] if item['shareholderEquity'] is not None else 0)
    growth = item['earningsGrowth'] if item['earningsGrowth'] is not None else 0

    health =  [24, 28, 30, 35, 40, 45, 50, 55, 60, 80, 80][health]
    attack =  [5,  7,  9,  11,  13, 15, 16, 17, 20, 24, 24][attack]
    defense = [1,  2,  3,  4,  5,  6,  7,  8,  9,  11, 11][defense]
    growth = max(2, min(round(growth * 10) + 5, 15))

    converted_data.append({
        'ticker': item['ticker'],
        'health': health,
        'attack': attack,
        'growth': growth,
        'defense': defense,
        'name': item['companyName'],
        'sector': item['sector']
    })

with open('card_data.json', 'w') as file:
    json.dump(converted_data, file, indent=2)

print("Conversion completed. Results saved to 'card_data.json'.")
