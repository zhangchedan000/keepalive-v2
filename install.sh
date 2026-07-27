#!/bin/bash
set -e

BASE=https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main
DIR=/opt/keepalive-v2

mkdir -p $DIR
curl -fsSL $BASE/keepalive.py -o $DIR/keepalive.py
curl -fsSL $BASE/keepalive.service -o /etc/systemd/system/keepalive-v2.service
chmod +x $DIR/keepalive.py

systemctl daemon-reload
systemctl enable --now keepalive-v2

echo "keepalive-v2 installed"
