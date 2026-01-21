#!/usr/bin/env python3
"""
Debug script to analyze actual log patterns and show what's being classified.
Run this to improve log_monitor.py pattern matching.
"""

import subprocess
import re
from collections import Counter

# Fetch logs
result = subprocess.run(
    ['ssh', 'root@192.168.4.141', 'ha core logs | tail -n 100'],
    capture_output=True,
    text=True,
    timeout=30
)

logs = result.stdout

print("=" * 80)
print("LOG ANALYSIS - UNCLASSIFIED ERROR PATTERNS")
print("=" * 80)

# Extract all ERROR and CRITICAL lines
error_lines = [line for line in logs.split('\n') if 'ERROR' in line or 'CRITICAL' in line]

print(f"\nTotal ERROR/CRITICAL lines: {len(error_lines)}\n")

# Group by pattern
patterns = Counter()
for line in error_lines:
    # Extract error component (in brackets)
    match = re.search(r'\[([^\]]+)\]', line)
    if match:
        component = match.group(1)
        patterns[component] += 1
    else:
        patterns['[UNBRACKETED]'] += 1

print("ERROR breakdown by component:")
for component, count in patterns.most_common():
    print(f"  {count:2d}x {component}")

print("\n" + "=" * 80)
print("ACTUAL ERROR LINES (first 15):")
print("=" * 80 + "\n")

for i, line in enumerate(error_lines[:15], 1):
    # Clean up long lines
    clean_line = line.replace('\n', ' ').replace('  ', ' ')
    if len(clean_line) > 100:
        clean_line = clean_line[:97] + "..."
    print(f"{i:2d}. {clean_line}")

print("\n" + "=" * 80)
print("SUGGESTED NEW PATTERNS:")
print("=" * 80)

# Analyze for new patterns
if any('ServiceNotFound' in line for line in error_lines):
    print("\n✓ ServiceNotFound errors (missing mobile app services)")
    print("  Pattern: re.compile(r'ServiceNotFound.*notify\\.', re.IGNORECASE)")
    print("  Severity: MEDIUM (notification service missing, non-critical)")
    print("  Type: SERVICE_NOT_FOUND")

if any('Task exception was never retrieved' in line for line in error_lines):
    print("\n✓ Async task exceptions")
    print("  Pattern: re.compile(r'Error doing job.*exception was never retrieved', re.IGNORECASE)")
    print("  Severity: LOW (caught exception, not critical)")
    print("  Type: ASYNC_EXCEPTION")

print("\n")
