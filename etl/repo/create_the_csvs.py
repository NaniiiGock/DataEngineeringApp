import pandas as pd
import os
import re
import json

DATA_DIR = "data/"

master_df = pd.DataFrame()

pattern = re.compile(r'^noaa_.*\.json$')
for file_name in os.listdir(DATA_DIR):
    if pattern.match(file_name):
        file_path = os.path.join(DATA_DIR, file_name)
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if not data.get('results'):
                    continue

                county_fips = file_name.split('_')[1].split('.')[0]

                # Aggregate data by date and datatype
                df = pd.DataFrame(data['results'])
                df['county_fips'] = county_fips
                aggregated_df = (
                    df.groupby(['date', 'datatype'])['value']
                    .mean()
                    .reset_index()
                )
                aggregated_df['county_fips'] = county_fips

                # Combine with master_df
                master_df = pd.concat([master_df, aggregated_df], ignore_index=True)

            except json.JSONDecodeError:
                print(f"Invalid JSON: {file_name}")

# Pivot the dataframe
pivoted_df = master_df.pivot_table(
    index=['date', 'county_fips'],  # Keep date and county_fips as indices
    columns='datatype',            # Pivot based on datatype
    values='value',                # Use value as the data to populate the table
    aggfunc='first'                # Use 'first' as we don't expect duplicates
).reset_index()

# Flatten the column hierarchy created by pivot_table
pivoted_df.columns.name = None

pivoted_df.to_csv('data/master_weather_data.csv', index=False)


            
