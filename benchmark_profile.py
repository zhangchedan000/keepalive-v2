#!/usr/bin/env python3
"""Generate benchmark parameters from detected hardware."""

from hardware_profile import get_hardware_profile


def get_benchmark_profile():
    hw = get_hardware_profile()

    if hw['memory_class'] == 'large':
        memory_test_mb = 1024
    elif hw['memory_class'] == 'medium':
        memory_test_mb = 512
    else:
        memory_test_mb = 256

    return {
        'hardware': hw,
        'memory_test_mb': memory_test_mb,
        'cpu_threads': hw['cpu_cores']
    }
