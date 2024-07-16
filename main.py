import os
import platform
import psutil
import socket
import subprocess
import GPUtil
from colorama import Fore, Style, init

def get_cpu_info():
    cpu_info = "Unknown"
    try:
        if platform.system() == "Windows":
            import wmi
            w = wmi.WMI()
            for cpu in w.Win32_Processor():
                cpu_info = cpu.Name
        elif platform.system() == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        cpu_info = line.strip().split(":")[1]
                        break
        elif platform.system() == "Darwin":
            command = "sysctl -n machdep.cpu.brand_string"
            cpu_info = subprocess.check_output(command, shell=True).strip().decode()
    except Exception as e:
        cpu_info = str(e)
    return cpu_info

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = "Unknown"
    if gpus:
        gpu_info = gpus[0].name
    return gpu_info

def get_system_info():
    info = {}

    # Network Information
    hostname = socket.gethostname()
    info['Hostname'] = hostname
    info['IP Address'] = socket.gethostbyname(hostname)

    # Operating System Information
    info['OS'] = platform.system()
    info['OS Version'] = platform.version()

    # CPU Information
    info['CPU'] = get_cpu_info()
    info['CPU Arch'] = platform.architecture()[0]
    info['CPU Cores'] = psutil.cpu_count(logical=True)
    info['CPU Speed'] = f"{psutil.cpu_freq().current:.2f} MHz"

    # GPU Information
    info['GPU'] = get_gpu_info()

    # Memory Information
    mem = psutil.virtual_memory()
    info['Total RAM'] = f"{round(mem.total / (1024**3))} GB"
    info['Used RAM'] = f"{round(mem.used / (1024**3))} GB"

    # Disk Information
    disk_usage = psutil.disk_usage('/')
    info['Disk Total'] = f"{round(disk_usage.total / (1024**3))} GB"
    info['Disk Used'] = f"{round(disk_usage.used / (1024**3))} GB"
    info['Disk Free'] = f"{round(disk_usage.free / (1024**3))} GB"

    # Shell
    info['Shell'] = os.environ.get('SHELL', 'Unknown')

    # Python Version
    info['Python Version'] = platform.python_version()

    return info

def display_system_info(info):
    init(autoreset=True)
    print(Fore.CYAN + "System Information")
    print(Fore.CYAN + "==================")
    keys_order = [
        'Hostname', 'IP Address', 'OS', 'OS Version', 'CPU', 'CPU Arch', 'CPU Cores', 
        'CPU Speed', 'GPU', 'Total RAM', 'Used RAM', 'Disk Total', 'Disk Used', 
        'Disk Free', 'Shell', 'Python Version'
    ]
    for key in keys_order:
        if key in info:
            value = info[key]
            if isinstance(value, list):
                print(Fore.YELLOW + f"{key}:")
                for item in value:
                    print(Fore.GREEN + f"  - {item}")
            else:
                print(Fore.YELLOW + f"{key}: {Fore.GREEN + str(value)}")

if __name__ == "__main__":
    system_info = get_system_info()
    display_system_info(system_info)