#!/usr/bin/env python3

'''
from scapy.all import sniff, IP, TCP
from collections import defaultdict
from datetime import datetime
import time
'''

import sys
import warnings
from scapy.all import sniff, IP, TCP, conf
from collections import defaultdict
from datetime import datetime
import time

# 🔥 CORRECTIONS POUR macOS
conf.debug_dissector = False  # Désactiver le debug
warnings.filterwarnings("ignore")  # Ignorer les warnings
sys.setrecursionlimit(10000)  # Augmenter limite récursion

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
        # Vérification robuste des flags
        syn = (flags & 0x02) != 0  # Bit SYN
        ack = (flags & 0x10) != 0  # Bit ACK
        
        if not syn or ack:
            return
        
        src = packet[IP].src
        port = packet[TCP].dport
        now = time.time()
        
        # Conversion explicite pour éviter les erreurs de type
        window = 30  # secondes
        self.history[src] = [
            (float(ts), int(p)) for ts, p in self.history[src] 
            if float(now) - float(ts) < float(window)
        ]
        
        self.history[src].append((float(now), int(port)))
        
        print(f"[*] SYN de {src} vers port {port} (total: {len(self.history[src])})")
        
        # Vérification seuil
        for scan_type, threshold in self.scan_patterns.items():
            if len(self.history[src]) >= threshold:
                if now - self.last_alert[src] > 30:
                    self.last_alert[src] = now
                    print(f"\n🚨 SCAN {scan_type.upper()} détecté depuis {src}")
                    print(f"   {len(self.history[src])} SYN reçus")
                    print(f"   Dernier port: {port}\n")
                    break

def main():
    print("=== DÉTECTEUR Nmap -sS (macOS) ===")
    detector = PortScanDetector()
    
    try:
        # Sur macOS, spécifier l'interface est crucial
        sniff(iface="lo0", prn=detector.packet_callback, store=0)
        #sniff(iface="en1", prn=detector.packet_callback, store=0)
        # Sur Linux
        #sniff(iface="lo", prn=detector.packet_callback, store=0)  # loopback
        #sniff(iface="eth0", prn=detector.packet_callback, store=0)  # Ethernet
        #sniff(iface="wlan0", prn=detector.packet_callback, store=0) # WiFi
    except Exception as e:
        print(f"Erreur: {e}")
        print("Essayez: sudo python3 script.py")

if __name__ == "__main__":
    main()