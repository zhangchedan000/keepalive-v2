#!/usr/bin/env python3
"""Runtime heartbeat helper for keepalive-v2."""

import time
from datetime import datetime
from pathlib import Path

STATE = Path('/var/lib/keepalive-v2')
HEARTBEAT = STATE / 'heartbeat.json'


def write_heartbeat(extra=None):
    STATE.mkdir(parents=True, exist_ok=True)
    data = {
        'heartbeat': datetime.now().isoformat(),
        'timestamp': time.time()
    }
    if extra:
        data.update(extra)
    HEARTBEAT.write_text(__import__('json').dumps(data, indent=2))


def read_heartbeat():
    if HEARTBEAT.exists():
        return __import__('json').loads(HEARTBEAT.read_text())
    return {}
