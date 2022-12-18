FROM ubuntu:latest

# Create app directory
ENV WORKSPACE /puppeteer
ENV OUTPUT /puppeteer/output
ENV VAR1 HELLO
RUN mkdir $WORKSPACE
WORKDIR $WORKSPACE

RUN DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update -y
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
    tshark \
    nano \
    python3-pip \
    dos2unix \
    host \
    nodejs \
    npm

# # Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

COPY main.js .
COPY launch.sh .
COPY tranco_87WV.csv .
# RUN npm ci
RUN npm install

RUN chmod -R o+rwx node_modules/puppeteer/.local-chromium
RUN chmod +x launch.sh
# COPY . .


# # If you are building your code for production
# # RUN npm ci --only=production
RUN pip install pyyaml

RUN mkdir -p /puppeteer/output


EXPOSE 8000

ENTRYPOINT ["/puppeteer/launch.sh"]