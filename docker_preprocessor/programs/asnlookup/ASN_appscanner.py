import pandas as pd
import numpy as np

# cat 1_prepped.csv | cut -d ',' -f2 | grep -iv IP | sort  | uniq > 1_prepped_IP_Unique.txt
# FILENAME="1_prepped_IP_Unique.txt"
# cat ${FILENAME} |  ./asnlookup --db my.db --batch > 21_prepped_IP_Unique_ASN.txt


test1 = pd.read_csv('/puppeteer/dataset/appscanner_dataset_merged_ip.txt', names=['IP'])
test2 = pd.read_csv('/puppeteer/dataset/appscanner_dataset_merged_ip_ASN.txt', names=['ASN'])
# data = pd.read_csv('ip2asn-v4.tsv',sep='\t', names=['begin_IP', 'end_IP','ASN','Country_Code','ASN_Name'])
test0 = pd.read_csv('/puppeteer/programs/asnlookup/dbip-asn-lite-2022-09.csv', names=['begin_IP', 'end_IP','ASN','ASN_Name'])
# test5 = pd.read_csv('/Users/mitchell/Downloads/asnlookup-darwin-amd64-v0.1.0/asn_name.txt', names=['ASN','ASN_Name'])
# test9 = pd.read_csv('/Users/mitchell/Downloads/asnlookup-darwin-amd64-v0.1.0/1_prepped.csv')
test_appscanner = pd.read_csv('/puppeteer/dataset/appscanner_dataset_merged.csv')
test9 = test_appscanner

test3 = test1.join(test2)
test3 = test3.replace('not found', '0')
test3["ASN"] = pd.to_numeric(test3["ASN"])
test0["ASN"] = pd.to_numeric(test0["ASN"])


# test4 = test0['ASN'].unique()
# # cat dbip-asn-lite-2022-08.csv | cut -d ',' -f 3,4
# test3.groupby('ASN').ASN.apply(lambda x : test0.tolist()).to_frame()['ASN_Name'].apply(pd.Series).fillna(' ')
# test3.groupby('ASN').ASN.apply(lambda x : test0.tolist()).to_frame()['ASN_Name'].apply(pd.Series).add_prefix('Class_').fillna(' ')

testx = test3.merge(test0[['ASN','ASN_Name']], on='ASN', how='left')
testx = testx.drop_duplicates(subset='IP')

test9.columns = test9.columns.str.replace('3', 'Dst IP')
testx.columns = testx.columns.str.replace('IP', 'Dst IP')
test9 = test9.merge(testx[['Dst IP','ASN','ASN_Name']], on="Dst IP")
test9.to_csv('/puppeteer/dataset/appscanner_dataset.csv')