import pandas as pd
import matplotlib.pyplot as plt


data_df = pd.read_csv("data/top_ten_data.csv")

# Organize data
plt.figure(figsize=(10, 6))
plt.bar(data_df['Org'],
        data_df['% Unreachable'],
        label='Unreachable',
        color='b')
plt.bar(data_df['Org'],
        data_df['% Affected'] - data_df['% Unreachable'],
        bottom=data_df['% Unreachable'],
        label='Affected',
        color='m')
# Add labels and title
plt.xlabel('Organizations', fontweight='bold', fontsize=15)
plt.ylabel('% of domains', fontweight='bold', fontsize=15)
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.title('Percent of Domains Unreachable and Affected by Top Organizations', fontsize=20)
plt.tight_layout()
plt.savefig('visuals/org_impact_vis.png')
plt.close()



b_df = pd.read_csv("data/bailiwick_simplified_data.csv")

plt.figure(figsize=(10, 8))
plt.bar(b_df['Bailiwick Status'],
        b_df['Domain Count'],
        color='b')
plt.xlabel("Bailiwick Status", fontweight='bold', fontsize=15)
plt.ylabel("Number of Domains", fontweight='bold', fontsize=15)
plt.title('Bailiwick Status Distribution', fontsize=20)
plt.savefig('visuals/bailiwick_count_plot.png')
plt.close()



