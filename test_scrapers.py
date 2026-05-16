import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scraper.static_scraper import scrape_static
from scraper.dynamic_scraper import scrape_dynamic
from storage.database import init_db, save_items, get_db, ScrapedItem

def test_static():
    print("Testing Static Scraper...")
    url = "http://books.toscrape.com/"
    data = scrape_static(url)
    if data:
        print(f"SUCCESS: Scraped {len(data)} items from {url}")
        print(f"Sample: {data[0]}")
        save_items(data)
    else:
        print("FAILED: No items scraped.")

def test_dynamic():
    print("\nTesting Dynamic Scraper...")
    url = "http://quotes.toscrape.com/js/"
    try:
        data = scrape_dynamic(url)
        if data:
            print(f"SUCCESS: Scraped {len(data)} items from {url}")
            print(f"Sample: {data[0]}")
            save_items(data)
        else:
            print("FAILED: No items scraped.")
    except Exception as e:
        print(f"FAILED with Error: {e}")

def verify_db():
    print("\nVerifying Database Storage...")
    init_db()
    db = next(get_db())
    count = db.query(ScrapedItem).count()
    print(f"Database currently has {count} items.")
    db.close()

if __name__ == "__main__":
    init_db()
    test_static()
    test_dynamic()
    verify_db()
