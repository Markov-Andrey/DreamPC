import re

def clean_price(text, pattern):
    """Очистка цены по указанному паттерну"""
    patterns = {
        "dns-shop.by": lambda t: re.sub(r'[^\d.]', '', t.replace('BYN', '')),
        "fk.by": lambda t: t.replace(' ', '').replace('руб.', '.').replace('коп.', '').replace(',', '.'),
        "ozon.by": lambda t: re.sub(r'[^\d,]', '', t).replace(',', '.'),
        "texnosmart.by": lambda t: re.sub(r'[^\d,]', '', t).replace(',', '.'),
        "catalog.onliner.by": lambda t: re.sub(r'[^\d,]', '', t).replace(',', '.'),
        "newton.by": lambda t: f"{t.replace(' ', '')[:-2]}.{t.replace(' ', '')[-2:]}",
        "x-core.by": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').replace('руб.', '')),
        "5element.by": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '')),
        "nsv.by": lambda t: re.sub(r'[^\d.]', '', t.replace(',', '.')),
        "alloplus.by": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '')),
        "amd.by": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').split('руб.')[0].strip()),
        "21vek.by": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').replace(',', '.').replace('р.', '')),
        "server.by": lambda t: re.sub(r'[^\d.]', '', t.replace(' ', '').replace(',', '.').replace('РУБ.', '')),
        "default": lambda t: t
    }

    return patterns.get(pattern, patterns["default"])(text)