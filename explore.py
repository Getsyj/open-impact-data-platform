import duckdb
con = duckdb.connect("impact.duckdb")
con.sql("SELECT count(*) AS rows, count(DISTINCT country) AS countries FROM raw_wb_water").show()