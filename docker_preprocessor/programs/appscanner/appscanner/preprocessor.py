from .reader import Reader
from .burst import Burst
from .flow import Flow
from .features import Features

import numpy as np
import pickle
from scapy.all import *
import ipaddress
import pandas as pd
from alive_progress import alive_bar
import os

print(os.environ["INPUT_RAW_DIR"])
INPUT_RAW_DIR = os.environ["INPUT_RAW_DIR"]
OUTPUT_DIR = os.environ["OUTPUT_DIR"]
PCAPDATE = os.environ["PCAPDATE"]

class Preprocessor(object):

    def __init__(self, verbose=False):
        """Preprocessor for extracting features from pcap files.

            Parameters
            ----------
            verbose : boolean, default=false
                If True, print which files are being read.
            """
        # Initialise preprocessors
        self.reader            = Reader(verbose)
        self.burstifyer        = Burst()
        self.flow_extractor    = Flow()
        self.feature_extractor = Features()

    def process(self, files, labels):
        """Extract data from files and attach given labels.

            Parameters
            ----------
            files : iterable of string
                Paths from which to extract data.

            labels : iterable of int
                Label corresponding to each path.

            Returns
            -------
            X : np.array of shape=(n_samples, n_features)
                Features extracted from files.

            y : np.array of shape=(n_samples,)
                Labels for each flow extracted from files.
            """
        # Initialise X and y
        X, y = list(), list()
        appended_data = []
        # Loop over all given files
        total = len(files)
        with alive_bar(total) as bar:
            for file, label in zip(files, labels):
                print(label)
                # print(file)
                # print(len(file))
                if os.stat(file).st_size == 0:
                    print("File {} is empty!".format(file))
                    continue
                initial = self.extract(file, label)
                if len(initial) == 0:
                    continue
                appended_data.append(initial)
                
                # initial.loc[:,'Label'] = label[0]
                # initial.loc[:,'Labelid'] = label[1]
                # data = np.array(list(self.extract(file).values())) #Main function for extracation of packet
                # data = np.array(list(initial.values())) #Main function for extracation of packet
                # data1 = np.array(list(initial.keys())) #Main function for extracation of packet

                # if len(initial) != 0 :
                    # data2 = np.concatenate((data, data1), axis=1)
                    # data = data2
                # data1 = np.array(list(self.extract(file).keys())) #Main function for extracation of packet
                # Append data to X
                # X.append(data)
                # Append label to y
                # y.append(np.array([label] * data.shape[0]))
                bar()

            # Filter empty entries from array
            # X = list(filter(lambda x: x.shape[0] != 0, X))
            # y = list(filter(lambda x: x.shape[0] != 0, y))

            # Append both X and y
            # X = np.concatenate(X)
            # y = np.concatenate(y)
            appended_data = pd.concat(appended_data, ignore_index=True)
            appended_data.reset_index()
            
            appended_data.to_csv('{}/{}_dataset.csv'.format(OUTPUT_DIR, PCAPDATE),index=False)
           
            # Return result
            return X, y

    def extract(self, file, label):
        """Extract flow features from given pcap file.

            Parameters
            ----------
            file : string
                Path to pcap file from which to extract flow features.

            Returns
            -------
            result : dict
                Dictionary of flow_key -> np.array of flow_features
                Flow tuple is defined as (timestamp, src, sport, dst, dport)
            """
        # Read packets
        # result = self.reader.read(file)

#---------- self-created ellende
        data_label = label
        infile = rdpcap(file)
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
        if len(A2packets) == 0:
            return(A2packets)
        test = pd.DataFrame(A2packets)
        ipaddr = test[1].unique()
        public_IP = []
        for i in ipaddr:
            # print(i)
            addr = ipaddress.ip_address(int(i))
            # print(addr.is_private)
            if addr.is_private == False:
                public_IP.append(i)
                
        test_array = []
        np.array(test_array)
        data = []

        if len(public_IP) == 0:
            return(public_IP)

        for IP in public_IP:
            # print(IP)
            ipaddr_iterate = test.loc[(test[1] == IP) | (test[2] == IP)]
            # print(ipaddr_iterate)
            self.packets = np.array(ipaddr_iterate)
            if self.packets.shape[0]:
                # Sort based on timestamp
                self.packets = self.packets[self.packets[:, 0].argsort()]

            result = self.packets
            # Split in burts
            result = self.burstifyer.split(result)
            # Extract flows
            # print(file)
            # print(len(result))
            result = self.flow_extractor.extract(result)
            # Extract features
            result = self.feature_extractor.extract(result) #Hier gebeurt de magie van 54 features extracatie berekeningen.
            # print(result)
            # test_array.append(result)
            
            for key in list(result.keys()):
                data.append(np.array(np.append(np.array(key), result[key])))
        
        tester = pd.DataFrame(data)
        tester.loc[:,'Label'] = label[0]
        tester.loc[:,'Labelid'] = label[1]
        # tester.to_csv('testje123.csv')
        # print(tester)

        # tester = pd.DataFrame(test_array)
        # print(tester)
        return(tester)


            # data = np.array(list(initial.values())) #Main function for extracation of packet
            # data1 = np.array(list(initial.keys())) 
#---------- self-created ellende


        # Split in burts
        result = self.burstifyer.split(result)
        # Extract flows
        print(file)
        # print(len(result))
        result = self.flow_extractor.extract(result)
        # Extract features
        result = self.feature_extractor.extract(result) #Hier gebeurt de magie van 54 features extracatie berekeningen.

        # Return result
        return result

    def save(self, outfile, X, y):
        """Save data to given outfile.

            Parameters
            ----------
            outfile : string
                Path of file to save data to.

            X : np.array of shape=(n_samples, n_features)
                Features extracted from files.

            y : np.array of shape=(n_samples,)
                Labels for each flow extracted from files.
            """
        with open(outfile, 'wb') as outfile:
            pickle.dump((X, y), outfile)

    def load(self, infile):
        """Load data from given infile.

            Parameters
            ----------
            infile : string
                Path of file from which to load data.

            Returns
            -------
            X : np.array of shape=(n_samples, n_features)
                Features extracted from files.

            y : np.array of shape=(n_samples,)
                Labels for each flow extracted from files.
            """
        with open(infile, 'rb') as infile:
            return pickle.load(infile)
