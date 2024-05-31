import pandas as pd

# Load raw data
data_df = pd.read_csv("data/cleaned_data.csv")

org_dict = {}

domain_names = data_df['DN'].unique()

for dn in domain_names:
    # df of data specific to each domain
    dn_df = data_df[data_df['DN'] == dn]

    dn_orgs = dn_df['Org'].unique()
    
    # Increment '# Affected'
    for org in dn_orgs:
        # add new orgs to dict
        if org not in org_dict.keys():
            org_dict[org] = {'# Unreachable': 0, '# Affected': 1}
        # already in list
        else:
            org_dict[org]['# Affected'] += 1
    
    # Increment '# Unreachable'
    if len(dn_orgs) == 1:
        org_dict[org]['# Unreachable'] += 1

# Make into df
org_df = pd.DataFrame.from_dict(org_dict)
org_df = org_df.T


org_df['% Unreachable'] = (org_df['# Unreachable'] / 10000) * 100
org_df['% Affected'] = (org_df['# Affected'] / 10000) * 100

org_df.reset_index(inplace=True)
org_df.rename(columns={'index': 'Org'}, inplace=True)

org_df.sort_values(by='% Unreachable', ascending=False, inplace=True)

org_df.to_csv('data/organization_impact_data.csv', index=False)
