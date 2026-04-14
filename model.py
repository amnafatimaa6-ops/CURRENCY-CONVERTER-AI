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
    "italy": "EUR",
    "spain": "EUR",
    "belgium": "EUR",
    "greece": "EUR",
    "portugal": "EUR",
    "canada": "CAD",
    "switzerland": "CHF",
    "australia": "AUD",
    "sweden": "SEK",
    "south korea": "KRW",
    "singapore": "SGD",
    "malaysia": "MYR",
    "saudi arabia": "SAR",
    "qatar": "QAR",
    "uae": "AED",
    "turkey": "TRY",
    "iraq": "IQD",
    "jordan": "JOD",
    "hungary": "HUF",
    "poland": "PLN",
    "romania": "RON",
    "maldives": "MVR",
    "iran": "IRR"
}

# 🌍 Currency Info
CURRENCY_INFO = {
    "PKR": {"name": "Pakistani Rupee", "country": "Pakistan", "strength": 2},
    "INR": {"name": "Indian Rupee", "country": "India", "strength": 3},
    "CNY": {"name": "Chinese Yuan", "country": "China", "strength": 6},
    "JPY": {"name": "Japanese Yen", "country": "Japan", "strength": 7},
    "USD": {"name": "US Dollar", "country": "United States", "strength": 9},
    "GBP": {"name": "British Pound", "country": "United Kingdom", "strength": 9},
    "EUR": {"name": "Euro", "country": "Europe", "strength": 8},
    "CAD": {"name": "Canadian Dollar", "country": "Canada", "strength": 8},
    "CHF": {"name": "Swiss Franc", "country": "Switzerland", "strength": 10},
    "AUD": {"name": "Australian Dollar", "country": "Australia", "strength": 8},
    "SEK": {"name": "Swedish Krona", "country": "Sweden", "strength": 8},
    "KRW": {"name": "South Korean Won", "country": "South Korea", "strength": 7},
    "SGD": {"name": "Singapore Dollar", "country": "Singapore", "strength": 9},
    "MYR": {"name": "Malaysian Ringgit", "country": "Malaysia", "strength": 5},
    "SAR": {"name": "Saudi Riyal", "country": "Saudi Arabia", "strength": 5},
    "QAR": {"name": "Qatari Riyal", "country": "Qatar", "strength": 6},
    "AED": {"name": "UAE Dirham", "country": "UAE", "strength": 7},
    "TRY": {"name": "Turkish Lira", "country": "Turkey", "strength": 4},
    "IQD": {"name": "Iraqi Dinar", "country": "Iraq", "strength": 2},
    "JOD": {"name": "Jordanian Dinar", "country": "Jordan", "strength": 6},
    "HUF": {"name": "Hungarian Forint", "country": "Hungary", "strength": 4},
    "PLN": {"name": "Polish Złoty", "country": "Poland", "strength": 5},
    "RON": {"name": "Romanian Leu", "country": "Romania", "strength": 4},
    "MVR": {"name": "Maldivian Rufiyaa", "country": "Maldives", "strength": 5},
    "IRR": {"name": "Iranian Rial", "country": "Iran", "strength": 1}
}


# 🌍 MAP DATA
def get_country_strength_map():
    return {v["country"]: v["strength"] for v in CURRENCY_INFO.values()}


# 🌐 FX API
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()
    return data["rates"][to_c]


# 🧠 PARSER
def parse_query(text):
    text = text.lower()

    import re
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


# 💱 CONVERTER
def convert(query):
    parsed = parse_query(query)

    if not parsed:
        return {"error": "Invalid input format"}

    amount, from_c, to_c = parsed

    rate = get_rate(from_c, to_c)
    result = round(amount * rate, 2)

    f = CURRENCY_INFO[from_c]
    t = CURRENCY_INFO[to_c]

    ratio = round(t["strength"] / f["strength"], 2)

    insight = [
        f"{f['name']} ({f['country']}) → {t['name']} ({t['country']})",
        f"{t['name']} is {ratio}x stronger than {f['name']}."
    ]

    return {
        "from": from_c,
        "to": to_c,
        "amount": amount,
        "rate": rate,
        "result": result,
        "insight": insight
    }


# 📊 DATA
def get_strength_data():
    return {k: v["strength"] for k, v in CURRENCY_INFO.items()}
