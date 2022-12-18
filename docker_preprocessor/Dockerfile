FROM node:latest

ENV WORKSPACE /puppeteer
ENV OUTPUT /puppeteer/output
ENV DATASET /puppeteer/dataset
ENV VAR1 HELLO
RUN mkdir $WORKSPACE
WORKDIR $WORKSPACE

RUN apt-get update
RUN apt-get install -y \
    libnspr4 \
    libnss3 \
    libgbm-dev \
    libpangocairo-1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libcups2 \
    libxss1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libgtk-3-0 \
    tcpdump \
    net-tools \
    tcpdump \
    dos2unix \
    openjdk-11-jdk \
    maven \
    gradle \
    libpcap-dev \
    python3-pip

    

COPY launch.sh .
COPY dataset_enrichment.sh .

RUN chmod +x launch.sh
RUN chmod +x dataset_enrichment.sh

RUN mkdir -p ${WORKSPACE}/output
RUN mkdir -p ${WORKSPACE}/dataset
RUN mkdir -p ${WORKSPACE}/dataset/cicflow
RUN mkdir -p ${WORKSPACE}/dataset/netcap
RUN mkdir -p ${WORKSPACE}/dataset/appscanner
RUN mkdir -p ${WORKSPACE}/programs/appscanner
RUN mkdir -p ${WORKSPACE}/programs/asnlookup
RUN mkdir -p ${WORKSPACE}/netcap

COPY programs/appscanner/ ${WORKSPACE}/programs/appscanner/
COPY programs/asnlookup/ ${WORKSPACE}/programs/asnlookup/


COPY binaries/asnlookup-linux-amd64-v0.1.0.tar.gz .
COPY binaries/pull_rib.sh ${WORKSPACE}/programs/asnlookup

RUN tar -xvzf asnlookup-linux-amd64-v0.1.0.tar.gz -C ${WORKSPACE}/programs/asnlookup
RUN rm asnlookup-linux-amd64-v0.1.0.tar.gz
RUN chmod +x ${WORKSPACE}/programs/asnlookup/asnlookup
RUN chmod +x ${WORKSPACE}/programs/asnlookup/asnlookup-utils
RUN chmod +x ${WORKSPACE}/programs/asnlookup/pull_rib.sh

COPY binaries/netcap_nodpi-v0.6.11_linux_amd64_libc.tar.gz .
RUN tar -xvzf netcap_nodpi-v0.6.11_linux_amd64_libc.tar.gz -C netcap
RUN mv netcap/netcap_nodpi-v0.6.11_linux_amd64_libc/* netcap/
RUN rm -rf netcap/netcap_nodpi-v0.6.11_linux_amd64_libc/
RUN rm netcap_nodpi-v0.6.11_linux_amd64_libc.tar.gz

COPY binaries/TCPDUMP_and_CICFlowMeter-master.zip .
RUN mkdir -p ${WORKSPACE}/cicflowmeter
RUN unzip TCPDUMP_and_CICFlowMeter-master.zip -d cicflowmeter
RUN rm TCPDUMP_and_CICFlowMeter-master.zip

RUN pip install scapy numpy pandas scikit-learn alive_progress


ENTRYPOINT ["/puppeteer/launch.sh"]