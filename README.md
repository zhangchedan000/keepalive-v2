# keepalive-v2

Adaptive Linux resource workload tester.

## Features

- System CPU monitoring
- Memory usage monitoring
- Network traffic statistics
- Per-machine profile generation
- Randomized task intervals
- CPU compression and hashing workload
- Network test module
- systemd service support

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main/install.sh | sudo bash
```

## Check Status

```bash
python3 /opt/keepalive-v2/keepalive.py --status
```

Status includes:

- machine profile
- CPU usage
- memory usage
- network usage
- last update time

## Service

```bash
systemctl status keepalive-v2
journalctl -u keepalive-v2 -f
```

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main/uninstall.sh | sudo bash
```
