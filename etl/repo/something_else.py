import pandas as pd
import os

weather_filepath = "data/master_weather_data.csv"
business_filepath = "data/Fortune_500_Corporate_Headquarters.csv"
result_filepath = "data/average temperatures.csv"

weather_df = pd.read_csv(weather_filepath)
business_df = pd.read_csv(business_filepath)