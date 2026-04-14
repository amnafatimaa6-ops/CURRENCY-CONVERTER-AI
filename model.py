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

# 🌍 Currency Intelligence Layer
CURRENCY_INFO = {
    "PKR": {"name": "Pakistani Rupee", "strength": 2},
    "INR": {"name": "Indian Rupee", "strength": 3},
    "CNY": {"name": "Chinese Yuan", "strength": 6},
    "JPY": {"name": "Japanese Yen", "strength": 7},
    "USD": {"name": "US Dollar", "strength": 9},
    "GBP": {"name": "British Pound", "strength": 9},
    "EUR": {"name": "Euro", "strength": 8},
    "CAD": {"name": "Canadian Dollar", "strength": 8},
    "CHF": {"name": "Swiss Franc", "strength": 10},
    "SAR": {"name": "Saudi Riyal", "strength": 5},
    "QAR": {"name": "Qatari Riyal", "strength": 6},
    "TRY": {"name": "Turkish Lira", "strength": 4},
    "HUF": {"name": "Hungarian Forint", "strength": 4},
    "PLN": {"name": "Polish Złoty", "strength": 5},
    "RON": {"name": "Romanian Leu", "strength": 4},
    "MVR": {"name": "Maldivian Rufiyaa", "strength": 5},
    "IRR": {"name": "Iranian Rial", "strength": 1}
}


# 🌐 FX API
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()
    return data["rates"][to_c]


# 🧠 SMART PARSER (ROBUST)
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


# 💱 MAIN ENGINE
def convert(query):
    parsed = parse_query(query)

    if not parsed:
        return {"error": "Invalid input format"}

    amount, from_c, to_c = parsed

    rate = get_rate(from_c, to_c)
    result = round(amount * rate, 2)

    from_strength = CURRENCY_INFO[from_c]["strength"]
    to_strength = CURRENCY_INFO[to_c]["strength"]

    comparison = round(to_strength / from_strength, 2)

    insight = []

    insight.append(
        f"{CURRENCY_INFO[to_c]['name']} is {comparison}x stronger than {CURRENCY_INFO[from_c]['name']} (based on economic index)."
    )

    if comparison > 1:
        insight.append("Your destination currency has higher purchasing power 💰")
    else:
        insight.append("Your source currency holds stronger value 💵")

    if amount > 1000:
        insight.append("High-value international transaction 🌍")

    return {
        "from": from_c,
        "to": to_c,
        "amount": amount,
        "rate": rate,
        "result": result,
        "insight": insight
    }


# 📊 DASHBOARD DATA
def get_strength_data():
    return {k: v["strength"] for k, v in CURRENCY_INFO.items()}
