import json
from yolo.helpers.constants import YAHOO_TRAVEL_TICKERS

# Load the JSON data
with open("data/travel_screener_yf.json", "r") as file:
    data = json.load(file)

# Extract the symbols
symbols = [quote["symbol"] for quote in data["finance"]["result"][0]["quotes"]]

# Print or use the symbols as needed

# deduplicate the symbols: YAHOO_TRAVEL_TICKERS
symbols = list(set(YAHOO_TRAVEL_TICKERS))
print(symbols)
