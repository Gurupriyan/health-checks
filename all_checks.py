import os
import shutil
import sys
import socket
import psutil


def check_reboot():
    """Returns True if the computer has a pending reboot"""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    """Returns True if there isn't enough space on disk, False otherwise"""
    du = shutil.disk_usage(disk)
    #Calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    gigabytes_free = du.free / 2**30

    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False

def check_root_full():
    """Returns true if the root partition is full, false otherwise"""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_no_network():
    """Returns True if it fails to resolve Google's URL, false otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def check_cpu_constrained():
    """Returns True if the cpu is having too much usage, false otherwise"""
    return psutil.cpu_percent(1) > 75


def main():
    checks = [
        (check_reboot, "Pending reboot."),
        (check_root_full, "Root Partition disk space critically low."),
        (check_no_network, "No working network."),
        (check_cpu_constrained, "CPU load too high.")
    ]

    everything_ok = True

    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False

    if not everything_ok:
        sys.exit(1)


    print("Everything is ok")
    sys.exit(0)

main()