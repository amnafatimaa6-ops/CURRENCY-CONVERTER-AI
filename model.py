import re
import requests

# 🌍 Country → Currency (EXPANDED)
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
    "belgium": "EUR",
    "greece": "EUR",
    "portugal": "EUR",

    "canada": "CAD",
    "switzerland": "CHF",
    "australia": "AUD",
    "sweden": "SEK",
    "mexico": "MXN",

    "south korea": "KRW",
    "north korea": "KPW",
    "singapore": "SGD",
    "malaysia": "MYR",

    "saudi": "SAR",
    "qatar": "QAR",
    "turkey": "TRY",
    "iraq": "IQD",
    "jordan": "JOD",

    "hungary": "HUF",
    "poland": "PLN",
    "romania": "RON",
    "maldives": "MVR",
    "iran": "IRR"
}

# 🌍 Currency Intelligence Layer
CURRENCY_INFO = {
    "PKR": {"name": "Pakistani Rupee", "country": "Pakistan", "strength": 2},
    "INR": {"name": "Indian Rupee", "country": "India", "strength": 3},
    "CNY": {"name": "Chinese Yuan", "country": "China", "strength": 6},
    "JPY": {"name": "Japanese Yen", "country": "Japan", "strength": 7},
    "USD": {"name": "US Dollar", "country": "USA", "strength": 9},
    "GBP": {"name": "British Pound", "country": "UK", "strength": 9},

    "EUR": {"name": "Euro", "country": "Europe", "strength": 8},
    "CAD": {"name": "Canadian Dollar", "country": "Canada", "strength": 8},
    "CHF": {"name": "Swiss Franc", "country": "Switzerland", "strength": 10},
    "AUD": {"name": "Australian Dollar", "country": "Australia", "strength": 8},
    "SEK": {"name": "Swedish Krona", "country": "Sweden", "strength": 8},
    "MXN": {"name": "Mexican Peso", "country": "Mexico", "strength": 5},

    "KRW": {"name": "South Korean Won", "country": "South Korea", "strength": 7},
    "KPW": {"name": "North Korean Won", "country": "North Korea", "strength": 1},
    "SGD": {"name": "Singapore Dollar", "country": "Singapore", "strength": 9},
    "MYR": {"name": "Malaysian Ringgit", "country": "Malaysia", "strength": 5},

    "SAR": {"name": "Saudi Riyal", "country": "Saudi Arabia", "strength": 5},
    "QAR": {"name": "Qatari Riyal", "country": "Qatar", "strength": 6},
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
    return {
        "Pakistan": 2,
        "India": 3,
        "China": 6,
        "Japan": 7,
        "United States": 9,
        "United Kingdom": 9,

        "Germany": 8,
        "France": 8,
        "Spain": 8,
        "Italy": 8,
        "Belgium": 8,
        "Greece": 7,
        "Portugal": 7,

        "Canada": 8,
        "Switzerland": 10,
        "Australia": 8,
        "Sweden": 8,
        "Mexico": 5,

        "South Korea": 7,
        "North Korea": 1,
        "Singapore": 9,
        "Malaysia": 5,

        "Saudi Arabia": 5,
        "Qatar": 6,
        "Turkey": 4,
        "Iraq": 2,
        "Jordan": 6,

        "Hungary": 4,
        "Poland": 5,
        "Romania": 4,
        "Maldives": 5,
        "Iran": 1
    }


# 🌐 FX API
def get_rate(from_c, to_c):
    url = f"https://open.er-api.com/v6/latest/{from_c}"
    data = requests.get(url).json()
    return data["rates"][to_c]


# 🧠 PARSER
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

    f = CURRENCY_INFO[from_c]
    t = CURRENCY_INFO[to_c]

    ratio = round(t["strength"] / f["strength"], 2)

    insight = [
        f"{t['name']} ({t['country']}) is {ratio}x stronger than {f['name']} ({f['country']}).",
        f"Currency Mapping: {from_c} → {f['name']} ({f['country']}) | {to_c} → {t['name']} ({t['country']})"
    ]

    if ratio > 1:
        insight.append("Destination currency has higher purchasing power 💰")
    else:
        insight.append("Source currency holds stronger economic value 💵")

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
