import socket
import argparse
import csv
from datetime import datetime
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

BANNER = r"""
 ____            _   ____                                  
|  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
| |_) / _ \| '__| __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
|  __/ (_) | |  | |_ ___) | (_| (_| | | | | | | |  __/ |   
|_|   \___/|_|   \__|____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                          
"""

print(Fore.CYAN + Style.BRIGHT + BANNER)

parser = argparse.ArgumentParser(description="⚡ Advanced Multi-threaded Port Scanner ⚡")
parser.add_argument("host", help="Target IP or hostname")
parser.add_argument("-p", "--ports", help="Port range (e.g. 20-80)", required=True)
parser.add_argument("-t", "--threads", help="Number of threads", type=int, default=100)

args = parser.parse_args()

host = args.host
start_port, end_port = map(int, args.ports.split('-'))
ip = socket.gethostbyname(host)
num_threads = args.threads

results = []

print(Fore.YELLOW + f"[*] Scanning {host} ({ip}) from port {start_port} to {end_port} with {num_threads} threads...\n")

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "N/A"
            service = {
                22: "SSH", 80: "HTTP", 443: "HTTPS",
                21: "FTP", 25: "SMTP", 3306: "MySQL",
                3389: "RDP"
            }.get(port, "Unknown")
            return {
                "IP": ip,
                "Port": port,
                "Status": "Open",
                "Service": service,
                "Banner": banner
            }
        s.close()
    except Exception:
        pass
    return None

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(scan_port, port) for port in range(start_port, end_port + 1)]
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(Fore.GREEN + f"[+] Port {result['Port']} is open")
            print(Fore.MAGENTA + f"    ↳ Service: {result['Service']}")
            print(Fore.CYAN + f"    ↳ Banner: {result['Banner']}")
            results.append(result)

from datetime import datetime
import os

# Generate timestamp in clear date-time format
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
safe_ip = ip.replace('.', '_')
home_dir = os.path.expanduser("~")

# CSV file
csv_file = os.path.join(home_dir, f"scan_results_{safe_ip}_{timestamp}.csv")
with open(csv_file, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["IP", "Port", "Status", "Service", "Banner"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

# TXT file
txt_file = os.path.join(home_dir, f"scan_results_{safe_ip}_{timestamp}.txt")
with open(txt_file, mode='w') as f:
    f.write(f"Scan Report for {host} ({ip}) - {datetime.now()}\n")
    f.write("="*60 + "\n")
    for row in results:
        f.write(f"Port {row['Port']} is open\n")
        f.write(f"    ↳ Service: {row['Service']}\n")
        f.write(f"    ↳ Banner: {row['Banner']}\n")
        f.write("-"*50 + "\n")

print(Fore.YELLOW + f"\n✔ Scan complete! Results saved in your Home Directory as:")
print(Fore.GREEN + f"   ➤ {csv_file}")
print(Fore.GREEN + f"   ➤ {txt_file}")
