import pandas as pd
import os

weather_filepath = "data/master_weather_data.csv"
business_filepath = "data/Fortune_500_Corporate_Headquarters.csv"
result_filepath = "data/average temperatures.csv"

weather_df = pd.read_csv(weather_filepath)
business_df = pd.read_csv(business_filepath)

county_avgs = weather_df.groupby(["county_fips"])[['TAVG', 'TMIN', 'TMAX']].mean().reset_index()
county_avgs['AVG'] = county_avgs[['TAVG', 'TMIN', 'TMAX']].mean(axis=1)
county_avgs = county_avgs[['county_fips', 'AVG']]

business_df.rename(columns= {'COUNTYFIPS' : 'county_fips'}, inplace = True)

business_df = business_df[['NAME', 'county_fips', 'REVENUES']]

result = business_df.merge(county_avgs, on='county_fips', how='inner')
result['YEAR'] = 2017
result.dropna(inplace=True)
result[['NAME', 'AVG', 'REVENUES', 'YEAR']].to_csv(result_filepath)

