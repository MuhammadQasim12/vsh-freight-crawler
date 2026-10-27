import json
from datetime import datetime, timedelta

RAW_DATA_FILE = "raw_scraped_data.json"
FRESH_DATA_FILE = "fresh_market_data.json"

def run_freight_crawler_and_analyzer():
    print("🚀 Initializing Freight Market Crawler & Analyzer...")
    
    try:
        with open(RAW_DATA_FILE, "r") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("⚠️ raw_scraped_data.json not found! Using initial fallback data.")
        raw_data = []

    now = datetime.now()
    cutoff_time = now - timedelta(hours=24) # 24-hour freshness rule
    
    fresh_entries = []
    market_gaps = []

    for entry in raw_data:
        # Expiry Check
        entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        if entry_time < cutoff_time:
            print(f"🗑️ Purged expired record: {entry['region']}")
            continue  

        # Market Gap Calculation (Load-to-Truck Ratio)
        loads = entry["available_loads"]
        trucks = max(entry["available_trucks"], 1)
        ltr = round(loads / trucks, 2)
        
        entry["ltr_ratio"] = ltr
        
        if ltr >= 4.0:
            entry["opportunity_tier"] = "🔥 HIGH MARGIN GAP"
            market_gaps.append(entry)
        else:
            entry["opportunity_tier"] = "Standard Market"

        fresh_entries.append(entry)

    with open(FRESH_DATA_FILE, "w") as f:
        json.dump(fresh_entries, f, indent=4)

    print(f"✅ Crawler execution successful!")
    print(f"   - Active fresh records stored: {len(fresh_entries)}")
    print(f"   - High-margin market gaps identified: {len(market_gaps)}")

if __name__ == "__main__":
    run_freight_crawler_and_analyzer()
