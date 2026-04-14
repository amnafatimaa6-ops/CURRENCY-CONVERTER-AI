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
    "IRR": "Iranian Rial → Iran 🇮🇷",
    "MVR": "Maldivian Rufiyaa → Maldives 🇲🇻",
    "CNY": "Chinese Yuan → China 🇨🇳",
    "CAD": "Canadian Dollar → Canada 🇨🇦",
    "JPY": "Japanese Yen → Japan 🇯🇵",
    "PKR": "Pakistani Rupee → Pakistan 🇵🇰",
    "GBP": "British Pound → United Kingdom 🇬🇧",
    "HUF": "Hungarian Forint → Hungary 🇭🇺",
    "PLN": "Polish Złoty → Poland 🇵🇱",
    "TRY": "Turkish Lira → Turkey 🇹🇷",
    "QAR": "Qatari Riyal → Qatar 🇶🇦",
    "RON": "Romanian Leu → Romania 🇷🇴",
    "EUR": "Euro → Eurozone 🇪🇺",
    "SAR": "Saudi Riyal → Saudi Arabia 🇸🇦",
    "INR": "Indian Rupee → India 🇮🇳",
    "CHF": "Swiss Franc → Switzerland 🇨🇭",
    "USD": "US Dollar → United States 🇺🇸"
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


# 🧠 SMART PARSER (FIXED)
def parse_query(text: str):
    text = text.lower()

    # extract number
    amount_match = re.search(r"\d+(\.\d+)?", text)
    if not amount_match:
        raise ValueError("No amount found")

    amount = float(amount_match.group())

    # clean separators
    cleaned = text.replace("to", " ").replace("in", " ")
    words = cleaned.split()

    found = []

    for w in words:
        w = w.strip()

        # direct currency match
        if w.upper() in CURRENCY_FULL_INFO:
            found.append(w.upper())

        # country → currency
        if w in CURRENCY_MAP:
            found.append(CURRENCY_MAP[w])

    # remove duplicates
    found = list(dict.fromkeys(found))

    if len(found) < 2:
        raise ValueError("Invalid input. Example: 10 pkr to usd")

    return amount, found[0], found[1]


# 🌐 API
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()

    if "rates" not in data:
        raise Exception("API error")

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


# 🌍 full currency info
def get_currency_full_list():
    return CURRENCY_FULL_INFO
