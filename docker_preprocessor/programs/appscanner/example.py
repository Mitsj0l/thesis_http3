# Imports
from appscanner.preprocessor import Preprocessor
from appscanner.appscanner   import AppScanner
from sklearn.preprocessing   import MinMaxScaler
from os.path import join
import glob
import numpy as np
import pandas as pd
import os
import pathlib

print(os.environ["INPUT_RAW_DIR"])
INPUT_RAW_DIR = os.environ["INPUT_RAW_DIR"]
OUTPUT_DIR = os.environ["OUTPUT_DIR"]
PCAPDATE = os.environ["PCAPDATE"]


# directory = '24-08-2022_17-29-01'
# directory = '24-08-2022_17-28-07'
# directory = INPUT_RAW_DIR
directory = "/puppeteer/{}".format(INPUT_RAW_DIR)
print(directory)
# directory = 'dataset/test1'
# directory = 'dataset/test2'
# directory = 'dataset/24-08-2022_17-07-49'


# train_glob = ('*1.pcap','*2.pcap','*3.pcap','*4.pcap','*5.pcap','*6.pcap','*7.pcap','*8.pcap')
# train_glob = ('*1.pcap','*2.pcap','*3.pcap','*4.pcap','*5.pcap','*6.pcap','*7.pcap','*8.pcap','*9.pcap','*10.pcap')
train_glob = ('*pcap')
# iterate over files in
# that directory

train_pcap_list = []
train_pcap_list_label = []
train_pcap_list_temp = []
# train_pcap_list = glob.glob('/puppeteer/output/23-08-2022_17-22-57/*.pcap')
train_pcap_list_temp = list(pathlib.Path(directory).glob('*.pcap'))
for pcap in train_pcap_list_temp:
   pcap = str(pcap)
   train_pcap_list.append(pcap)

# print(train_pcap_list)
# for ext in train_glob:
#    # train_pcap_list.extend(glob(join(directory, ext)))
#    train_pcap_list.extend(glob.glob('{}*.pcap'.format(directory)))
#    print(ext)
#    # print(train_pcap_list)

for pcap_item in train_pcap_list:
   pcap_item = str(pcap_item)
   # print(pcap_item)
   step1 = pcap_item.split("/")
   # print(step1)
   step2 = step1[4].split("_")
   # print(step2)

   step3 = step2[0]
   # print(step3)

   combine = [step3, step1[4] ]
   print(combine)

   # print(step3)
   train_pcap_list_label.append(combine)
   # print(train_pcap_list_label)

# print(train_pcap_list_label)

# Create preprocessor
preprocessor = Preprocessor()
# Load from files
# print(train_pcap_list)
# print(len(train_pcap_list))
# print(train_pcap_list_label)
# print(len(train_pcap_list_label))
X_train, y_train = preprocessor.process(
    files = train_pcap_list,
    labels = train_pcap_list_label
)

print("Appscanner job Finished, thanks for the fish!")
# # Load from files
# X_test, y_test = preprocessor.process(
#     # files  = ['<path_file_1>', ..., '<path_file_n>'], # Path   to your own test pcap files
#     files  = test_pcap_list,
#     # labels = ['<label_1>'    , ..., '<label_n>'],     # Labels of your own test pcap files
#     labels = test_pcap_list_label
# )



# pd.DataFrame(X_train).to_csv("output/x_train.csv", index=False)
# # pd.DataFrame(X_test).to_csv("output/x_test.csv", index=False)
# # pd.DataFrame(y_test).to_csv("output/y_test.csv", index=False)
# pd.DataFrame(y_train).to_csv("output/y_train.csv", index=False)


# # Scale features
# scaler = MinMaxScaler()
# X_train = scaler.fit_transform(X_train)
# X_test  = scaler.transform(X_test)


# # Pass through appscanner
# scanner = AppScanner(threshold=0.9)

# # Fit scanner
# scanner.fit(X_train, y_train)
# # Predict labels of test data
# y_pred = scanner.predict(X_test)

# np.sum(y_pred == y_test)
# print(np.sum(y_pred == y_test)/len(y_pred))




# from scapy.all import *

# filename="24-08-2022_17-29-01\discord.gg_1.pcap"
# scapy_cap = rdpcap(filename)
# UDP in scapy_cap
# pkt = IP()/TCP()
# pkt.haslayer(scapy_cap)

# pkt2 = IP()/UDP()
# pkt2.haslayer(scapy_cap)

# sniff(filter="ip", store=0, offline=scapy_cap)

# countTCP = 0
# countUDP = 0
# for i in range(0, len(scapy_cap)):
#           pkt = scapy_cap[1]
#           if (TCP in pkt):
#                    countTCP+= 1
#           elif (UDP in pkt):
#                    countUDP+= 1

# for packet in scapy_cap:
#     # We're only interested packets with a DNS Round Robin layer
#     if packet.haslayer(TCP):
#       print(packet)
#         # If the an(swer) is a DNSRR, print the name it replied with.
#       #   if isinstance(packet.an, DNSRR):
#       #       print(packet.an.rrname)

# if len(scapy_cap[UDP]) ==3891:
#    print("Yes")

# else:
#    print("no no")
#    None

# def main():
#    sniff(offline='traffic.pcap', prn=my_method,store=0)
#    sniff(prn=self.extract_UDP, lfilter=lambda x: UDP in x, offline=infile)

#    sniff(prn=self.extract, lfilter=lambda x: TCP in x, offline=infile)
#    sniff(prn=self.extract_UDP, lfilter=lambda x: UDP in x, offline=infile)


# def extract_UDP(self, packet):
#    """Extract relevant fields from given packet and adds it to globel
#       self.packets variable.

#       Parameters
#       ----------
#       packet : scapy.IP
#             Scapy IP packet extracted by sniff function.
#       """
#    # Extract relevant content from packet
#    data = [float(packet.time),
#             int(ipaddress.ip_address(packet["IP"].src)),
#             int(ipaddress.ip_address(packet["IP"].dst)),
#             packet["UDP"].sport,
#             packet["UDP"].dport,
#             packet["IP"].len]
#    # Add packet to buffer
#    self.packets.append(data)

# mylist = {(1661368493.16312, '192.168.0.72', 53297.0, '142.250.179.136', 443.0): array([-1.27800000e+03, -5.30000000e+01, -1.13860000e+03,  2.39920000e+02,
#         3.66584651e+02,  1.34384306e+05,  2.43224038e+00,  4.30673561e+00,
#        -1.27800000e+03, -1.27800000e+03, -1.27800000e+03, -1.27800000e+03,
#        -1.27800000e+03, -1.27800000e+03, -1.27800000e+03, -1.27800000e+03,
#        -4.97600000e+02,  6.50000000e+01,  6.10000000e+01,  1.27800000e+03,
#         1.08970588e+02,  8.44757785e+01,  2.11413638e+02,  4.46957264e+04,
#         5.45530517e+00,  3.07156860e+01,  6.10000000e+01,  6.10000000e+01,
#         6.10000000e+01,  6.10000000e+01,  6.10000000e+01,  6.10000000e+01,
#         6.10000000e+01,  6.18000000e+01,  9.00000000e+01,  3.40000000e+01,
#        -1.27800000e+03,  1.27800000e+03, -7.10141414e+02,  6.45756351e+02,
#         6.76275484e+02,  4.57348531e+05,  5.11008094e-01, -1.27225534e+00,
#        -1.27800000e+03, -1.27800000e+03, -1.27800000e+03, -1.27800000e+03,
#        -1.27800000e+03, -2.21200000e+02,  6.10000000e+01,  6.10000000e+01,
#         6.10000000e+01,  9.90000000e+01]), (1661368498.036889, '192.168.0.72', 44219.0, '35.186.220.184', 443.0): array([-1.27800000e+03, -5.30000000e+01, -6.86111111e+02,  5.26123457e+02,
#         5.80826447e+02,  3.37359361e+05, -6.27623695e-02, -2.36088773e+00,
#        -1.27800000e+03, -1.27800000e+03, -1.27800000e+03, -1.13160000e+03,
#        -5.46000000e+02, -3.41200000e+02, -1.88600000e+02, -9.38000000e+01,
#        -5.30000000e+01,  9.00000000e+00,  6.10000000e+01,  1.27800000e+03,
#         3.08833333e+02,  3.23055556e+02,  4.78538783e+02,  2.28999367e+05,
#         2.36518546e+00,  5.67112851e+00,  6.50000000e+01,  6.90000000e+01,
#         6.90000000e+01,  6.90000000e+01,  1.26000000e+02,  1.83000000e+02,
#         1.88000000e+02,  1.93000000e+02,  7.35500000e+02,  6.00000000e+00,
#        -1.27800000e+03,  1.27800000e+03, -2.88133333e+02,  5.62560000e+02,
#         7.27400643e+02,  5.29111695e+05,  6.95689194e-02,  1.63044908e-01,
#        -1.27800000e+03, -1.27800000e+03, -4.94800000e+02, -1.88600000e+02,
#        -5.30000000e+01, -7.40000000e+00,  6.74000000e+01,  9.18000000e+01,
#         1.89000000e+02,  1.50000000e+01])}


# from scapy.all import *
# import numpy as np
# import ipaddress

# packets = []
# scapy_cap = rdpcap('dataset/test/arxiv.org_4.pcap')


# def extract_UDP(packet):
#    """Extract relevant fields from given packet and adds it to globel
#       self.packets variable.

#       Parameters
#       ----------
#       packet : scapy.IP
#             Scapy IP packet extracted by sniff function.
#       """
#    # Extract relevant content from packet
#    data = [float(packet.time),
#             int(ipaddress.ip_address(packet["IP"].src)),
#             int(ipaddress.ip_address(packet["IP"].dst)),
#             packet["UDP"].sport,
#             packet["UDP"].dport,
#             packet["IP"].len,
#             packet["IP"].proto]
#    # Add packet to buffer
#    packets.append(data)

# sniff(prn=extract_UDP, lfilter=lambda x: UDP in x, offline=scapy_cap)

