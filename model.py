import re
import requests

# 🌍 Country → Currency mapping
CURRENCY_MAP = {
    "pakistan": "PKR",
    "pkr": "PKR",

    "india": "INR",
    "inr": "INR",

    "china": "CNY",
    "japan": "JPY",

    "usa": "USD",
    "us": "USD",

    "uk": "GBP",

    "germany": "EUR",
    "france": "EUR",
    "spain": "EUR",
    "italy": "EUR",

    "canada": "CAD",
    "switzerland": "CHF",

    "saudi": "SAR",
    "qatar": "QAR",

    "turkey": "TRY",
    "hungary": "HUF",
    "romania": "RON",
    "poland": "PLN",

    "maldives": "MVR",
    "iran": "IRR"
}

# 🌍 NEW: Currency → Country mapping (REVERSE LOOKUP)
CURRENCY_TO_COUNTRY = {
    "PKR": "Pakistan",
    "INR": "India",
    "CNY": "China",
    "JPY": "Japan",
    "USD": "United States",
    "GBP": "United Kingdom",
    "EUR": "Eurozone (Germany, France, Spain, Italy etc.)",
    "CAD": "Canada",
    "CHF": "Switzerland",
    "SAR": "Saudi Arabia",
    "QAR": "Qatar",
    "TRY": "Turkey",
    "HUF": "Hungary",
    "RON": "Romania",
    "PLN": "Poland",
    "MVR": "Maldives",
    "IRR": "Iran"
}

# 📊 Expensiveness index
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


# 🧠 Parse input
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


# 💱 Convert
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


# 📊 chart data
def get_expensiveness_data():
    return EXPENSIVE_INDEX


# 🌍 NEW: currency → country info
def get_currency_country(currency_code):
    return CURRENCY_TO_COUNTRY.get(currency_code, "Unknown")
