
"""
Electricity Consumption Scraper - Monthly Data Expanded to Daily
"""

import requests
import csv
from datetime import datetime, timedelta
from collections import Counter

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
        print(f"Error fetching EIA data: {e}")

    return []


def expand_monthly_to_daily(monthly_data, city):
    """
    Repeat the SAME monthly value for every day in that month.
    This keeps daily rows for merging purposes while preserving
    the original monthly signal.
    """

    daily_records = []

    days_in_month = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    for record in monthly_data:

        period = record.get("period", "")
        sales = record.get("sales", 0)

        if not period or not sales:
            continue

        try:
            year = int(period.split("-")[0])
            month = int(period.split("-")[1])

        except:
            continue

        days = days_in_month.get(month, 30)

        # Monthly total in kWh
        monthly_kwh = float(sales) * 1_000_000

        for day in range(1, days + 1):

            try:
                date = datetime(year, month, day).strftime("%Y-%m-%d")

                daily_records.append({
                    "City": city,
                    "Date": date,
                    "Electricity Consumption": round(monthly_kwh, 2),
                    "Source": "eia-monthly-expanded",
                    "Granularity": "monthly_repeated"
                })

            except:
                pass

    return daily_records


def generate_estimated_monthly(city, year=2023):
    """
    Generate estimated MONTHLY electricity data
    then repeat it daily for merge compatibility.
    """

    import random

    random.seed(hash(city) % 10000)

    base_monthly = {
        "Cairo": 9500000000,
        "Dubai": 7200000000,
        "London": 18000000000,
        "Tokyo": 42000000000,
        "Paris": 15000000000,
        "Nairobi": 1200000000
    }

    base = base_monthly.get(city, 5000000000)

    monthly_factors = {
        1: 1.15,
        2: 1.10,
        3: 1.00,
        4: 0.95,
        5: 1.00,
        6: 1.10,
        7: 1.20,
        8: 1.25,
        9: 1.10,
        10: 1.00,
        11: 1.05,
        12: 1.15
    }

    days_in_month = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    all_data = []

    for month in range(1, 13):

        factor = monthly_factors.get(month, 1.0)

        monthly_kwh = (
            base
            * factor
            * (1 + random.uniform(-0.03, 0.03))
        )

        days = days_in_month[month]

        for day in range(1, days + 1):

            try:
                date = datetime(year, month, day).strftime("%Y-%m-%d")

                all_data.append({
                    "City": city,
                    "Date": date,
                    "Electricity Consumption": round(monthly_kwh, 2),
                    "Source": "estimated-monthly-expanded",
                    "Granularity": "monthly_repeated"
                })

            except:
                pass

    return all_data


def main():

    print("=" * 60)
    print("Electricity Consumption Scraper")
    print("Monthly Data Expanded Into Daily Rows")
    print("=" * 60)

    all_data = []

    # Real New York data
    print("\n[Getting New York real data from EIA...]")

    ny_monthly = fetch_eia_monthly("NY", 2023)

    if ny_monthly:

        ny_daily = expand_monthly_to_daily(
            ny_monthly,
            "New York"
        )

        all_data.extend(ny_daily)

        print(
            f"  New York: {len(ny_daily)} records "
            f"(monthly-expanded)"
        )

    else:

        print("  Failed - using estimation")

        all_data.extend(
            generate_estimated_monthly(
                "New York",
                2023
            )
        )

    # Other cities
    cities = [
        "Cairo",
        "Dubai",
        "London",
        "Tokyo",
        "Paris",
        "Nairobi"
    ]

    for city in cities:

        print(f"  {city}: generating monthly estimation...")

        city_data = generate_estimated_monthly(city, 2023)

        all_data.extend(city_data)

    print(f"\nTotal records: {len(all_data)}")

    # Save CSV
    output = "electricity_consumption_2023.csv"

    with open(output, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "City",
                "Date",
                "Electricity Consumption",
                "Source",
                "Granularity"
            ]
        )

        writer.writeheader()
        writer.writerows(all_data)

    print(f"\nSaved to: {output}")

    # Stats
    stats = Counter(d["Source"] for d in all_data)

    print("\nSource breakdown:")

    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()