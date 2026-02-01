"""
Network Information Scanner
Display network status and information
"""
import socket
import psutil
import requests

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unknown"

def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return "Unable to fetch"

def get_network_interfaces():
    """Get network interface information"""
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    
    return interfaces, stats

def format_bytes(bytes):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def main():
    print("NETWORK INFORMATION:\n")
    
    # IP Addresses
    print("IP ADDRESSES:")
    print(f"   Local IP: {get_local_ip()}")
    print(f"   Public IP: {get_public_ip()}")
    print(f"   Hostname: {socket.gethostname()}")
    
    # Network interfaces
    interfaces, stats = get_network_interfaces()
    print("\nNETWORK INTERFACES")
    
    for interface_name, addresses in interfaces.items():
        if interface_name in stats:
            stat = stats[interface_name]
            status = "Up" if stat.isup else "Down"
            print(f"\n   {interface_name} ({status})")
            print(f"   Speed: {stat.speed} Mbps" if stat.speed > 0 else "   Speed: Unknown")
            
            for addr in addresses:
                if addr.family == socket.AF_INET:
                    print(f"   IPv4: {addr.address}")
                elif addr.family == socket.AF_INET6:
                    print(f"   IPv6: {addr.address}")
    
    # Network usage
    net_io = psutil.net_io_counters()
    print("\nNETWORK USAGE")
    print(f"   Bytes Sent: {format_bytes(net_io.bytes_sent)}")
    print(f"   Bytes Received: {format_bytes(net_io.bytes_recv)}")
    print(f"   Packets Sent: {net_io.packets_sent:,}")
    print(f"   Packets Received: {net_io.packets_recv:,}")
    
    # Active connections
    connections = psutil.net_connections()
    active_connections = [c for c in connections if c.status == 'ESTABLISHED']
    print(f"\nACTIVE CONNECTIONS")
    print(f"   Total: {len(connections)}")
    print(f"   Established: {len(active_connections)}")

if __name__ == "__main__":
    main()
