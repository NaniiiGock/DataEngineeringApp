import pandas as pd
import os

business_filepath = "data/Fortune_500_Corporate_Headquarters.csv"
result_filepath = "data/company revenues.csv"

business_df = pd.read_csv(business_filepath)

result = business_df[['NAME', 'REVENUES']]

result['YEAR'] = 2017
result.dropna(inplace=True)
result[['NAME', 'REVENUES', 'YEAR']].to_csv(result_filepath, index=False)

