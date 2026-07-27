#!/bin/bash

SERVICE=keepalive-v2

if systemctl is-active --quiet $SERVICE; then
  echo "service: running"
else
  echo "service: stopped"
  exit 1
fi

if [ -f /var/lib/keepalive-v2/status.json ]; then
  echo "status: available"
else
  echo "status: missing"
fi

if [ -f /etc/keepalive-v2/config.json ]; then
  echo "config: available"
else
  echo "config: missing"
fi
