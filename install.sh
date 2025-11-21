#!/bin/bash
apt update -y && apt install -y python3 git
git clone https://github.com/fraud1843/fake-botnet-c2.git
cd fake-botnet-c2
chmod +x main.py
nohup ./main.py > /dev/null 2>&1 &
echo "Fake C2 running on port 9977"
echo "http://$(curl -s ifconfig.me):9977"
