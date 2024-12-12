# Turns the raw data inside data/my_duckdb_file.db into nice star schema tables

import duckdb
import pandas as pd

# Path to the DuckDB file
db_path = "./repo/data/my_duckdb_file.db"

# Connect to the DuckDB database
conn = duckdb.connect(database=db_path, read_only=False)

# Read the "fortune_500" table into a pandas DataFrame
df = conn.execute("SELECT * FROM fortune_500").fetchdf()

# Only keep the relevant columns
df = df[['RANK', 'NAME', 'STATE', 'COUNTY', 'EMPLOYEES', 'REVENUES', 'COUNTYFIPS', 'PROFIT']]
df['ID'] = df['NAME'].astype('category').cat.codes
df['BUSINESSID'] = df['ID']

business_fact = df.copy()[['BUSINESSID', 'RANK', 'EMPLOYEES', 'REVENUES', 'PROFIT']]
business_fact['ID'] = business_fact.index

business_dim = df.copy()[['ID', 'NAME', 'COUNTYFIPS']]

county_dim = df.copy()[['COUNTYFIPS', 'COUNTY', 'STATE']]
county_dim = county_dim.drop_duplicates()

# Load the DataFrames into the DuckDB database as tables, if they don't exist
dfs_with_table_names = {'BusinessFACT': business_fact,
                        'BusinessDIM': business_dim,
                        'CountyDIM': county_dim}

# Load the DataFrames into the DuckDB database as tables, if they don't exist
for table_name, df in dfs_with_table_names.items():
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} AS 
    SELECT * FROM df
    """)

# Close the connection
conn.close()
