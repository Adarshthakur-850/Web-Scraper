import streamlit as st
import requests
import pandas as pd
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Web Scraper Dashboard", page_icon="🕷️", layout="wide")

st.title("🕷️ Web Scraper AI")

# Sidebar for Actions
st.sidebar.header("Control Panel")

scrape_type = st.sidebar.radio("Scraper Type", ["Static (Requests)", "Dynamic (Selenium)"])
target_url = st.sidebar.text_input("Target URL", 
                                  value="http://books.toscrape.com/" if scrape_type == "Static (Requests)" else "http://quotes.toscrape.com/js/")

if st.sidebar.button("Start Scraping"):
    endpoint = "/scrape/static" if "Static" in scrape_type else "/scrape/dynamic"
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json={"url": target_url})
        if resp.status_code == 200:
            st.sidebar.success(resp.json()["message"])
        else:
            st.sidebar.error(f"Error: {resp.text}")
    except requests.exceptions.ConnectionError:
        st.sidebar.error("Could not connect to API. Is it running?")

# Main Data View
st.subheader("Scraped Data")

if st.button("Refresh Data"):
    try:
        resp = requests.get(f"{API_URL}/data")
        if resp.status_code == 200:
            data = resp.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
                st.download_button("Download CSV", df.to_csv(index=False), "scraped_data.csv", "text/csv")
            else:
                st.info("No data found in database.")
        else:
            st.error("Failed to fetch data.")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to Backend API. Please run `uvicorn api.app:app`.")
