from sklearn import metrics
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn import preprocessing
import sweetviz as sv


le = preprocessing.LabelEncoder()


import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import csv
import time
import warnings
import math
warnings.filterwarnings("ignore")

time_current = time.time()
timestamp= str(time_current) 
result="./output/results_{}.csv".format(timestamp) #a CSV file is named in which the results are saved.
# filename = './output/x_train.csv'
x_train = pd.read_csv('./output/x_train.csv', index_col=None)
# x_train = pd.read_csv('./output/31_output.csv', index_col=None)
y_train1 = pd.read_csv('./output/y_train.csv', index_col=None)
y_train2 = y_train1['0']

refclasscol=list(x_train.columns.values)
print(refclasscol)

drop_columns = ['54', '55', '56', '58']

x_train = x_train.drop(drop_columns, axis=1)

x_train = pd.merge(x_train, y_train1, left_index=True, right_index=True)


x_train_unique_pcaps_labelid = x_train['1_y'].unique()
#Calculate length of external servers per pcap dataset to create extra diversication
# labelid = '1688.com_1.pcap'

def ASN_UNIQUE_FEATURES():
    for labelid in x_train_unique_pcaps_labelid:
        indexer = x_train.loc[x_train['1_y'] == labelid].index
        ASN_UNIQUE = x_train.loc[x_train['1_y'] == labelid][['ASN']].nunique()
        ASN_NAME_UNIQUE = x_train.loc[x_train['1_y'] == labelid][['ASN_Name']].nunique()

        x_train.loc[indexer,'N_ASN_UNIQUE'] = ASN_UNIQUE[0]
        x_train.loc[indexer,'N_ASN_NAME_UNIQUE'] = ASN_NAME_UNIQUE[0]

ASN_UNIQUE_FEATURES()

def TCP_UDP_FEATURES():
    for labelid in x_train_unique_pcaps_labelid:
        print(labelid)
        indexer = x_train.loc[x_train['1_y'] == labelid].index
        indexer_tcp = x_train.loc[x_train['1_y'] == labelid]['59'] == 6 
        indexer_udp = x_train.loc[x_train['1_y'] == labelid]['59'] == 17
        tcp_data = x_train.loc[x_train['1_y'] == labelid][x_train['59'] == 6]
        udp_data = x_train.loc[x_train['1_y'] == labelid][x_train['59'] == 17]

        tcp_data_unique = tcp_data['57'].unique()
        udp_data_unique = udp_data['57'].unique()

        x_train.loc[indexer,'TCP_IP_COUNT'] = len(tcp_data_unique)
        x_train.loc[indexer,'UDP_IP_COUNT'] = len(udp_data_unique)
        # len(x_train.loc[x_train['1_y'] == labelid ]['57'].unique())
        # x_train.loc[indexer,'N_EXT_IP'] = len(x_train.loc[x_train['1_y'] == labelid ]['57'].unique())
        # [x_train['57'] ].unique()
TCP_UDP_FEATURES()



# def TCP_UDP_COMBO():
#     for labelid in x_train_unique_pcaps_labelid:
#         print(labelid)
#         indexer = x_train.loc[x_train['1_y'] == labelid].index
#         len(x_train.loc[x_train['1_y'] == labelid ]['57'].unique())
#         x_train.loc[indexer,'N_EXT_IP'] = len(x_train.loc[x_train['1_y'] == labelid ]['57'].unique())
#         # [x_train['57'] ].unique()
# TCP_UDP_COMBO()
    
print(x_train['59'].nunique())
x_train = pd.get_dummies(x_train, columns=['59'])
print(x_train.shape)


# objList = x_train.select_dtypes(include = "object").columns #Get all object types in columns
# x_train[objList] = x_train[objList].apply(le.fit_transform) #Auto Encode 'object' columns to int and float's.

drop_columns = ['Unnamed: 0'] #<- 0.43

# 'ASN_Name','N_ASN_UNIQUE', 'N_ASN_NAME_UNIQUE'

x_train = x_train.drop(drop_columns, axis=1)

x_train.to_csv('output/0_preprocess_data_cleaned99.csv' ,index = False,header=True,mode="w")

my_report = sv.analyze(x_train)
my_report.show_html() # Default arguments will  generate to "SWEETVIZ_REPORT.html"


pret = x_train

# pret.groupby('1_y').mean()['N_EXT_IP']
pret.groupby('0_y')
pret.groupby('0_y').mean()['N_EXT_IP']
pret.groupby('1_y').sum().index

# for labelid in test:
#     print(labelid)
#     df.loc[df['labelID'] == labelid ]
#     indexer = df.loc[df['labelID'] == labelid].index
#     tcp_data = df.loc[df['labelID'] == labelid][df.Protocol.shift() == 6]
#     udp_data = df.loc[df['labelID'] == labelid][df.Protocol.shift() == 6]

#     df.loc[indexer,'TCP_Flow IAT Min'] = tcp_data['Flow IAT Min'].mean()
#     df.loc[indexer,'UDP_Flow IAT Min'] = udp_data['Flow IAT Min'].mean()

#     df.loc[indexer,'TCP_Flow IAT Max'] = tcp_data['Flow IAT Max'].mean()
#     df.loc[indexer,'UDP_Flow IAT Max'] = udp_data['Flow IAT Max'].mean()

#     df.loc[indexer,'TCP_Flow Duration'] = tcp_data['Flow Duration'].mean()
#     df.loc[indexer,'UDP_Flow Duration'] = udp_data['Flow Duration'].mean()

#     df.loc[indexer,'TCP_Flow Packets/s'] = tcp_data['Flow Packets/s'].mean()
#     df.loc[indexer,'UDP_Flow Packets/s'] = udp_data['Flow Packets/s'].mean()

#     df.loc[indexer,'TCP_PKT_COUNT'] = len(df.loc[df['labelID'] == labelid][df.Protocol.shift() == 6].index)
#     df.loc[indexer,'UDP_PKT_COUNT'] = len(df.loc[df['labelID'] == labelid][df.Protocol.shift() == 17].index)



x_train = pd.read_csv('./output/31_output.csv', index_col=None)

drop_columns = ['Unnamed: 0'] #<- 0.43

# 'ASN_Name','N_ASN_UNIQUE', 'N_ASN_NAME_UNIQUE'
y_train = x_train
y_train = y_train.drop(drop_columns, axis=1)


y_train = pd.read_csv('./output/tcp_udp_5_extrafeatures/31_output.csv', index_col=None)
x_train = y_train

y_train.to_csv('output/tcp_udp_5_extrafeatures/31_output_final.csv' ,index = False,header=True,mode="w")