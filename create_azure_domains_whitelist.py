#!/usr/bin/env python3

import urllib.request

# Yes really, I'm using 2 HTML parsers, yes this is terrible, yes this is sloppy code.
from bs4 import BeautifulSoup
from html.parser import HTMLParser

# This is some of the worst python code I have ever written by the way.

url = "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns"

def fetch_html(url):
    try:
        response = urllib.request.urlopen(url)
        html_bytes = response.read()
        html_string = html_bytes.decode('utf-8')
        return html_string
    except Exception as e:
        print(f"HTML fetching failed: {e}")
        return None

def cleanuphtml(raw_html):
    commercial_split = raw_html.partition('<h2 id="commercial">Commercial</h2>')
    government_split = commercial_split[2].partition('<h2 id="government">Government</h2>')
    return government_split[0]

class SupTagRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_sup = False

    def handle_starttag(self, tag, attrs):
        if tag == 'sup':
            self.in_sup = True
        else:
            self.result.append('<' + tag + '>')

    def handle_endtag(self, tag):
        if tag == 'sup':
            self.in_sup = False
        else:
            self.result.append('</' + tag + '>')

    def handle_data(self, data):
        if not self.in_sup:
            self.result.append(data)

def remove_sup_tags(html_content):
    parser = SupTagRemover()
    parser.feed(html_content)
    return ''.join(parser.result)

def extract_hostnames_from_tables(relevant_html):
    soup = BeautifulSoup(relevant_html, 'html.parser')

    domains_list_dirty = []
    
    # Find all tables in the parsed HTML
    tables = soup.find_all('table')
    
    # Iterate through each table
    for table in tables:
        # Find all rows in the table
        rows = table.find_all('tr')
        
        # Iterate through each row
        for row in rows:
            # Find all cells in the row
            cells = row.find_all('td')
            
            # Check if the row has at least 3 cells
            if len(cells) >= 3:
                # Extract and print the 3rd and 4th values
                third_value = cells[2]
                fourth_value = cells[3] if len(cells) > 3 else ""
                
                # Add the modified cells to the list
                domains_list_dirty.append(third_value)
                domains_list_dirty.append(fourth_value)
    
    return domains_list_dirty

def final_cleanup(domains_list_dirty):
    final_list_pre_substitution = []
    for cell in domains_list_dirty:
        cell = str(cell)
        soup = BeautifulSoup(cell, 'html.parser')
        td_tag = soup.find('td')
        if td_tag:
            str_td_tag = str(td_tag)
            values = str_td_tag.split('<br/>')      
            for value in values:
                bruh = value.replace('<td>','')
                bruh2 = bruh.replace('</td>','')
                final_list_pre_substitution.append(bruh2.strip())
    return final_list_pre_substitution

def remove_region_naming(final_list_pre_substitution):
    substitutions = ["{regionName}.","{subzone}.","{dnsPrefix}.","{instanceName}.","{region}.","{regionCode}.","{partitionId}."]
    domains_list = []
    for domain in final_list_pre_substitution:
        for substitution in substitutions:
            if substitution in domain:
                domain = domain.partition(substitution)[2]
        if domain not in domains_list:
            domains_list.append(domain)
    return domains_list

raw_html = fetch_html(url)
almost_relevant_html = cleanuphtml(raw_html)
relevant_html = remove_sup_tags(almost_relevant_html)
domains_list_dirty = extract_hostnames_from_tables(relevant_html)
final_list_pre_substitution = final_cleanup(domains_list_dirty)
domains_list = remove_region_naming(final_list_pre_substitution)

for domain in domains_list:
    print(domain)
