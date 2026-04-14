# model.py

import re
import requests

# ---------- MASTER CURRENCY REGISTRY ----------
CURRENCY_MAP = {
    # Pakistan
    "pkr": "PKR",
    "rupee": "PKR",
    "rupees": "PKR",
    "pakistani rupee": "PKR",

    # India
    "inr": "INR",
    "indian rupee": "INR",

    # China
    "cny": "CNY",
    "yuan": "CNY",
    "renminbi": "CNY",

    # Japan
    "jpy": "JPY",
    "yen": "JPY",

    # USA
    "usd": "USD",
    "dollar": "USD",
    "dollars": "USD",
    "us dollar": "USD",

    # UK
    "gbp": "GBP",
    "pound": "GBP",
    "pounds": "GBP",
    "british pound": "GBP",

    # Europe (Eurozone countries)
    "eur": "EUR",
    "euro": "EUR",
    "euros": "EUR",
    "germany": "EUR",
    "france": "EUR",
    "spain": "EUR",
    "italy": "EUR",

    # Hungary
    "hungary": "HUF",
    "forint": "HUF",
    "huf": "HUF",

    # Romania
    "romania": "RON",
    "ron": "RON",
    "leu": "RON",

    # Turkey
    "turkey": "TRY",
    "turkish lira": "TRY",
    "lira": "TRY",
    "try": "TRY",

    # Poland
    "poland": "PLN",
    "pln": "PLN",
    "zloty": "PLN",
}


# ---------- SMART PARSER ----------
def parse_query(text: str):
    text = text.lower()

    # extract number
    amount_match = re.search(r"\d+(\.\d+)?", text)
    if not amount_match:
        raise ValueError("No amount found")

    amount = float(amount_match.group())

    # detect currencies mentioned
    found = []

    for key, value in CURRENCY_MAP.items():
        if key in text:
            found.append(value)

    # remove duplicates while keeping order
    found = list(dict.fromkeys(found))

    if len(found) < 2:
        raise ValueError("Could not detect 2 currencies clearly")

    return amount, found[0], found[1]


# ---------- LIVE RATE ENGINE ----------
def get_rate(from_currency: str, to_currency: str):
    url = f"https://api.exchangerate.host/latest?base={from_currency}&symbols={to_currency}"
    data = requests.get(url).json()

    return data["rates"][to_currency]


# ---------- CORE FUNCTION ----------
def convert_text(query: str):
    amount, from_curr, to_curr = parse_query(query)

    rate = get_rate(from_curr, to_curr)
    result = round(amount * rate, 2)

    return {
        "input": f"{amount} {from_curr}",
        "output": f"{result} {to_curr}",
        "rate": rate,
        "path": f"{from_curr} → {to_curr}"
    }
