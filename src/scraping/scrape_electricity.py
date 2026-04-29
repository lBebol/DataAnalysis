#!/usr/bin/env python3
"""
Electricity Consumption Scraper - With EIA Monthly Data
"""

import requests
import csv
import json
from datetime import datetime, timedelta
import time

API_KEY = "G3L9gGFuYE1ljXHGoNSrX5f3NJ3wToeSfQ4ejYTf"

def fetch_eia_monthly(state_code="NY", year=2023):
    """Fetch monthly electricity sales data from EIA"""
    url = "https://api.eia.gov/v2/electricity/retail-sales/data"
    params = {
        "api_key": API_KEY,
        "frequency": "monthly",
        "data[0]": "sales",
        "facets[stateid][]": state_code,
        "facets[sectorid][]": "ALL",
        "start": f"{year}-01",
        "end": f"{year}-12",
        "length": 12
    }
    
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            j = r.json()
            return j.get("response", {}).get("data", [])
    except Exception as e:
        print(f"Error: {e}")
    
    return []

def distribute_monthly_to_daily(monthly_data, city):
    """Distribute monthly MWh into daily values"""
    daily_records = []
    
    for record in monthly_data:
        period = record.get("period", "")
        sales = record.get("sales", 0)  # million kWh
        
        if not period or not sales:
            continue
        
        # Parse month
        try:
            month = int(period.split("-")[1])
            year = int(period.split("-")[0])
        except:
            continue
        
        # Days in each month
        days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        
        days = days_in_month.get(month, 30)
        
        # Daily kWh = (monthly million kWh / days) * 1000000
        daily_kwh = (float(sales) * 1000000) / days
        
        for day in range(1, days + 1):
            try:
                date = datetime(year, month, day).strftime("%Y-%m-%d")
                daily_records.append({
                    "City": city,
                    "Date": date,
                    "Electricity Consumption": round(daily_kwh, 2),
                    "Source": "eia-monthly"  # Mark as real (from EIA)
                })
            except:
                pass
    
    return daily_records

def generate_estimated(city, year=2023):
    """Generate estimated data for other cities"""
    import random
    random.seed(hash(city) % 10000)
    
    base_demand = {
        "Cairo": 15000,
        "Dubai": 12000,
        "London": 35000,
        "Tokyo": 100000,
        "Paris": 25000,
        "Nairobi": 2500
    }
    
    base = base_demand.get(city, 10000)
    all_data = []
    
    for day_idx in range(365):
        date = datetime(year, 1, 1) + timedelta(days=day_idx)
        month = date.month
        dow = date.weekday()
        
        if month in [6, 7, 8]:
            sf = 1.2
        elif month in [12, 1, 2]:
            sf = 1.15
        else:
            sf = 1.0
        
        wf = 0.85 if dow >= 5 else 1.0
        
        demand_mw = base * sf * wf * (1 + random.uniform(-0.05, 0.05))
        kwh = demand_mw * 1000 * 24
        
        all_data.append({
            "City": city,
            "Date": date.strftime("%Y-%m-%d"),
            "Electricity Consumption": round(kwh, 2),
            "Source": "estimated"  # Mark as estimated
        })
    
    return all_data

def main():
    print("=" * 60)
    print("Electricity Consumption Scraper - EIA Monthly Data")
    print("=" * 60)
    
    all_data = []
    
    # Get real New York data
    print("\n[Getting New York real data from EIA...]")
    ny_monthly = fetch_eia_monthly("NY", 2023)
    
    if ny_monthly:
        ny_daily = distribute_monthly_to_daily(ny_monthly, "New York")
        all_data.extend(ny_daily)
        print(f"  New York: {len(ny_daily)} daily records (from EIA monthly)")
    else:
        print("  Failed - using estimation")
        all_data.extend(generate_estimated("New York", 2023))
    
    # Generate for other cities
    cities = ["Cairo", "Dubai", "London", "Tokyo", "Paris", "Nairobi"]
    
    for city in cities:
        print(f"  {city}: generating estimation...")
        all_data.extend(generate_estimated(city, 2023))
    
    print(f"\nTotal: {len(all_data)} records")
    
    # Save
    output = "electricity_consumption_2023.csv"
    
    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["City", "Date", "Electricity Consumption", "Source"])
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"Saved to: {output}")
    
    # Stats
    from collections import Counter
    stats = Counter(d["Source"] for d in all_data)
    print(f"\nSource breakdown: {dict(stats)}")

if __name__ == "__main__":
    main()