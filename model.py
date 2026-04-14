import re
import requests

# 🌍 Country → Currency mapping
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

# 🌍 FULL CURRENCY DISPLAY INFO
CURRENCY_FULL_INFO = {
    "IRR": "Iranian Rial → Iran 🇮🇷",
    "MVR": "Maldivian Rufiyaa → Maldives 🇲🇻",
    "CNY": "Chinese Yuan (Renminbi) → China 🇨🇳",
    "CAD": "Canadian Dollar → Canada 🇨🇦",
    "JPY": "Japanese Yen → Japan 🇯🇵",
    "PKR": "Pakistani Rupee → Pakistan 🇵🇰",
    "GBP": "British Pound Sterling → United Kingdom 🇬🇧",
    "HUF": "Hungarian Forint → Hungary 🇭🇺",
    "PLN": "Polish Złoty → Poland 🇵🇱",
    "TRY": "Turkish Lira → Turkey 🇹🇷",
    "QAR": "Qatari Riyal → Qatar 🇶🇦",
    "RON": "Romanian Leu → Romania 🇷🇴",
    "EUR": "Euro → Eurozone (Germany, France, Spain, Italy) 🇪🇺",
    "SAR": "Saudi Riyal → Saudi Arabia 🇸🇦",
    "INR": "Indian Rupee → India 🇮🇳",
    "CHF": "Swiss Franc → Switzerland 🇨🇭",
    "USD": "US Dollar → United States 🇺🇸"
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

# 🧠 Parse user input
def parse_query(text: str):
    text = text.lower()

    amount = re.search(r"\d+(\.\d+)?", text)
    if not amount:
        raise ValueError("No amount found in input")

    amount = float(amount.group())

    found = []
    for k, v in CURRENCY_MAP.items():
        if k in text:
            found.append(v)

    found = list(dict.fromkeys(found))

    if len(found) < 2:
        raise ValueError("Need 2 currencies or countries in query")

    return amount, found[0], found[1]


# 🌐 Live FX API
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


# 🌍 full currency list (UI)
def get_currency_full_list():
    return CURRENCY_FULL_INFO
