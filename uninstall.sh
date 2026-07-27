#!/bin/bash
set -e

systemctl disable --now keepalive-v2 2>/dev/null || true
rm -f /etc/systemd/system/keepalive-v2.service
rm -rf /opt/keepalive-v2
rm -rf /var/lib/keepalive-v2
systemctl daemon-reload

echo "keepalive-v2 removed"
