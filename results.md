# Results: Programming Project 02: Reproducing and extending DNS research

## Instructions for duplicating our experiments:
To run the data collection, the analysis, and visualizations, simply run:
```bash
./run_research.sh 
```
This script takes no parameters and will leave you with a data folder containing the raw and analysed data, as well as a visuals folder contain all figures to show the analysed results.
<br/>

## Dependencies
```bash
pip3 install pandas
```
```bash
pip3 install ipaddress
```
```bash
pip3 install matplotlib
```


## Scripts
* `run_research.sh`


## All the python files 
* `bailiwick_analysis.py`
* `data_vis.py`
* `error_handling_cleanup.py`
* `organization_analysis.py`
* `research.py`
* `top_ten.py`


## All csv files after research is completed
* `data/raw_data.csv`
* `data/organization_impact_data.csv`
* `data/top_ten_data.csv`
* `data/tranco_G6Z3K.csv`
* `data/cleaned_data.csv`
* `data/Bailiwick_data.csv`
* `data/bailiwick_simplified_data.csv`
* `data/top_ten_data_with_totals.csv`
* `data/top_ten_data.csv`


## All visuals (png files) after research is completed
* `bailiwick_count_plot.png`
* `org_impact.png`


## Handling of bad data
Throughout the data collection process, bad-lookups, failure to find NSs, among other failures are recorded in the `raw_data.csv` output. For the sake of bailiwick analysis, we were able to use some data that was unusable for organization based analysis due to only needing the NSs for a given domain, without even needing their IPs, so this may have allowed us to perform more in-depth analysis than we otheriwse would have been capable of in that respect. In the case of analysis related to organizations however, any incomplete data had to be removed, so it may well have impacted overall results. Similarly, it is possible that there are issues in our data collection which we fail to identify, such as missing NSs for a given domain. In light of that, all results should be considered with caution, and some consistency, the methods should be repeated.
<br/>

## Replicating Table 1

| No. | Org                                             | % Unreachable        | % Affected           |
|-----|-------------------------------------------------|----------------------|----------------------|
| 0   | AMAZON-02                                       | 23.7                 | 25.77                |
| 1   | CLOUDFLARENET                                   | 23.49                | 24.47                |
| 2   | GOOGLE                                          | 4.5                  | 4.760000000000001    |
| 3   | AKAMAI-ASN2                                     | 2.16                 | 6.65                 |
| 4   | SECURITYSERVICES                                | 2.06                 | 3.36                 |
| 5   | MICROSOFT-CORP-MSN-AS-BLOCK                     | 1.87                 | 2.37                 |
| 6   | NSONE                                           | 1.1900000000000002   | 3.75                 |
| 7   | TIGGEE                                          | 1.12                 | 1.69                 |
| 8   | GODADDY-DNS                                     | 0.4499999999999999   | 0.95                 |
| 9   | CLOUDNSNET Cloud DNS Ltd.                       | 0.32                 | 0.5499999999999999   |
| 10  | ALIBABA-CN-NET Hangzhou Alibaba Advertising Co. | 0.31                 | 0.93                 |
| Total |                                               | 61.17                | 75.25                |

* **Top 10K domains with incomplete data [that] had to be removed: 289**

* This Table (`data/top_ten_data_with_totals.csv`) shows the top 10 most popular name server hosting providers by the percentage of domains
that would be unreachable if that provider experienced an outage, i.e. highlighting the potential impact of an outage on domain accessibility. 
* In compiling our top ten list, we encountered a challenge: variations in naming conventions for the same organization within our dataset. For instance, AKAMAI appeared under multiple aliases, including **AKAMAI-ASN2**, **AKAMAI-ASN1**, and **AKAMAI-LINODE-AP Akamai Connected Cloud**. 
* These variations in naming made it difficult to accurately aggregating data. We tried to consolidate these entities, but the variation in naming conventions limited our ability to group all related orgs under a single organization effectively. 
* We also think that this might have impacted the accuracy of our top ten list, potentially underrepresenting the ranking of some of the organizations. 
* We also noticed that for the Top 10 list that we compiled, there is a significatant decline after **CLOUDFLARENET** (ranked 2nd on the list) to the next most common organization, **GOOGLE** (Our result here is different form the paper which states **AKAMAI**, which could be a result from the variation in naming convention mentioned above)
<br/><br/>

## Bailiwick Section

### Methodology for determining if a domain's name servers are exclusively in-bailiwick
We initially remove rows where the name server status is listed as **No NS found**, since these rows do not contribute useful information for determining their bailiwick status. We then iterate over each unique domain in the `raw_data.csv`, focusing on the rows that are associated with that specific domain to check its bailiwick status based on the values in the **Bailiwick** column from the `raw_data.csv`. This columns was developed in the initial data collection, and categorizes each NS as 'in' or 'out' based on whether or not the full domain string appears within the NS's name.

Then for each domain, we identified the unique values of the **Bailiwick** column. We then check the bailiwick status of a domain based on the following criterias:

- If there is only one unique bailiwick value and it is "in," all NSs for the domain are considered to be in-bailiwick, and the domain is categorized as **In Bailiwick**.
- If there is only one unique bailiwick value but it is not "in" (indicating all values are "out"), then the domain is labeled as **Out of Bailiwick**.
- If there are multiple unique bailiwick values (indicating a combination of "in" and "out"), the NSs for the domain are considered to be **Partially in Bailiwick**.



### Bailiwick Analysis
![alt text](<visuals/first_time_bailiwick_counts.png>)
__Above is the bailiwick_count_plot.png output for our test run. The analysis provided will be based upon the data captured in this execution of the code at 11:45 PM, 3/6/2024, however we expect that these results will stay relatively consistent within a small enough timeframe. The same visual for each individual run of the code will appear as `bailiwick_count_plot.png`


* #### out-of-bailiwick
    We found that the majority of domains fall into the out-of-bailiwick category, over 8,000 of the 10,000 domains. The massive amount of domains in the out-of-bailiwick category likely reflect the majority of sites, which are hosted by more capable or professional hosting services, while the domain in question is focused away from the commitment and overhead of server upkeep. This category may also account for those large companies/domains with inconsistent NS naming, such as the NS, ns-27.awsdns-03.com for amazonaws.com, as well as cases in which the domain is clearly owned by a larger company, which uses its name servers from its primary domain to host the smaller domain. This is the case with the domain, googleapis.com and its name servers which include ns2.google.com (among other ns#.google.com NSs)


* #### in-bailiwick
    Those 1000+ in the in-bailiwick category are likely a result of focusing upon the top 10k of domains through tranco's ranking, meaning that this accounts, disproportionately for massive tech companies which prioritise server ownership/maintenance and security.


* #### partially-in-bailiwick
    The partially-in-bailiwick category likely accounts for domains which have some name-servers hosted by 3rd parties for increased consistency.
<br/><br/>





## Further Research 
 
![xkcd Research](https://imgs.xkcd.com/comics/further_research_is_needed.png)

_[https://xkcd.com/2268](https://xkcd.com/2268)_