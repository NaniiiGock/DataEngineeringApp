import duckdb

# Path to the DuckDB file
db_path = "./repo/data/my_duckdb_file.db"

# Connect to the DuckDB database
conn = duckdb.connect(database=db_path, read_only=True)

# List of tables to check
tables_to_check = ['BusinessFACT', 'BusinessDIM', 'CountyDIM', 'WeatherFACT']

# Check if the tables exist and print their contents
for table in tables_to_check:
    result = conn.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table}'").fetchone()
    if result[0] > 0:
        print(f"Table '{table}' exists.")
        # Print the first few rows of the table
        df = conn.execute(f"SELECT * FROM {table}").fetchdf()
        print(df.head())
    else:
        print(f"Table '{table}' does not exist.")

# Close the connection
conn.close()
