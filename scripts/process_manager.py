"""
Process Manager - View running processes
"""
import psutil

def get_top_processes(limit=10):
    """Get top processes by CPU and memory usage"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            processes.append({
                'name': pinfo['name'],
                'cpu': pinfo['cpu_percent'],
                'memory': pinfo['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage
    processes.sort(key=lambda x: x['cpu'], reverse=True)
    return processes[:limit]

def main():
    """Display top processes"""
    processes = get_top_processes(8)
    
    print("TOP PROCESSES:\n")
    for i, proc in enumerate(processes, 1):
        print(f"{i}. {proc['name']}: CPU {proc['cpu']:.1f}%, RAM {proc['memory']:.1f}%")
    
    # System summary
    cpu_total = psutil.cpu_percent(interval=1)
    ram_total = psutil.virtual_memory().percent
    
    print(f"\nSystem: CPU {cpu_total}%, RAM {ram_total}%")

if __name__ == "__main__":
    main()
