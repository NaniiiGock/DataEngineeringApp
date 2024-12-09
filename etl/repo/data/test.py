import duckdb

# Connect to the DuckDB database
con = duckdb.connect('my_duckdb_file.db')

# List all schemas
schemas = con.execute("SELECT schema_name FROM information_schema.schemata;").fetchall()
print("All schemas:", schemas)

# List tables in each 'main' schema
tables_in_main = con.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema = 'main'
    ORDER BY table_name;
""").fetchall()
print("Tables in 'main' schema:", tables_in_main)