# keepalive-v2

Adaptive Linux resource workload tester.

Features:
- Reads current system CPU, memory and network usage
- Adds configurable test workload when needed
- Per-machine local profile generation
- CPU, memory and network test modules
- systemd service support

Install:

```bash
curl -fsSL https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main/install.sh | sudo bash
```

Status:

```bash
python3 /opt/keepalive-v2/keepalive.py --status
```

Uninstall:

```bash
curl -fsSL https://raw.githubusercontent.com/zhangchedan000/keepalive-v2/main/uninstall.sh | sudo bash
```
