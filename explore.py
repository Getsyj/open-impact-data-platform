import duckdb
con = duckdb.connect("impact.duckdb")

def q(title, sql):
    print("\n==", title)
    con.sql(sql).show(max_rows=60)

q("1 Shape", "SELECT count(*) AS rows, count(DISTINCT country) AS countries, min(year) AS first_year, max(year) AS last_year FROM raw_wb_water")
q("1 Column types", "DESCRIBE raw_wb_water")
q("2 Missing overall", "SELECT count(*) - count(value) AS missing_values, round(100.0 * (count(*) - count(value)) / count(*), 1) AS pct_missing FROM raw_wb_water")
q("2 Missing by year", "SELECT year, count(*) AS rows, count(value) AS with_value, count(*) - count(value) AS missing FROM raw_wb_water GROUP BY year ORDER BY missing DESC LIMIT 10")
q("3 Duplicates (expect no rows)", "SELECT country, year, count(*) AS n FROM raw_wb_water GROUP BY country, year HAVING count(*) > 1")
q("4 Value range", "SELECT min(value) AS lowest, max(value) AS highest, round(avg(value), 1) AS average FROM raw_wb_water")
q("5 All names (look for non-countries)", "SELECT DISTINCT country, country_code FROM raw_wb_water ORDER BY country")
q("5 Codes with more than one name (expect no rows)", "SELECT country_code, count(DISTINCT country) AS names FROM raw_wb_water GROUP BY country_code HAVING count(DISTINCT country) > 1")
q("6 Oldest latest-years", "SELECT country, max(year) AS latest_year FROM raw_wb_water WHERE value IS NOT NULL GROUP BY country ORDER BY latest_year, country LIMIT 15")
q("6 Countries with no data at all", "SELECT country FROM raw_wb_water GROUP BY country HAVING count(value) = 0")
q("7 India's trend", "SELECT year, value FROM raw_wb_water WHERE country = 'India' AND value IS NOT NULL ORDER BY year DESC LIMIT 10")