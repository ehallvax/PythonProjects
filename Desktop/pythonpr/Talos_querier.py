import requests
import json
import os
import time
import xlsxwriter
import threading
import csv

dict_out = {}  # domain : categorization will be written in this dictionary

threads = []

def search_function(search_string):
    req = requests.session()
    tries = 100  # nr of retries if JSON return an error
    if search_string.count('.') ==1:
        Parameter = '/api/v2/details/domain/'
    elif search_string.count('.') ==2:
        Parameter = '/api/v2/details/host/'
    else:
        Parameter = '/api/v2/details/ip/'
    for i in range(tries):
        try: #will try to query the URL, in case of JSON error, will wait 10 sec and query again (max 100 time)
            r_details = req.get('https://talosintelligence.com/sb_api/query_lookup',
                                        headers={'referer': 'https://talosintelligence.com/reputation_center/lookup?search={}'.format(search_string)},
                                        params={
                                            'query' : Parameter,
                                            'query_entry': search_string
                                        })
            #print(r_details)
            r_details = r_details.json()#send the get request to fetch the content
            #print(r_details)
            if 'category' in r_details:  #checks if category is a key in r_details dict.
                    if r_details['category'] is None:
                        print('{} : N/A'.format(search_string))
                        dict_out[search_string] = 'N/A'
                    else:
                        print('{} : {}'.format(search_string, r_details['category']['description']))
                        dict_out[search_string] = r_details['category']['description']
            elif 'error' in r_details:  #if there are no inputs at all will display "no results"
                print('{} : No results'.format(search_string))
                dict_out[search_string] = 'No Result'
        except json.decoder.JSONDecodeError as e:
            print(e)
            if i < tries - 1:
                time.sleep(10)
                continue
            else:
                raise
        break

def trim_domain(url_in):
    out_domain = url_in
    prefixes = ['http://', 'https://']
    for prefix in prefixes:
        if url_in.startswith(prefix):
            out_domain = url_in[len(prefix):]
    return out_domain

def get_url(url_file):
    with open(url_file, 'r', encoding='utf-8') as file_domains:  # open csv file to fetch the data
        for lines in csv.reader(file_domains):  # reads each line
            if ',' in lines:
                list_of_domains = lines.split(',')
                for domain in list_of_domains:
                    yield trim_domain(domain)
            else:
                print(lines[0])
                domain = lines[0].strip('\ufeff')
                yield trim_domain(domain)

for url in get_url('/Users/ehallvax/Desktop/web_test.csv'):
    search_function(url)
    time.sleep(1.7)




if 'Domain or IP' in dict_out: #will delete the header of the original csv file
    del dict_out['Domain or IP']

workbook = xlsxwriter.Workbook('/Users/ehallvax/Desktop/Websites_categorised.xlsx')#print the output to a xlsx files
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
worksheet.set_column(1, 1, 50)
worksheet.write('A1', 'Domains', bold)
worksheet.write('B1', 'Categorisation', bold)
row = 1
col = 0
for domain in dict_out:
    worksheet.write_string(row, col, domain )
    worksheet.write_string(row, col + 1, dict_out[domain])
    row +=1
workbook.close()







