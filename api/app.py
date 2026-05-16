from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from storage.database import init_db, save_items, get_db, ScrapedItem
from scraper.static_scraper import scrape_static
from scraper.dynamic_scraper import scrape_dynamic
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI(title="Web Scraper API")

# Initialize DB
init_db()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape/static")
async def trigger_static_scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Triggers a static scrape of the given URL in the background.
    """
    def run_scrape(url):
        data = scrape_static(url)
        if data:
            save_items(data)
            
    background_tasks.add_task(run_scrape, request.url)
    return {"message": f"Static scraping started for {request.url}"}

@app.post("/scrape/dynamic")
async def trigger_dynamic_scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Triggers a dynamic scrape (Selenium) of the given URL in the background.
    """
    def run_scrape(url):
        data = scrape_dynamic(url)
        if data:
            save_items(data)
            
    background_tasks.add_task(run_scrape, request.url)
    return {"message": f"Dynamic scraping started for {request.url}"}

@app.get("/data")
def get_data(limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves latest scraped data.
    """
    items = db.query(ScrapedItem).order_by(ScrapedItem.scraped_at.desc()).limit(limit).all()
    return items
