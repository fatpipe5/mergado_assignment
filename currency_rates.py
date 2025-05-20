import requests

ALLOWED_CURRENCIES = {"CZK", "USD", "EUR"}
CNB_URL = (
    "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/"
    "kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"
)

def get_rates():
    """
    Vrati dictionary {'EUR': xx.xx, 'USD': yy.yy}
    Tieto hodnoty uvadzaju kolko CZK dostaneme za 1 EUR/USD'.
    """
    response = requests.get(CNB_URL, timeout=5)
    response.raise_for_status()

    lines = response.text.strip().splitlines()
    rates = {}
    for row in lines[2:]: #preskocime datum a header
        _country, _currency, qty, code, rate = row.split("|")
        if code in ("USD", "EUR"):
            rate = float(rate.replace(",", "."))
            rates[code] = rate

    return rates

def convert_price(amount, src_cur, dst_cur, rates):
    """Prevod meny zo src_cur na dst_cur pouzitim rates dictionary."""
    if src_cur == dst_cur:
        return amount

    if src_cur == "CZK": # najprv vyjadrime vsetko v CZK
        czk_amount = amount
    else:
        czk_amount = amount * rates[src_cur]

    if dst_cur == "CZK": #potom prevod CZK --> dst_cur
        converted_price = czk_amount
    else:
        converted_price = czk_amount / rates[dst_cur]

    return round(converted_price, 2)
