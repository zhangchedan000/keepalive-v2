# keepalive-v2

Adaptive Linux resource workload tester.

Version: 2.0.0

## Features

- System CPU monitoring
- Memory usage monitoring
- Network traffic statistics
- Local profile generation
- Configurable test parameters
- CPU compression and hashing benchmark module
- Network test module
- systemd service support
- Runtime logs and status files

## Configuration

Default configuration location:

```text
/etc/keepalive-v2/config.json
```

Example:

```json
{
  "cpu_target": 20,
  "memory_target": 25,
  "network_test": true,
  "log": true,
  "cycle_days": 7
}
```

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main/install.sh | sudo bash
```

## Check Status

```bash
python3 /opt/keepalive-v2/keepalive.py --status
```

## Service

```bash
systemctl status keepalive-v2
journalctl -u keepalive-v2 -f
```

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main/uninstall.sh | sudo bash
```
