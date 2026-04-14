import re
import requests

# 🌍 Country → Currency
CURRENCY_MAP = {
    "pakistan": "PKR",
    "india": "INR",
    "china": "CNY",
    "japan": "JPY",
    "usa": "USD",
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
    "poland": "PLN",
    "romania": "RON",
    "maldives": "MVR",
    "iran": "IRR"
}

# 🌍 Economic strength (proxy index)
CURRENCY_INFO = {
    "PKR": {"name": "Pakistan", "strength": 2},
    "INR": {"name": "India", "strength": 3},
    "CNY": {"name": "China", "strength": 6},
    "JPY": {"name": "Japan", "strength": 7},
    "USD": {"name": "USA", "strength": 9},
    "GBP": {"name": "UK", "strength": 9},
    "EUR": {"name": "Eurozone", "strength": 8},
    "CAD": {"name": "Canada", "strength": 8},
    "CHF": {"name": "Switzerland", "strength": 10},
    "SAR": {"name": "Saudi", "strength": 5},
    "QAR": {"name": "Qatar", "strength": 6},
    "TRY": {"name": "Turkey", "strength": 4},
    "HUF": {"name": "Hungary", "strength": 4},
    "PLN": {"name": "Poland", "strength": 5},
    "RON": {"name": "Romania", "strength": 4},
    "MVR": {"name": "Maldives", "strength": 5},
    "IRR": {"name": "Iran", "strength": 1}
}


# 🌐 FX API
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()
    return data["rates"][to_c]


# 🧠 parser
def parse_query(text):
    text = text.lower()

    amount = re.search(r"\d+(\.\d+)?", text)
    if not amount:
        return None

    amount = float(amount.group())

    found = []

    for k, v in CURRENCY_MAP.items():
        if k in text:
            found.append(v)

    for c in CURRENCY_INFO.keys():
        if c.lower() in text:
            found.append(c)

    found = list(dict.fromkeys(found))

    if len(found) < 2:
        return None

    return amount, found[0], found[1]


# 💱 conversion + intelligence
def convert(query):
    parsed = parse_query(query)

    if not parsed:
        return {"error": "Invalid input format"}

    amount, from_c, to_c = parsed

    rate = get_rate(from_c, to_c)
    result = round(amount * rate, 2)

    f_strength = CURRENCY_INFO[from_c]["strength"]
    t_strength = CURRENCY_INFO[to_c]["strength"]

    ratio = round(t_strength / f_strength, 2)

    insight = []

    insight.append(f"{CURRENCY_INFO[to_c]['name']} is {ratio}x stronger than {CURRENCY_INFO[from_c]['name']}.")

    if ratio > 1:
        insight.append("Destination country has higher purchasing power 💰")
    else:
        insight.append("Source currency has stronger economic value 💵")

    if amount >= 1000:
        insight.append("High-value financial transaction detected 🌍")
    elif amount <= 20:
        insight.append("Small-scale personal spending 💸")

    return {
        "from": from_c,
        "to": to_c,
        "amount": amount,
        "rate": rate,
        "result": result,
        "insight": insight,
        "ratio": ratio
    }


# 📊 strength dataset
def get_strength_data():
    return {k: v["strength"] for k, v in CURRENCY_INFO.items()}
