#!/bin/bash

# Create needed directories (workaround for Azure Containers) https://stackoverflow.com/questions/70308541/azure-container-cant-access-a-mounted-volume-on-startup-why
mkdir -p ${WORKSPACE}/output
mkdir -p ${WORKSPACE}/feature_extract

#Sequential function
# head -n 100 tranco_87WV.csv > custom.csv

MINWAIT=1
MAXWAIT=30
sleep $((MINWAIT+RANDOM % (MAXWAIT-MINWAIT)))

#Randomizing function :)
init_lines=1000
lines=3
input_file=tranco_87WV.csv


for i in {1..10}; do
    #Pak de 1000 populaire bestemmingen, stom deze in de blender en pak 500 random lines hiervan; zorg voor confusion in meerdere containers.
    #Retrieve first 1000 lines of Tranco list, random sort and retrieve the 500 lines; tries to create a balanced raw dataset.
    <$input_file head -n $init_lines | sort -R | head -n $lines > custom.csv

    # <$input_file sort -R | head -n $lines > custom.csv

    cat custom.csv | cut -d ',' -f2 > main.csv

    dos2unix main.csv

    echo "Epoch $i times"

    timestamp_dir=$(date +%d-%m-%Y_%H-%M-%S)
    mkdir $OUTPUT/$timestamp_dir

    for i in $(cat main.csv); do
        #Verify if domain exists:
        if ! host $i > /dev/null
            then
                echo "No IP for ${i}"
            else
                echo "Capturing data of $i"
                for iteration in {1..10}; do
                    tcpdump -i eth0 -n port '(80 or 443)' -w $OUTPUT/$timestamp_dir/${i}_${iteration}.pcap &
                    PROC_TCPDUMP_ID=$!
                    # echo $PROC_TCPDUMP_ID
                    sleep 5

                    iteration_loop=$iteration website=$i timestamp=$timestamp_dir node --unhandled-rejections=strict main.js & #Aftrappen van Nodejs script
                    PROC_NODE_ID=$!
                    # echo $PROC_NODE_ID

                    while kill -0 "$PROC_NODE_ID" >/dev/null 2>&1; do
                        # echo "PROCESS IS RUNNING"
                        :
                    done

                    echo "Process finished - sleep 15 seconds"
                    sleep 7

                    kill -2 $PROC_TCPDUMP_ID
                    sleep 3

                    #Outdated pre-processing; might use CICFlowmeter, Cisco Mercury or Netcap
                    # tshark -r $OUTPUT/$timestamp_dir/$i.pcap -V -T json > $OUTPUT/$timestamp_dir/$i.pcap.json

                    # exit 0
                done
            fi
    done
done
