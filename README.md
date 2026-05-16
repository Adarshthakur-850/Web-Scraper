# Web Scraper System

A production-quality web scraping system that collects structured data from static and dynamic websites, stores it in a SQLite database, and exposes it via a REST API and a Streamlit Dashboard.

## Features
- **Static Scraper**: Uses `requests` and `BeautifulSoup` for fast scraping of static HTML.
- **Dynamic Scraper**: Uses `Selenium` to handle JavaScript-rendered content.
- **Storage**: Structured data storage using `SQLAlchemy` and SQLite.
- **API**: FastAPI backend to trigger scraping jobs and retrieve data.
- **UI**: Streamlit dashboard to control scrapers and view/export data.

## Project Structure
```
Web Scraper/
│
├── scraper/              # Scraper logic
│   ├── static_scraper.py
│   ├── dynamic_scraper.py
│   └── parser.py
├── storage/              # Database models
│   └── database.py
├── api/                  # FastAPI backend
│   └── app.py
├── ui/                   # Streamlit Frontend
│   └── streamlit_app.py
└── requirements.txt
```

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Selenium requires Chrome browser installed.*

## Running the Application

### Option 1: Streamlit UI
Interactive dashboard.
```bash
streamlit run ui/streamlit_app.py
```

### Option 2: FastAPI Backend
REST API.
```bash
uvicorn api.app:app --reload
```
API Documentation: `http://localhost:8000/docs`.

## Verification
To verify the scrapers without the UI/API:
```bash
python test_scrapers.py
```
This script runs both scrapers against test sites (`books.toscrape.com`, `quotes.toscrape.com`) and checks the database.
