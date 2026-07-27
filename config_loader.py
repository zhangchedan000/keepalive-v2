#!/usr/bin/env python3
"""Configuration helper for keepalive-v2."""

import json
from pathlib import Path

CONFIG_PATH = Path('/etc/keepalive-v2/config.json')

DEFAULT = {
    'cpu_target': 20,
    'memory_target': 25,
    'network_test': True,
    'log': True,
    'cycle_days': 7,
}


def load_config():
    cfg = dict(DEFAULT)
    try:
        if CONFIG_PATH.exists():
            cfg.update(json.loads(CONFIG_PATH.read_text()))
    except Exception:
        pass
    return cfg
