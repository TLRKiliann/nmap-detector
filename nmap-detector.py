#!/usr/bin/env python3

'''
####################################
#                                  #
#        nmap-detector v1.0        #
#                                  #
####################################
'''

import sys
import warnings
from scapy.all import sniff, IP, TCP, conf
from collections import defaultdict
from datetime import datetime
import time

# Especially for MacOS
conf.debug_dissector = False  # Deactivate debug
warnings.filterwarnings("ignore")  # Ignore warnings
sys.setrecursionlimit(10000)  # Iterative limit increase

class PortScanDetector:
    def __init__(self):
        self.scan_patterns = {
            'rapide': 5,
            'modere': 10,
            'lent': 30,
        }
        self.history = defaultdict(list)
        self.last_alert = defaultdict(float)
        
    def packet_callback(self, packet):
        if not packet.haslayer(IP) or not packet.haslayer(TCP):
            return
        
        flags = packet[TCP].flags
        # Verify flags
        syn = (flags & 0x02) != 0  # Bit SYN
        ack = (flags & 0x10) != 0  # Bit ACK
        
        if not syn or ack:
            return
        
        src = packet[IP].src
        port = packet[TCP].dport
        now = time.time()
        
        # To avoid error of type
        window = 30  # seconds
        self.history[src] = [
            (float(ts), int(p)) for ts, p in self.history[src] 
            if float(now) - float(ts) < float(window)
        ]
        
        self.history[src].append((float(now), int(port)))
        
        print(f"[*] SYN from {src} to port {port} (total: {len(self.history[src])})")
        
        for scan_type, threshold in self.scan_patterns.items():
            if len(self.history[src]) >= threshold:
                if now - self.last_alert[src] > 30:
                    self.last_alert[src] = now
                    print(f"\n🚨 SCAN {scan_type.upper()} detected of {src}")
                    print(f"   {len(self.history[src])} SYN recieved")
                    print(f"   Last port: {port}\n")
                    break

def main():
    print("=== Nmap Detector v1.0 ===")
    detector = PortScanDetector()
    
    try:
        # Linux
        sniff(iface="lo", prn=detector.packet_callback, store=0)  # loopback
        #sniff(iface="eth0", prn=detector.packet_callback, store=0)  # Ethernet
        #sniff(iface="wlan0", prn=detector.packet_callback, store=0) # WiFi
        # MacOS
        #sniff(iface="lo0", prn=detector.packet_callback, store=0) # loopback
        #sniff(iface="en0", prn=detector.packet_callback, store=0) # Ethernet
        #sniff(iface="en1", prn=detector.packet_callback, store=0) # Wifi
        # Windows
        #sniff(iface="Ethernet", prn=detector.package_callback, store=0) # Ethernet
    except Exception as e:
        print(f"Erreur: {e}")
        print("Try: sudo python3 nmap-detector.py")

if __name__ == "__main__":
    main()