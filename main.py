from browser import BrowserManager
from patterns import clean_price
from urllib.parse import urlparse
import json
import time

def extract_price(page, selector, pattern="default"):
    """Достаем цену по селектору с указанным паттерном очистки"""
    try:
        element = page.query_selector(selector)
        if element:
            if element.get_attribute('itemprop') == 'price':
                price_text = element.get_attribute('content')
            else:
                price_text = element.inner_text().strip()

            return clean_price(price_text, pattern)
    except:
        pass
    return None

def extract_domain(url):
    """Извлекает домен из URL для использования как ключа"""
    parsed = urlparse(url)
    domain = parsed.netloc
    return domain.replace('www.', '')

def main():
    with open('selector.json', 'r', encoding='utf-8') as f:
        stores_config = json.load(f)['stores']

    with open('products.json', 'r', encoding='utf-8') as f:
        products_data = json.load(f)

    browser = BrowserManager(headless=True)

    try:
        for product in products_data['products']:
            print(f"\n🎯 {product['name']}")
            print("=" * 50)

            prices = []

            for url in product['urls']:
                store_key = extract_domain(url)
                selector = stores_config.get(store_key, '')

                print(f"🏪 {store_key}")

                page = browser.new_page()
                price_text = None

                for attempt in range(5):
                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=10000)
                        price_text = extract_price(page, selector, store_key)
                        if price_text:
                            break
                        time.sleep(0.5)
                    except Exception:
                        time.sleep(1)
                        continue

                if price_text:
                    try:
                        price_value = float(price_text)
                        prices.append({
                            'store': store_key,
                            'price': price_value,
                            'url': url,
                            'price_text': price_text
                        })
                        print(f"💰 {price_text}")
                    except ValueError:
                        print(f"💰 {price_text} (не число)")
                else:
                    print("❌ Цена не найдена")

                page.close()
                time.sleep(0.5)

            if prices:
                min_price = min(prices, key=lambda x: x['price'])
                print(f"\n🏆 МИНИМАЛЬНАЯ ЦЕНА: {min_price['price_text']}")
                print(f"🏪 Магазин: {min_price['store']}")
                print(f"🔗 Ссылка: {min_price['url']}")

            print("=" * 50)

    finally:
        browser.close()

if __name__ == "__main__":
    main()