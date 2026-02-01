"""
System Information Script
Displays detailed system information
"""
import platform
import psutil
from datetime import datetime

def get_size(bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def main():
    print("SYSTEM INFORMATION:\n")
    
    # System info
    print("SYSTEM:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Version: {platform.version()}")
    print(f"   Machine: {platform.machine()}")
    print(f"   Processor: {platform.processor()}")
    
    # CPU info
    print(f"\nCPU")
    print(f"   Physical Cores: {psutil.cpu_count(logical=False)}")
    print(f"   Total Cores: {psutil.cpu_count(logical=True)}")
    print(f"   Usage: {psutil.cpu_percent(interval=1)}%")
    
    # Memory info
    memory = psutil.virtual_memory()
    print(f"\nMEMORY")
    print(f"   Total: {get_size(memory.total)}")
    print(f"   Available: {get_size(memory.available)}")
    print(f"   Used: {get_size(memory.used)} ({memory.percent}%)")
    
    # Disk info
    disk = psutil.disk_usage('/')
    print(f"\nDISK (C:)")
    print(f"   Total: {get_size(disk.total)}")
    print(f"   Used: {get_size(disk.used)} ({disk.percent}%)")
    print(f"   Free: {get_size(disk.free)}")
    
    # Battery info (if available)
    battery = psutil.sensors_battery()
    if battery:
        print(f"\nBATTERY")
        print(f"   Charge: {battery.percent}%")
        print(f"   Plugged In: {'Yes' if battery.power_plugged else 'No'}")
        if not battery.power_plugged and battery.secsleft != -1:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            print(f"   Time Remaining: {hours}h {minutes}m")
    
    # Boot time
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    print(f"\nUPTIME")
    print(f"   Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    uptime = datetime.now() - boot_time
    print(f"   Uptime: {uptime.days} days, {uptime.seconds // 3600} hours")

if __name__ == "__main__":
    main()
