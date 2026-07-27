#!/bin/bash
set -e

BASE=https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main
DIR=/opt/keepalive-v2

if [ "$(id -u)" != "0" ]; then
 echo "run as root"
 exit 1
fi

command -v curl >/dev/null || apt-get update && apt-get install -y curl

mkdir -p $DIR
mkdir -p /var/lib/keepalive-v2

curl -fsSL $BASE/keepalive.py -o $DIR/keepalive.py
curl -fsSL $BASE/keepalive.service -o /etc/systemd/system/keepalive-v2.service

chmod +x $DIR/keepalive.py

systemctl daemon-reload
systemctl enable keepalive-v2
systemctl restart keepalive-v2

echo "keepalive-v2 installed"
echo "status: python3 $DIR/keepalive.py --status"
