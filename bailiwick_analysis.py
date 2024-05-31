import pandas as pd

# Load data
raw_df = pd.read_csv("data/raw_data.csv")

# remove rows that could cause issues
raw_df = raw_df[raw_df['NS'] != 'No NS found']
# Create final df
bailiwick_df = pd.DataFrame(columns=['Domain', 'Bailiwick Status'])

for domain in raw_df["DN"].unique():
    # focus NSs of that domain
    domain_df = raw_df[raw_df['DN'] == domain]

    b_uniques = domain_df['Bailiwick'].unique()

    # all Bailiwick outputs are the same
    if len(b_uniques) == 1:
        # All IN
        if b_uniques[0] == "in":
            bailiwick_df.loc[len(bailiwick_df)] = {'Domain': domain, 'Bailiwick Status': 'In Bailiwick'}
        # All OUT
        else:
            bailiwick_df.loc[len(bailiwick_df)] = {'Domain': domain, 'Bailiwick Status': 'Out of Bailiwick'}

    # Mixed in and out NSs
    else:
        bailiwick_df.loc[len(bailiwick_df)] = {'Domain': domain, 'Bailiwick Status': 'Partially in Bailiwick'}

# Make csv
bailiwick_df.to_csv('data/Bailiwick_data.csv', index=False)



b_df = pd.read_csv("data/Bailiwick_data.csv")

b_organized = pd.DataFrame(columns=['Bailiwick Status', 'Domain Count'])
for b_status in b_df['Bailiwick Status'].unique():
        d_count = b_df['Bailiwick Status'].value_counts()[b_status]
        new_row = {'Bailiwick Status': b_status, 'Domain Count': d_count}
        b_organized.loc[len(b_organized)] = new_row

b_organized.to_csv('data/bailiwick_simplified_data.csv', index=False)