import socket
import threading
import argparse

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"[+] Port {port} is open")
        sock.close()
    except:
        pass

def main(ip, ports):
    print(f"[*] Scanning {ip}...")
    for port in ports:
        t = threading.Thread(target=scan_port, args=(ip, port))
        t.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("ip", help="Target IP address or domain")
    parser.add_argument("-p", "--ports", help="Comma-separated ports (e.g. 22,80,443)", default="20-1024")
    args = parser.parse_args()

    ip = args.ip
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = list(range(start, end + 1))
    else:
        ports = [int(p.strip()) for p in args.ports.split(",")]

    main(ip, ports)
