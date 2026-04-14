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

# 🌍 Currency → Full Info
CURRENCY_FULL_INFO = {
    "PKR": "Pakistani Rupee → Pakistan 🇵🇰",
    "INR": "Indian Rupee → India 🇮🇳",
    "CNY": "Chinese Yuan → China 🇨🇳",
    "JPY": "Japanese Yen → Japan 🇯🇵",
    "USD": "US Dollar → United States 🇺🇸",
    "GBP": "British Pound → United Kingdom 🇬🇧",
    "EUR": "Euro → Eurozone 🇪🇺",
    "CAD": "Canadian Dollar → Canada 🇨🇦",
    "CHF": "Swiss Franc → Switzerland 🇨🇭",
    "SAR": "Saudi Riyal → Saudi Arabia 🇸🇦",
    "QAR": "Qatari Riyal → Qatar 🇶🇦",
    "TRY": "Turkish Lira → Turkey 🇹🇷",
    "HUF": "Hungarian Forint → Hungary 🇭🇺",
    "PLN": "Polish Złoty → Poland 🇵🇱",
    "RON": "Romanian Leu → Romania 🇷🇴",
    "MVR": "Maldivian Rufiyaa → Maldives 🇲🇻",
    "IRR": "Iranian Rial → Iran 🇮🇷"
}

# 📊 Expensiveness Index
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

# 🧠 FIXED PARSER (ROBUST)
def parse_query(text: str):
    text = text.lower()

    # 💰 amount
    amount_match = re.search(r"\d+(\.\d+)?", text)
    if not amount_match:
        raise ValueError("Enter amount like 10 pkr to usd")

    amount = float(amount_match.group())

    # 🧹 clean text
    cleaned = text.replace("to", " ")
    words = cleaned.split()

    found = []

    for w in words:
        w = w.strip()

        # currency code match
        if w.upper() in CURRENCY_FULL_INFO:
            found.append(w.upper())

        # country → currency
        if w in CURRENCY_MAP:
            found.append(CURRENCY_MAP[w])

    # remove duplicates
    found = list(dict.fromkeys(found))

    # 🔥 fallback scan (fixes your error)
    if len(found) < 2:
        for k, v in CURRENCY_MAP.items():
            if k in text:
                found.append(v)

        found = list(dict.fromkeys(found))

    if len(found) < 2:
        raise ValueError("Need 2 currencies (example: 10 pkr to usd)")

    return amount, found[0], found[1]


# 🌐 API
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()
    return data["rates"][to_c]


# 💱 convert
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


# 📊 chart
def get_expensiveness_data():
    return EXPENSIVE_INDEX


# 🌍 full names
def get_currency_full_list():
    return CURRENCY_FULL_INFO
