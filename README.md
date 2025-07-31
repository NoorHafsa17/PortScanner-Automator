# PortScanner-Automator 🔎

A basic Python script to scan open ports on a target IP address or domain using multi-threading.

## Features
- Scan specific ports or a range
- Fast and lightweight using `threading`
- Easily extendable (e.g., add Nmap or banner grabbing)

## Usage

```bash
python3 port_scanner.py <target-ip> -p 22,80,443
