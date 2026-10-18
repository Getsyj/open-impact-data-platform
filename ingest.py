import requests, duckdb, pandas as pd

indicator = "SH.H2O.BASW.ZS"  # basic drinking water, % of population
url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
resp = requests.get(url, params={"format": "json", "per_page": 20000}, timeout=30)
resp.raise_for_status()
rows = resp.json()[1]

df = pd.DataFrame([
    {"country": r["country"]["value"], "country_code": r["countryiso3code"],
     "year": int(r["date"]), "value": r["value"], "indicator": indicator}
    for r in rows
])
df.to_csv("data/raw/wb_water.csv", index=False)

con = duckdb.connect("impact.duckdb")
con.execute("CREATE OR REPLACE TABLE raw_wb_water AS SELECT * FROM read_csv_auto('data/raw/wb_water.csv')")
print(con.execute("SELECT count(*), min(year), max(year) FROM raw_wb_water").fetchall())