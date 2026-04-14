import re
import requests

# 🌍 Expanded Currency Map (countries included)
CURRENCY_MAP = {
    # Asia
    "pakistan": "PKR",
    "pkr": "PKR",
    "india": "INR",
    "inr": "INR",
    "china": "CNY",
    "yuan": "CNY",
    "japan": "JPY",
    "yen": "JPY",
    "maldives": "MVR",
    "mvr": "MVR",

    # Middle East
    "saudi": "SAR",
    "saudi arabia": "SAR",
    "qatar": "QAR",
    "iran": "IRR",
    "turkey": "TRY",

    # Europe
    "switzerland": "CHF",
    "swiss": "CHF",
    "germany": "EUR",
    "france": "EUR",
    "spain": "EUR",
    "italy": "EUR",
    "poland": "PLN",
    "hungary": "HUF",
    "romania": "RON",

    # North America
    "usa": "USD",
    "us": "USD",
    "canada": "CAD",

    # Default currencies
    "euro": "EUR",
    "eur": "EUR",
    "dollar": "USD",
    "pound": "GBP",
    "uk": "GBP"
}

# 💰 Expensiveness index (for chart)
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


# 🧠 PARSER
def parse_query(text: str):
    text = text.lower()

    amount = re.search(r"\d+(\.\d+)?", text)
    if not amount:
        raise ValueError("No amount found")

    amount = float(amount.group())

    found = []
    for k, v in CURRENCY_MAP.items():
        if k in text:
            found.append(v)

    found = list(dict.fromkeys(found))

    if len(found) < 2:
        raise ValueError("Need 2 currencies")

    return amount, found[0], found[1]


# 🌐 API
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()

    if "rates" not in data:
        raise Exception("API failed")

    return data["rates"][to_c]


# 💱 conversion
def convert_text(query):
    amount, f, t = parse_query(query)
    rate = get_rate(f, t)

    return {
        "amount": amount,
        "from": f,
        "to": t,
        "result": round(amount * rate, 2),
        "rate": rate
    }


# 📊 EXPENSIVENESS DATA (for chart)
def get_expensiveness_data():
    return EXPENSIVE_INDEX
