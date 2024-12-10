# Turns the raw data inside data/my_duckdb_file.db into nice star schema tables

import duckdb
import pandas as pd

# Path to the DuckDB file
db_path = "./repo/data/my_duckdb_file.db"

# Connect to the DuckDB database
conn = duckdb.connect(database=db_path, read_only=False)

# Read the "fortune_500" table into a pandas DataFrame
df = conn.execute("SELECT * FROM weather_data").fetchdf()

# Pivot the DataFrame
pivot_df = df.pivot_table(index=['date', 'county_fips'], columns='datatype', values='value').reset_index()

# Flatten the column names
pivot_df.columns.name = None
pivot_df.columns = [col if isinstance(col, str) else col[1] for col in pivot_df.columns]
pivot_df['ID'] = pivot_df.index
pivot_df.rename(columns={'date': 'DATE',
                         'county_fips': 'COUNTYFIPS'}, inplace=True)

dfs_with_table_names = {'WeatherFACT': pivot_df}

# Load the DataFrames into the DuckDB database as tables, if they don't exist
for table_name, df in dfs_with_table_names.items():
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} AS
    SELECT * FROM df
    """)

# Close the connection
conn.close()
