import re

def clean_price(text, pattern):
    """Очистка цены по указанному паттерну"""
    patterns = {
        "dns": lambda t: re.sub(r'[^\d.]', '', t.replace('BYN', '')),
        "fk": lambda t: t.replace(' ', '').replace('руб.', '.').replace('коп.', '').replace(',', '.'),
        "ozon": lambda t: re.sub(r'[^\d,]', '', t).replace(',', '.'),
        "texnosmart": lambda t: re.sub(r'[^\d,]', '', t).replace(',', '.'),
        "onliner": lambda t: re.sub(r'[^\d,]', '', t).replace(',', '.'),
        "newton": lambda t: f"{t.replace(' ', '')[:-2]}.{t.replace(' ', '')[-2:]}",
        "xcore": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').replace('руб.', '')),
        "5element": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '')),
        "nsv": lambda t: re.sub(r'[^\d.]', '', t.replace(',', '.')),
        "alloplus": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '')),
        "amd": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').split('руб.')[0].strip()),
        "21vek": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').replace(',', '.').replace('р.', '')),
        "server_by": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').replace(',', '.').replace('РУБ.', '')),
        "default": lambda t: t
    }

    return patterns.get(pattern, patterns["default"])(text)