from scapy.all import *
import numpy as np
import ipaddress
import pandas as pd


class Reader(object):

    def __init__(self, verbose=True):
        """Reader object for reading packets from .pcap files.

            Parameters
            ----------
            verbose : boolean, default=false
                If True, print which files are being read.
            """
        self.verbose = verbose

    def read(self, infile):
        """Read TCP packets from input file.

            Parameters
            ----------
            infile : string
                pcap file from which to read packets.

            Returns
            -------
            result : list
                List of packets extracted from pcap file.
                Each packet is represented as a list of:
                 - timestamp
                 - IP source (in byte representation)
                 - IP destination (in byte representation)
                 - TCP source port
                 - TCP destination port
                 - packet length.
            """
        # If verbose, print loading file
        if self.verbose:
            print("Loading {}...".format(infile))

        # Set buffer of packets
        
        # Process packets in infile

        infile = rdpcap(infile)
        # print(len(scapy_cap[TCP]))
        amount_tcp_pkt = len(infile[TCP])
        amount_udp_pkt = len(infile[UDP])


        # sniff(prn=self.extract, lfilter=lambda x: TCP in x, offline=infile)
        # sniff(prn=self.extract_UDP, lfilter=lambda x: UDP in x, offline=infile)
        #Created the following loop since Scapy was providing/using current time,
        #Thus appscanner was calculing based on wront metrics...
        # infile = rdpcap(infile)
        self.packets = []
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
                self.packets.append(data)

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
                self.packets.append(data)
        

        # Determine the public IP's
        A2packets = self.packets
        test = pd.DataFrame(A2packets)
        ipaddr = test[1].unique()
        public_IP = []
        for i in ipaddr:
            print(i)
            addr = ipaddress.ip_address(int(i))
            # print(addr.is_private)
            if addr.is_private == False:
                public_IP.append(i)

        for IP in public_IP:
            print(IP)
            ipaddr_iterate = test.loc[(test[1] == IP) | (test[2] == IP)]
            print(ipaddr_iterate)
            self.packets = np.array(self.packets)
            if self.packets.shape[0]:
                # Sort based on timestamp
                self.packets = self.packets[self.packets[:, 0].argsort()]

        # print(len(scapy_cap[UDP]))
        # if len(scapy_cap[UDP]) != 0:
        #     if self.verbose:
        #         print("Processing {} UDP Frames of {}...".format(len(scapy_cap[UDP]), infile))
        #     sniff(prn=self.extract_UDP, lfilter=lambda x: UDP in x, offline=infile)


        # Convert to numpy array
        self.packets = np.array(self.packets)
        # In case of packets, sort on timestamp
        if self.packets.shape[0]:
            # Sort based on timestamp
            self.packets = self.packets[self.packets[:, 0].argsort()]

        # Return extracted packets
        return self.packets

    def extract(self, packet):
        """Extract relevant fields from given packet and adds it to globel
           self.packets variable.

            Parameters
            ----------
            packet : scapy.IP
                Scapy IP packet extracted by sniff function.
            """
        # Extract relevant content from packet
        data = [float(packet.time),
                int(ipaddress.ip_address(packet["IP"].src)),
                int(ipaddress.ip_address(packet["IP"].dst)),
                packet["TCP"].sport,
                packet["TCP"].dport,
                packet["IP"].len,
                packet["IP"].proto]
        # Add packet to buffer
        self.packets.append(data)

    def extract_UDP(self, packet):
        """Extract relevant fields from given packet and adds it to globel
           self.packets variable.

            Parameters
            ----------
            packet : scapy.IP
                Scapy IP packet extracted by sniff function.
            """
        # Extract relevant content from packet
        data = [float(packet.time),
                int(ipaddress.ip_address(packet["IP"].src)),
                int(ipaddress.ip_address(packet["IP"].dst)),
                packet["UDP"].sport,
                packet["UDP"].dport,
                packet["IP"].len,
                packet["IP"].proto]
        # Add packet to buffer
        self.packets.append(data)
