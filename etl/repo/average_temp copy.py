import pandas as pd
import os

business_filepath = "data/Fortune_500_Corporate_Headquarters.csv"
result_filepath = "data/state results.csv"
states_filepath = "data/states.csv"

states_df = pd.read_csv(states_filepath)
states_df['STATE'] = states_df['Abbreviation']

business_df = pd.read_csv(business_filepath)
business_df = business_df.merge(states_df, how='inner', on="STATE")
business_df['STATE'] = business_df['State']

result = business_df[['STATE', 'REVENUES']].groupby(['STATE'])['REVENUES'].sum().reset_index()
result['YEAR'] = 2017
result.dropna(inplace=True)
result.to_csv(result_filepath)