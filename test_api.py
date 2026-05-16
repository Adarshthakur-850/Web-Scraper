import requests
import sys

API_URL = "http://127.0.0.1:8000"

def test_api():
    print(f"Testing API at {API_URL}...")
    try:
        # Check /data endpoint
        resp = requests.get(f"{API_URL}/data")
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"SUCCESS: Retrieved {len(data)} items from API.")
                print(f"Sample: {data[0]}")
            else:
                print("WARNING: API returned 200 but data is empty (expected populated DB).")
        else:
            print(f"FAILED: API returned status {resp.status_code}")
            print(resp.text)
            
    except Exception as e:
        print(f"FAILED with Error: {e}")

if __name__ == "__main__":
    test_api()
