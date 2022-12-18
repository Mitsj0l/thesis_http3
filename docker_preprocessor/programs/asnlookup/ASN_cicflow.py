from cgi import test
import pandas as pd
import numpy as np
import ipaddress


test1 = pd.read_csv('/puppeteer/dataset/cicflow/dataset_cic_merged_ip.txt', names=['IP'])
test2 = pd.read_csv('/puppeteer/dataset/cicflow/dataset_cic_merged_ip_ASN.txt', names=['ASN'])
test0 = pd.read_csv('/puppeteer/programs/asnlookup/dbip-asn-lite-2022-09.csv', names=['begin_IP', 'end_IP','ASN','ASN_Name'])
test_appscanner = pd.read_csv('/puppeteer/dataset/cicflow/dataset.csv')
test9 = test_appscanner

test3 = test1.join(test2)
test3 = test3.replace('not found', '0')
test3["ASN"] = pd.to_numeric(test3["ASN"])
test0["ASN"] = pd.to_numeric(test0["ASN"])
testx = test3.merge(test0[['ASN','ASN_Name']], on='ASN', how='left')
testx = testx.drop_duplicates(subset='IP')


IP_Private = []
for i in testx['IP']:
    # print(i)
    ipaddress.ip_address(i).is_private
    addr = ipaddress.ip_address(i)
    # print(addr.is_private)
    if addr.is_private == True:
        IP_Private.append(i)

print(testx.shape)
for IP in IP_Private:
    print(IP)
    testx.drop(testx[testx['IP'] == IP].index, inplace = True)
print(testx.shape)


# test9.columns = test9.columns.str.replace('3', 'Dst IP')
testx.rename(columns = {'IP':'Dst IP'}, inplace = True)
print(test9.shape)
df_dst = test9.merge(testx[['Dst IP','ASN','ASN_Name']], on="Dst IP")
print(test9.shape)

testx.rename(columns = {'Dst IP':'Src IP'}, inplace = True)
print(test9.shape)
df_src = test9.merge(testx[['Src IP','ASN','ASN_Name']], on="Src IP")
print(test9.shape)


df_merged = pd.concat([df_src, df_dst], axis=0)

df_merged.to_csv('/puppeteer/dataset/cicflow/cicflow_dataset.csv')