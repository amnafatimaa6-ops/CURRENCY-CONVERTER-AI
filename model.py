import re
import requests

# ---------- DATA ----------
CURRENCY_MAP = {
    "pakistan": "PKR", "india": "INR", "china": "CNY",
    "japan": "JPY", "usa": "USD", "uk": "GBP",
    "germany": "EUR", "france": "EUR", "spain": "EUR", "italy": "EUR",
    "canada": "CAD", "switzerland": "CHF",
    "saudi": "SAR", "qatar": "QAR",
    "turkey": "TRY", "hungary": "HUF",
    "poland": "PLN", "romania": "RON",
    "maldives": "MVR", "iran": "IRR"
}

CURRENCY_FULL = {
    "PKR": "Pakistani Rupee 🇵🇰",
    "INR": "Indian Rupee 🇮🇳",
    "USD": "US Dollar 🇺🇸",
    "EUR": "Euro 🇪🇺",
    "GBP": "British Pound 🇬🇧",
    "JPY": "Japanese Yen 🇯🇵",
    "CHF": "Swiss Franc 🇨🇭",
    "CAD": "Canadian Dollar 🇨🇦",
    "CNY": "Chinese Yuan 🇨🇳",
    "TRY": "Turkish Lira 🇹🇷",
    "RON": "Romanian Leu 🇷🇴",
    "HUF": "Hungarian Forint 🇭🇺",
    "PLN": "Polish Złoty 🇵🇱",
    "SAR": "Saudi Riyal 🇸🇦",
    "QAR": "Qatari Riyal 🇶🇦",
    "MVR": "Maldivian Rufiyaa 🇲🇻",
    "IRR": "Iranian Rial 🇮🇷"
}

EXPENSIVE_INDEX = {
    "CHF": 10, "USD": 9, "GBP": 9, "EUR": 8,
    "CAD": 8, "JPY": 7, "CNY": 6,
    "SAR": 5, "QAR": 6, "TRY": 4,
    "PLN": 5, "HUF": 4, "RON": 4,
    "INR": 3, "PKR": 2, "MVR": 5, "IRR": 1
}


# ---------- FX ----------
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()
    return data["rates"][to_c]


# ---------- SMART PARSER ----------
def extract_currencies(text):
    text = text.lower()
    found = []

    for word in text.split():
        if word.upper() in CURRENCY_FULL:
            found.append(word.upper())
        if word in CURRENCY_MAP:
            found.append(CURRENCY_MAP[word])

    found = list(dict.fromkeys(found))
    return found


def extract_amount(text):
    match = re.search(r"\d+(\.\d+)?", text)
    return float(match.group()) if match else None


# ---------- AI ENGINE ----------
def ai_engine(query):
    amount = extract_amount(query)
    currencies = extract_currencies(query)

    if not amount or len(currencies) < 2:
        return {
            "type": "error",
            "message": "Try: 100 pkr to usd or 50 yen to euro"
        }

    from_c, to_c = currencies[0], currencies[1]

    rate = get_rate(from_c, to_c)
    result = round(amount * rate, 2)

    strength_ratio = EXPENSIVE_INDEX[to_c] / EXPENSIVE_INDEX[from_c]

    explanation = []

    if strength_ratio > 1:
        explanation.append(f"{CURRENCY_FULL[to_c]} is stronger than {CURRENCY_FULL[from_c]} by ~{round(strength_ratio,2)}x.")
    else:
        explanation.append(f"{CURRENCY_FULL[from_c]} is stronger or similar in value.")

    if amount > 1000:
        explanation.append("Large international transaction detected 🌍")
    elif amount < 20:
        explanation.append("Small spending amount 💸")

    explanation.append(f"{amount} {from_c} = {result} {to_c}")

    return {
        "type": "success",
        "from": from_c,
        "to": to_c,
        "amount": amount,
        "result": result,
        "rate": rate,
        "explanation": explanation
    }
