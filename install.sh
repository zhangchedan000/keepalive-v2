#!/bin/bash
set -e

BASE=https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main
DIR=/opt/keepalive-v2
CONFIG=/etc/keepalive-v2
VERSION_FILE=$BASE/VERSION

if [ "$(id -u)" != "0" ]; then
 echo "run as root"
 exit 1
fi

if ! command -v curl >/dev/null; then
 apt-get update
 apt-get install -y curl
fi

mkdir -p $DIR
mkdir -p /var/lib/keepalive-v2
mkdir -p $CONFIG

curl -fsSL $BASE/keepalive.py -o $DIR/keepalive.py
curl -fsSL $BASE/config_loader.py -o $DIR/config_loader.py
curl -fsSL $BASE/hardware_profile.py -o $DIR/hardware_profile.py
curl -fsSL $BASE/benchmark_profile.py -o $DIR/benchmark_profile.py
curl -fsSL $BASE/healthcheck.sh -o $DIR/healthcheck.sh
curl -fsSL $BASE/keepalive.service -o /etc/systemd/system/keepalive-v2.service

if [ ! -f $CONFIG/config.json ]; then
cat > $CONFIG/config.json <<EOF
{
  "cpu_target": 20,
  "memory_target": 25,
  "network_test": true,
  "log": true,
  "cycle_days": 7
}
EOF
fi

chmod +x $DIR/keepalive.py
chmod +x $DIR/healthcheck.sh

systemctl daemon-reload
systemctl enable keepalive-v2
systemctl restart keepalive-v2

VERSION=$(curl -fsSL $VERSION_FILE 2>/dev/null || echo unknown)

echo "keepalive-v2 installed"
echo "version: $VERSION"
echo "status: python3 $DIR/keepalive.py --status"
echo "health: bash $DIR/healthcheck.sh"
