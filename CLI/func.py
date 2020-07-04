import psutil
import platform

from datetime import datetime

def get_size(bytes, suffix = "B"):

    factor = 1024

    for unit in ["", "K", "M", "G", "T", "P"]:

        if bytes < factor:

            return f"{bytes:.2f}{unit}{suffix}"

        bytes /= factor

def system():

  uname = platform.uname()

  cpufreq = psutil.cpu_freq()

  disk_io = psutil.disk_io_counters()

  svmem = psutil.virtual_memory()

  boot_time_timestamp = psutil.boot_time()

  if_addrs = psutil.net_if_addrs()

  bt = datetime.fromtimestamp(boot_time_timestamp)

  partitions = psutil.disk_partitions()

  swap = psutil.swap_memory()

  net_io = psutil.net_io_counters()

  per_core = ""
  
  for i, percentage in enumerate(psutil.cpu_percent(percpu = True, interval = 1)):

      per_core += f"Core {i + 1}: {percentage}%\n"

  parts = ""

  for partition in partitions:

    parts += f"Device: {partition.device}\n"
    parts += f"  Mountpoint: {partition.mountpoint}\n"
    parts += f"  File system type: {partition.fstype}\n"

    try:

      partition_usage = psutil.disk_usage(partition.mountpoint)
    
    except PermissionError:

      continue

    parts += f"  Total Size: {get_size(partition_usage.total)}\n"
    parts += f"  Used: {get_size(partition_usage.used)}\n"
    parts += f"  Free: {get_size(partition_usage.free)}\n"
    parts += f"  Percentage: {partition_usage.percent}%\n"

  net_interfaces = ""

  for interface_name, interface_addresses in if_addrs.items():

    for address in interface_addresses:

      net_interfaces += f"=== Interface: {interface_name} ===\n"

      if str(address.family) == "AddressFamily.AF_INET":

        net_interfaces += f"  IP Address: {address.address}\n"
        net_interfaces += f"  Netmask: {address.netmask}\n"
        net_interfaces += f"  Broadcast IP: {address.broadcast}\n"

      elif str(address.family) == "AddressFamily.AF_PACKET":

        net_interfaces += f"  MAC Address: {address.address}\n"
        net_interfaces += f"  Netmask: {address.netmask}\n"
        net_interfaces += f"  Broadcast MAC: {address.broadcast}\n"

  info = f"""
================ SYSTEM INFO ================
System: {uname.system}
Node Name: {uname.node}
Release: {uname.release}
Version: {uname.version}
Machine: {uname.machine}
Processor: {uname.processor}

Boot Time: {bt.month}/{bt.day}/{bt.year} {bt.hour}:{bt.minute}:{bt.second}

==== PROCESSOR INFO ====

Physical cores: {psutil.cpu_count(logical = False)}
Total cores: {psutil.cpu_count(logical = True)}

Max Frequency: {cpufreq.max:.2f}Mhz
Min Frequency: {cpufreq.min:.2f}Mhz
Current Frequency: {cpufreq.current:.2f}Mhz

CPU Usage Per Core:
{per_core}

Total CPU Usage: {psutil.cpu_percent()}%

==== MEMORY INFO ====

Total Memory: {get_size(svmem.total)}
Available Memory: {get_size(svmem.available)}
Used Memory: {get_size(svmem.used)}
Memory Percentage: {svmem.percent}%

SWAP Total: {get_size(swap.total)}
SWAP Free: {get_size(swap.free)}
SWAP Used: {get_size(swap.used)}
SWAP Percentage: {swap.percent}%

==== PARTITIONS INFO ==== 

{parts}
Total disk read: {get_size(disk_io.read_bytes)}
Total disk write: {get_size(disk_io.write_bytes)}

==== NETWORK INFO ====

{net_interfaces}
Total Bytes Sent: {get_size(net_io.bytes_sent)}
Total Bytes Received: {get_size(net_io.bytes_recv)}
"""

  print(info)

def help(config):

  version = config["version"]

  info = f"""
================ HELP ================
ZealousOS v{version} - Listing Commands

COMMAND     |     ALIASES
            |
help        |     info
system      |     sys, sys-stats
clear       |     cls
license     |     
echo        |     print, write
reboot      |     rbt
logout      |     lgt
server      |     sv
package     |     pkg
tree        |     list
"""

  print(info)

def license():

  info = """
Copyright 2020-20xx; ZealousOS Team

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

  print(info)