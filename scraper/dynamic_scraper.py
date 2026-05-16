from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

# Configure logging
logger = logging.getLogger(__name__)

def scrape_dynamic(url="http://quotes.toscrape.com/js/"):
    logger.info(f"Starting dynamic scrape of {url}")
    results = []
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Run in background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        # Wait for JS to load
        time.sleep(2) 
        
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        
        for quote in quotes:
            try:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                
                # Mapping quote to our DB schema (using title for text, url as author for now)
                item = {
                    "title": text[:50] + "...", # Truncate for title
                    "price": 0.0, # Quotes have no price
                    "currency": "N/A",
                    "url": author, # Storing author in URL field for demo simplicity
                    "source_type": "dynamic"
                }
                results.append(item)
            except Exception as e:
                logger.error(f"Error parsing quote: {e}")
                
        driver.quit()
        logger.info(f"Scraped {len(results)} items successfully.")
        return results

    except Exception as e:
        logger.error(f"Selenium error scraping {url}: {e}")
        return []
