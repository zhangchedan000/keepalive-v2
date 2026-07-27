#!/usr/bin/env python3
"""Hardware profile helper for benchmark-style workloads."""

import os


def get_total_memory_mb():
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                if line.startswith('MemTotal'):
                    return int(line.split()[1]) // 1024
    except Exception:
        return 0


def get_hardware_profile():
    cores = os.cpu_count() or 1
    memory_mb = get_total_memory_mb()

    if memory_mb >= 16384:
        memory_class = 'large'
    elif memory_mb >= 8192:
        memory_class = 'medium'
    else:
        memory_class = 'small'

    return {
        'cpu_cores': cores,
        'memory_mb': memory_mb,
        'memory_class': memory_class,
    }
