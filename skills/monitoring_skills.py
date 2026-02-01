"""
System Monitoring Skills - CPU, RAM, GPU, Temperature monitoring

Provides real-time system performance monitoring capabilities.
"""

import psutil
import platform
from datetime import datetime
from typing import Dict
from skills import BaseSkill


class MonitoringSkills(BaseSkill):
    """System performance monitoring."""
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        monitoring_intents = [
            'check_system',
            'system_status',
            'cpu_usage',
            'memory_usage',
            'disk_usage',
            'battery_status',
            'network_status',
            'kill_process'
        ]
        return intent in monitoring_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute monitoring commands."""
        try:
            if intent == 'check_system':
                return self._get_system_overview()
            elif intent == 'cpu_usage':
                return self._get_cpu_info()
            elif intent == 'memory_usage':
                return self._get_memory_info()
            elif intent == 'disk_usage':
                return self._get_disk_info()
            elif intent == 'battery_status':
                return self._get_battery_info()
            elif intent == 'network_status':
                return self._get_network_info()
            elif intent == 'kill_process':
                return self._kill_process(entities.get('process_name', ''))
            else:
                return self._get_system_overview()
        except Exception as e:
            self.logger.error(f"Monitoring error: {e}")
            return f"Error getting system information: {str(e)}"
    
    def _get_system_overview(self) -> str:
        """Get complete system overview."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get temperatures if available
        temps = ""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temp_info = psutil.sensors_temperatures()
                if temp_info:
                    temps = f"\nCPU Temperature: {temp_info.get('coretemp', [{}])[0].current}°C"
        except:
            pass
        
        return (
            f"System Status:\n"
            f"CPU Usage: {cpu_percent}%\n"
            f"RAM: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)\n"
            f"Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB){temps}"
        )
    
    def _get_cpu_info(self) -> str:
        """Get detailed CPU information."""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        
        avg_cpu = sum(cpu_percent) / len(cpu_percent)
        
        result = f"CPU Information:\n"
        result += f"Cores: {cpu_count}\n"
        result += f"Average Usage: {avg_cpu:.1f}%\n"
        
        if cpu_freq:
            result += f"Frequency: {cpu_freq.current:.0f} MHz\n"
        
        # Show per-core usage
        for i, percent in enumerate(cpu_percent[:8]):  # Show first 8 cores
            result += f"Core {i}: {percent}%\n"
        
        return result
    
    def _get_memory_info(self) -> str:
        """Get detailed memory information."""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return (
            f"Memory Information:\n"
            f"Total RAM: {memory.total // (1024**3)}GB\n"
            f"Available: {memory.available // (1024**3)}GB\n"
            f"Used: {memory.used // (1024**3)}GB ({memory.percent}%)\n"
            f"Swap: {swap.used // (1024**3)}GB / {swap.total // (1024**3)}GB ({swap.percent}%)"
        )
    
    def _get_disk_info(self) -> str:
        """Get disk usage information."""
        partitions = psutil.disk_partitions()
        result = "Disk Information:\n"
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                result += (
                    f"\n{partition.device} ({partition.mountpoint}):\n"
                    f"  Total: {usage.total // (1024**3)}GB\n"
                    f"  Used: {usage.used // (1024**3)}GB ({usage.percent}%)\n"
                    f"  Free: {usage.free // (1024**3)}GB\n"
                )
            except PermissionError:
                continue
        
        return result
    
    def _get_battery_info(self) -> str:
        """Get battery status."""
        if not hasattr(psutil, "sensors_battery"):
            return "Battery information not available on this system."
        
        battery = psutil.sensors_battery()
        if battery is None:
            return "No battery detected. System is plugged in."
        
        status = "charging" if battery.power_plugged else "discharging"
        time_left = battery.secsleft
        
        result = f"Battery Status:\n"
        result += f"Charge: {battery.percent}%\n"
        result += f"Status: {status}\n"
        
        if time_left != psutil.POWER_TIME_UNLIMITED and time_left != psutil.POWER_TIME_UNKNOWN:
            hours = time_left // 3600
            minutes = (time_left % 3600) // 60
            result += f"Time remaining: {hours}h {minutes}m"
        
        return result
    
    def _get_network_info(self) -> str:
        """Get network information."""
        net_io = psutil.net_io_counters()
        
        sent_mb = net_io.bytes_sent / (1024**2)
        recv_mb = net_io.bytes_recv / (1024**2)
        
        return (
            f"Network Information:\n"
            f"Data Sent: {sent_mb:.1f} MB\n"
            f"Data Received: {recv_mb:.1f} MB\n"
            f"Packets Sent: {net_io.packets_sent}\n"
            f"Packets Received: {net_io.packets_recv}"
        )
    
    def _kill_process(self, process_name: str) -> str:
        """Kill a process by name."""
        if not process_name:
            return "Please specify a process name to kill."
        
        killed = []
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if killed:
            return f"Killed processes: {', '.join(killed)}"
        else:
            return f"No process found matching '{process_name}'"
