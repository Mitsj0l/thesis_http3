import numpy as np
import pickle
from scapy.all import *
import ipaddress
import pandas as pd

file = "dataset/test2/1688.com_1.pcap"

infile = rdpcap(file)
packets = []
if len(infile[TCP]) != 0:
    for i in range(0, len(infile[TCP])):
        # print(scapy_cap[i].time)
        packet_n = infile[i]
        # timestamp = float(scapy_cap[i].time)
        data = [float(packet_n.time),
                int(ipaddress.ip_address(packet_n["IP"].src)),
                int(ipaddress.ip_address(packet_n["IP"].dst)),
                packet_n.sport,
                packet_n.dport,
                packet_n["IP"].len,
                packet_n["IP"].proto]
        packets.append(data)

if len(infile[UDP]) != 0:
    for i in range(0, len(infile[UDP])):
        # print(scapy_cap[i].time)
        packet_n = infile[i]
        # timestamp = float(scapy_cap[i].time)
        data = [float(packet_n.time),
                int(ipaddress.ip_address(packet_n["IP"].src)),
                int(ipaddress.ip_address(packet_n["IP"].dst)),
                packet_n.sport,
                packet_n.dport,
                packet_n["IP"].len,
                packet_n["IP"].proto]
        packets.append(data)


# Determine the public IP's
A2packets = packets
test = pd.DataFrame(A2packets)
ipaddr = test[1].unique()
public_IP = []
for i in ipaddr:
    print(i)
    addr = ipaddress.ip_address(int(i))
    # print(addr.is_private)
    if addr.is_private == False:
        public_IP.append(i)



threshold = 0.0250
result = list()

public_IP = "225127182"
for IP in public_IP:
    print(IP)
    ipaddr_iterate = test.loc[(test[1] == IP) | (test[2] == IP)]
    print(ipaddr_iterate)
    packets = np.array(ipaddr_iterate)
    if packets.shape[0]:
        # Sort based on timestamp
        packets = packets[packets[:, 0].argsort()]


    pkt_diff = ipaddr_iterate[0].astype(float).diff()
    indices_split = [0] + pkt_diff[pkt_diff > threshold].index.tolist() + [ipaddr_iterate.shape[0]]
    for start, end in zip(indices_split, indices_split[1:]):
        result.append(ipaddr_iterate[start+1:end+1])
