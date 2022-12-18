#!/bin/bash

#Init...
mkdir -p dataset/appscanner

# tcpdump_and_cicflowmeter/convert_pcap_csv.sh -k -d ../output/cicflow/ ../output/26-07-2022_09-45-07/*
#Make CICFlowmeter dataset directories
# MINWAIT=10
# MAXWAIT=85
# sleep $((MINWAIT+RANDOM % (MAXWAIT-MINWAIT))); #Initiate wait so that parallel processing containers can create their LOCK Files.
# sleep $[ ( $RANDOM % 20 )  + 1 ]s;

LOCKFILECIC="lock_file_CIC" #Define lock_file file for parallel docker processing.
LOCKFILEAPPSCANNER="lock_file_APPSCAN" #Define lock_file file for parallel docker processing.
LOCKFILENCAP="lock_file_NCAP" #Define lock_file file for parallel docker processing.
LOCKFILECONVERTED="lock_file_CONVERTED" #Define lock_file file for parallel docker processing.

# #Create appropiate folders based on the the gathered PCAP-files by different containers
for FILE in output/*/; 
    do echo $FILE;
    PCAPDATE=`echo ${FILE} | cut -d '/' -f2`;
    mkdir -p dataset/cicflow/$PCAPDATE
    # mkdir -p dataset/appscanner/$PCAPDATE
done

# #Rename samples to reflect day of capture. This takes care for redundant samples of domain names that have been captured on previous/later days.
for FILE in output/*/; 
    do echo $FILE;
    if [ -f "$FILE/$LOCKFILECONVERTED" ]; then
        echo "$LOCKFILECONVERTED exists for $FILE. Skipping..."
    else
        echo "$LOCKFILECONVERTED does not exist. Initiating renaming process for this directory $FILE dataset"
        touch $FILE/$LOCKFILECONVERTED
        PCAPDATE=`echo ${FILE} | cut -d '/' -f2`;
        for PCAPFILE in $FILE*.*;
            # do echo $PCAPFILE;
            do PCAPDATE=`echo ${PCAPFILE} | cut -d '/' -f2`;
                        # #Dirty way of adding an additional label with data into each dataset :+
            FILENAME=`echo ${PCAPFILE} | cut -d '/' -f3 | cut -d '_' -f 1`;
            LABEL_NR=`echo ${PCAPFILE} | cut -d '/' -f3 | cut -d '_' -f 2 | cut -d '.' -f 1`;
            FILENAME_LABEL=`echo ${FILENAME}_${LABEL_NR}`;
            FILENAME_EXT=`echo ${PCAPFILE} | cut -d '/' -f3 | cut -d '_' -f 2 | cut -d '.' -f 2`;
            # LABELID=`echo ${PCAPFILE} | cut -d '/' -f3 | cut -d '.' -f 1,2`;
            # EXT=`echo ${PCAPFILE} | cut -d '/' -f3 | cut -d '.' -f 3`;
            PCAP_PATH=`echo ${PCAPFILE} | cut -d '/' -f 1,2`;

            # OUTPUTFILENAME="${PCAP_PATH}/${LABELID}_${PCAPDATE}.${EXT}"
            OUTPUTFILENAME="${PCAP_PATH}/${FILENAME_LABEL}_${PCAPDATE}.${FILENAME_EXT}"
            echo $OUTPUTFILENAME;
            mv ${PCAPFILE} $OUTPUTFILENAME
        done
    fi
done

#Appscanner application
for FILE in output/*/; 
    do echo $FILE;
    if [ -f "$FILE/$LOCKFILEAPPSCANNER" ]; then
        echo "$LOCKFILEAPPSCANNER exists for $FILE. Skipping..."
    else
        # do echo $FILE;
        echo "$LOCKFILEAPPSCANNER does not exist. Initiating Appscanner processing for this directory $FILE dataset"
        touch $FILE/$LOCKFILEAPPSCANNER
        PCAPDATE=`echo ${FILE} | cut -d '/' -f2`;
        echo $PCAPDATE
        # INPUT_RAW_DIR=$FILE
        # OUTPUT_DIR = "dataset/appscanner/"
        export INPUT_RAW_DIR=$FILE;
        export OUTPUT_DIR="dataset/appscanner/";
        export PCAPDATE=`echo ${FILE} | cut -d '/' -f2`;
        python3 programs/appscanner/example.py
    fi
done

# #CICFlow application to convert PCAP to CSV with 75 features
for FILE in output/*/; 
    
    do echo $FILE;
        if [ -f "$FILE/$LOCKFILECIC" ]; then
            echo "$LOCKFILECIC exists for $FILE. Skipping..."

        else 
            echo "$LOCKFILECIC does not exist. Initiating CICFlow processing for this directory $FILE dataset"
            touch $FILE/$LOCKFILECIC
            for PCAPFILE in $FILE*.pcap;
                do echo $PCAPFILE;
                    PCAPDATE=`echo ${PCAPFILE} | cut -d '/' -f2`;

                    ./cicflowmeter/tcpdump_and_cicflowmeter/convert_pcap_csv.sh -k -d dataset/cicflow/$PCAPDATE/ $PCAPFILE ;
                    echo $PCAPDATE
                    echo $PCAPFILE
                    
                    #Dirty way of adding an additional label with data into each dataset :+
                    LABELID=`echo ${PCAPFILE} | cut -d '/' -f3 | cut -d '.' -f 1,2`;
                    LABELGENERAL=`echo ${LABELID} | cut -d '_' -f1`;
                    LABELCOMBO=`echo ${LABELGENERAL},${LABELID}`;

                    LABELNEW="Label,labelID"

                    OUTPUTFILENAME="dataset/cicflow/${PCAPDATE}/${LABELID}_ISCX.csv"
                    echo $LABELID;
                    echo $LABELGENERAL;
                    echo $LABELCOMBO;
                    echo $OUTPUTFILENAME;
                    sed -i "s/NeedManualLabel/${LABELCOMBO}/g" -i $OUTPUTFILENAME
                    sed -i "s/Label/${LABELNEW}/g" -i $OUTPUTFILENAME
            
            done
        fi
    # sleep $((MINWAIT+RANDOM % (MAXWAIT-MINWAIT))) 
done


# #NETCAP Statistics creator
# for PCAP_FOLDER in output/*;
#     do echo $PCAP_FOLDER;
#     PCAPDATE=`echo ${PCAP_FOLDER} | cut -d '/' -f2`;
#     mkdir -p dataset/netcap/$PCAPDATE
#     if [ -f "$PCAP_FOLDER/$LOCKFILENCAP" ]; then
#         echo "$LOCKFILENCAP exists for $FILE. Skipping..."

#     else 
#         echo "$LOCKFILENCAP does not exist. Initiating processing request for this directory $PCAP_FOLDER dataset"
#         touch $PCAP_FOLDER/$LOCKFILENCAP
#         for FILE in $PCAP_FOLDER/*.pcap;
#             do echo $FILE;
#             NETCAPEXT=`echo ${FILE} | cut -d '/' -f 3 | cut -d '.' -f 1,2`;
#             ./netcap/net capture -read $FILE -out="dataset/netcap/$PCAPDATE/$NETCAPEXT/"
#             echo $NETCAPEXT
#             FILENAME=`echo ${FILE} | cut -d '/' -f 3 | cut -d '.' -f 1,2`;
#             TEST="dataset/netcap/$PCAPDATE/$FILENAME"
#             echo $TEST
#             for FILE1 in $TEST/*.gz;
#                 do echo $FILE1;
#                 NETCAPEXT=`echo ${FILE1} | cut -d '/' -f5 | cut -d '.' -f1`;
#                 SUBJECT=`echo ${FILE1} | cut -d '/' -f4`;

#                 ./netcap/net dump -read $FILE1 -csv > "${TEST}/${SUBJECT}_${NETCAPEXT}.csv"
#             done
#             cd ${TEST}
#             ls | grep -v .csv$| xargs rm
#             cd /puppeteer
#         done
#     fi
#     # sleep $((MINWAIT+RANDOM % (MAXWAIT-MINWAIT))) 
# done



#ASN_Lookup enhancements. Credits https://github.com/banviktor/asnlookup
echo "Initiating ASN Lookup DB Prep"
cd /puppeteer/programs/asnlookup
./pull_rib.sh
bzcat rib.*.bz2 | ./asnlookup-utils convert --input - --output my.db

#Credits https://db-ip.com/db/download/ip-to-asn-lite
wget https://download.db-ip.com/free/dbip-asn-lite-2022-09.csv.gz
gzip -d dbip-asn-lite-2022-09.csv.gz

cd $WORKSPACE


# #Merge APPSCANNER-dataset
for FILE in dataset/appscanner/*; 
    do echo $FILE;
    awk '(NR == 1) || (FNR > 1)' $FILE >> dataset/appscanner_dataset_merged_raw.csv
done
# #Easy way for merging all samples with 1 unique header
cat dataset/appscanner_dataset_merged_raw.csv | grep 'Labelid' | uniq > dataset/appscanner_dataset_merged.csv
cat dataset/appscanner_dataset_merged_raw.csv | grep -v 'Labelid' >> dataset/appscanner_dataset_merged.csv
rm dataset/appscanner_dataset_merged_raw.csv #Clean-up of old files

#Retrieve the unique external IP-addresses for APPSCANNER dataset:
cat dataset/appscanner_dataset_merged.csv | grep -v 'Labelid' | awk -F "," '{print $4}' | sort | uniq > dataset/appscanner_dataset_merged_ip.txt
APPSC_IPFILE="dataset/appscanner_dataset_merged_ip.txt"
cat ${APPSC_IPFILE} |  /puppeteer/programs/asnlookup/asnlookup --db /puppeteer/programs/asnlookup/my.db --batch > dataset/appscanner_dataset_merged_ip_ASN.txt

#Dataset enrichment with ASN + ASN_Owner
python3 /puppeteer/programs/asnlookup/ASN_appscanner.py
rm dataset/appscanner_dataset_merged.csv dataset/appscanner_dataset_merged_ip.txt dataset/appscanner_dataset_merged_ip_ASN.txt






#Merge  CIC-dataset
for FILE in dataset/cicflow/*/*; 
    do echo $FILE;
    awk '(NR == 1) || (FNR > 1)' $FILE >> dataset/cicflow/dataset_merged.csv
done
#Easy way for merging all samples with 1 unique header
cat dataset/cicflow/dataset_merged.csv | grep 'Flow' | uniq > dataset/cicflow/dataset.csv
cat dataset/cicflow/dataset_merged.csv | grep -v 'Flow' >> dataset/cicflow/dataset.csv
rm dataset/cicflow/dataset_merged.csv #Clean-up of old files

#Retrieve the unique external IP-addresses for CICFLOW dataset:
echo $PWD
cat dataset/cicflow/dataset.csv | awk -F ',' '{print $2}' | grep -v "IP" | sort | uniq > dataset/cicflow/dataset_cic_merged_raw_ip.txt
cat dataset/cicflow/dataset.csv | awk -F ',' '{print $4}' | grep -v "IP" | sort | uniq >> dataset/cicflow/dataset_cic_merged_raw_ip.txt
cat dataset/cicflow/dataset_cic_merged_raw_ip.txt | sort | uniq > dataset/cicflow/dataset_cic_merged_ip.txt
APPSC_IPFILE="dataset/cicflow/dataset_cic_merged_ip.txt"
cat ${APPSC_IPFILE} |  /puppeteer/programs/asnlookup/asnlookup --db /puppeteer/programs/asnlookup/my.db --batch > dataset/cicflow/dataset_cic_merged_ip_ASN.txt

python3 /puppeteer/programs/asnlookup/ASN_cicflow.py

cd /puppeteer/dataset/cicflow
rm dataset.csv dataset_cic_merged_ip.txt dataset_cic_merged_ip_ASN.txt dataset_cic_merged_raw_ip.txt
cd $WORKSPACE

echo "Job done, thanks for the fish!" 