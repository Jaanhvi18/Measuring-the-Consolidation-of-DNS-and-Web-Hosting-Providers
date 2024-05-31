import pandas as pd



data_df = pd.read_csv("data/organization_impact_data.csv")

features_to_drop = ['# Unreachable', '# Affected']

final_data_df = data_df.drop(features_to_drop, axis=1)
top_ten = final_data_df.head(11)
total_unreachable = top_ten['% Unreachable'].sum()
total_affected = top_ten['% Affected'].sum()
space = ' ' #completely unnecessary addition but I just wanted it to look exactly the same, PLEASE IGNORE 

totals_df = pd.DataFrame({'Org': [space],'% Unreachable': [total_unreachable], '% Affected': [total_affected]})
totals_df.index = ['Total']
data_df_with_totals = pd.concat([top_ten, totals_df])

data_df_with_totals.to_csv('data/top_ten_data_with_totals.csv', index=True)

top_ten.to_csv('data/top_ten_data.csv', index=True)
