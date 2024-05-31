import pandas as pd


cleaned_df = pd.read_csv("data/raw_data.csv")
bad_data = ['No NS found', 'Bad IP', 'No ASN info', 'No Org info']
initial_count = cleaned_df.shape[0] # before removing the bad data
for bad_output in bad_data:
    cleaned_df = cleaned_df[cleaned_df["Org"] != bad_output]
final_count = cleaned_df.shape[0]  # after removing the bad data
removed_entries = initial_count - final_count
cleaned_df.to_csv('data/cleaned_data.csv', index=False)
print("Top 10K domains with incomplete data [that] had to be removed:",removed_entries)






