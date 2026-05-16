import requests
from bs4 import BeautifulSoup
import logging
from .parser import clean_text, parse_price, parse_rating

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_static(url="http://books.toscrape.com/"):
    logger.info(f"Starting static scrape of {url}")
    results = []
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select('article.product_pod')
        
        for product in products:
            try:
                title = clean_text(product.h3.a['title'])
                price_text = clean_text(product.select_one('p.price_color').text)
                price, currency = parse_price(price_text)
                rating_class = product.select_one('p.star-rating')['class']
                rating = parse_rating(rating_class) # Not storing rating in DB model yet, but good to have
                
                # Link
                relative_link = product.h3.a['href']
                full_link = requests.compat.urljoin(url, relative_link)
                
                item = {
                    "title": title,
                    "price": price,
                    "currency": currency,
                    "url": full_link,
                    "source_type": "static"
                }
                results.append(item)
            except Exception as e:
                logger.error(f"Error parsing product: {e}")
                continue
                
        logger.info(f"Scraped {len(results)} items successfully.")
        return results
        
    except requests.RequestException as e:
        logger.error(f"Network error scraping {url}: {e}")
        return []
