import pandas as pd
import dns.resolver
import ipaddress
from ipaddress import ip_address


def main():
    data = load_csv("data/tranco_G6Z3K.csv", 10000)
    
    # get DNS resolver
    r = dns.resolver.Resolver()
    r.nameservers = ['127.0.0.1']
    r.port = 8053

    # Start raw data dataframe
    total_raw_data = pd.DataFrame(columns=['DN', 'NS', 'Bailiwick', 'IP', 'ASN', 'Org'])


    # Go through each Domain
    for dn in data['DN']:

        # Get list of name servers
        ns_list = get_NSs(r, dn)

        # Handle bad results of lookup
        if len(ns_list) == 0:
            new_row = {'DN': dn, 'NS': 'No NS found', 'Bailiwick': 'No NS found', 'IP': 'No NS found', 'ASN': 'No NS found', 'Org': 'No NS found'}
            total_raw_data.loc[len(total_raw_data)] = new_row
            
        
        # Go through each name server
        for ns in ns_list:

            # Get Bailiwick data
            bailiwick = ''
            if dn in ns:
                bailiwick = "in"
            else:
                bailiwick = "out"

            # Get IP list for each name server (should only ever be len 1)
            ns_ip = get_NS_IP(r, ns)

            # Handle bad results of lookup
            if ns_ip == "Lookup failed" or ns_ip == "No IP found":
                new_row = {'DN': dn, 'NS': ns, 'Bailiwick': bailiwick, 'IP': 'Bad IP', 'ASN': 'Bad IP', 'Org': 'Bad IP'}
                total_raw_data.loc[len(total_raw_data)] = new_row
                continue


            # Get ASN for that IP
            asn = get_ASN(r, ns_ip)

            # Handle bad results of lookup
            if asn == "No ASN info" or asn == "Lookup failed":
                new_row = {'DN': dn, 'NS': ns, 'Bailiwick': bailiwick, 'IP': ns_ip, 'ASN': 'No ASN info', 'Org': 'No ASN info'}
                total_raw_data.loc[len(total_raw_data)] = new_row
                continue


            # Get org from that ASN
            organization = get_organization(r, asn)

            # Handle bad results of lookup
            if organization == "No org records" or organization == "Lookup failed":
                new_row = {'DN': dn, 'NS': ns, 'Bailiwick': bailiwick, 'IP': ns_ip, 'ASN': asn, 'Org': 'No Org info'}
                total_raw_data.loc[len(total_raw_data)] = new_row
                continue


            # Add findings to raw data dataframe
            new_row = {'DN': dn, 'NS': ns, 'Bailiwick': bailiwick, 'IP': ns_ip, 'ASN': asn, 'Org': organization}
            total_raw_data.loc[len(total_raw_data)] = new_row

    
    # Raw data to CSV
    total_raw_data.to_csv('data/raw_data.csv', index=False)
    print(total_raw_data)
        


def get_organization(r, asn):
    cymru_query_site = asn + ".asn.cymru.com"
    try:
        asn_info = r.resolve(cymru_query_site, "TXT")
    except dns.resolver.NoAnswer:
        return "No org records"
    except dns.exception.DNSException as e: ### TIMEOUT?
        return "Lookup failed"

    org = str(asn_info[0]).split(' | ')[4].split(',')[0] # I deeply apologize for this line

    return org



def get_ASN(r, ns_ip):
    asn_num = cymru_origin_query(r, ns_ip)
    # IF MULTIPLE ASNs FOUND, USE ONLY THE FIRST ASN GIVEN
    asn = "AS" + asn_num.split(" ")[0]

    return asn
    


def cymru_origin_query(r, ns_ip):
    rev_ip = reverse_ip(ns_ip)
    cymru_query_site = rev_ip + ".origin.asn.cymru.com"
    try:
        origin_info = r.resolve(cymru_query_site, "TXT")
    except dns.resolver.NoAnswer:
        return 'No ASN info'
    except dns.exception.DNSException as e:
        return 'Lookup failed'

    asn_num = str(origin_info[0]).split(' | ')[0][1:]

    return asn_num



def reverse_ip(ip_str):
    rev_ip = ipaddress.ip_address(ip_str).reverse_pointer
    rev_ip = str(rev_ip)[0:-13]

    return rev_ip



def get_NS_IP(r, ns):
    try:
        name_server_ips = r.resolve(ns, dns.rdatatype.A)
    except dns.resolver.NoAnswer:
        return 'No IP found'
    except dns.exception.DNSException as e:
        return 'Lookup failed'
    
    ns_ip = str(name_server_ips[0])

    return ns_ip



def get_NSs(r, domain):
    ns_list = []
    try:
        name_servers = r.resolve(domain, dns.rdatatype.NS)
        for ns in name_servers:
            ns_list.append(str(ns))
    except dns.resolver.NoAnswer:
        ns_list=[]
    except dns.exception.DNSException as e:
        ns_list=[]

    return ns_list
    


def load_csv(filename, num_rows):
    df = pd.read_csv(filename, names=['Rank', 'DN'])
    df = df.iloc[0:num_rows]
    return df


if __name__ == '__main__':
    main()