import re
import requests

# 🌍 Currency + Country mapping
CURRENCY_MAP = {
    "pakistan": "PKR",
    "pkr": "PKR",

    "india": "INR",
    "inr": "INR",

    "china": "CNY",
    "yuan": "CNY",

    "japan": "JPY",
    "yen": "JPY",

    "usa": "USD",
    "us": "USD",
    "dollar": "USD",
    "usd": "USD",

    "uk": "GBP",
    "britain": "GBP",
    "pound": "GBP",

    "euro": "EUR",
    "eur": "EUR",
    "germany": "EUR",
    "france": "EUR",
    "spain": "EUR",
    "italy": "EUR",

    "canada": "CAD",
    "cad": "CAD",

    "switzerland": "CHF",
    "swiss": "CHF",

    "saudi": "SAR",
    "qatar": "QAR",

    "turkey": "TRY",
    "lira": "TRY",

    "hungary": "HUF",
    "romania": "RON",
    "poland": "PLN",

    "maldives": "MVR",
    "iran": "IRR"
}

# 📊 Expensiveness index (for chart)
EXPENSIVE_INDEX = {
    "CHF": 10,
    "USD": 9,
    "GBP": 9,
    "EUR": 8,
    "CAD": 8,
    "JPY": 7,
    "CNY": 6,
    "SAR": 5,
    "QAR": 6,
    "TRY": 4,
    "PLN": 5,
    "HUF": 4,
    "RON": 4,
    "INR": 3,
    "PKR": 2,
    "MVR": 5,
    "IRR": 1
}


# 🧠 Parse input text
def parse_query(text: str):
    text = text.lower()

    amount_match = re.search(r"\d+(\.\d+)?", text)
    if not amount_match:
        raise ValueError("No amount found")

    amount = float(amount_match.group())

    found = []
    for key, value in CURRENCY_MAP.items():
        if key in text:
            found.append(value)

    found = list(dict.fromkeys(found))

    if len(found) < 2:
        raise ValueError("Could not detect 2 currencies/countries")

    return amount, found[0], found[1]


# 🌐 Live FX API
def get_rate(from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    data = requests.get(url).json()

    if "rates" not in data:
        raise Exception("API failed or blocked")

    return data["rates"][to_currency]


# 💱 Convert
def convert_text(query: str):
    amount, f, t = parse_query(query)
    rate = get_rate(f, t)

    return {
        "amount": amount,
        "from": f,
        "to": t,
        "result": round(amount * rate, 2),
        "rate": rate
    }


# 📊 Chart data
def get_expensiveness_data():
    return EXPENSIVE_INDEX


# 🌍 Currency list for UI
def get_currency_list():
    return sorted(set(CURRENCY_MAP.values()))
