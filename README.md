<div align="center">
  
# ⚡ nmap-detector v1.0

*Network scanning tool*

[![Stars](https://img.shields.io/github/stars/TLRKiliann/my-appy?style=social)](https://github.com/TLRKiliann/my-appy/stargazers)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/TLRKiliann/my-appy)](https://github.com/TLRKiliann/my-appy)

</div>

Detection of nmap intrusion attempts.

```
-T0 (Paranoid)      → More stealthy, but impractical on large targets
-T1 (Sneaky)        → Very stealthy, usable in real-world conditions
-T2 (Polite)        → Moderately stealthy
-T3 (Normal)        → Default behavior, detectable on sensitive networks
-T4 (Aggressive)    → Easily detectable
-T5 (Insane)        → Extremely detectable, packet loss possible
```

## Installation

`git clone ...`

**Activate**

`source my-appy/venv/bin/activate`

**Go to my-appy**

`cd my-appy`

`pip install scapy`


**Selective update**

`pip install --upgrade scapy pip freeze > requirements.txt`


**Update all versions**

`pip install -r requirements.txt`


**Update to the latest compatible versions**

`pip install --upgrade -r requirements.txt`


## Run app

:warning: It's not possible to read detection with firewall !

**Terminal n°1**

`sudo nmap -sS -p 1-6000 -T3 127.0.0.1`

**Terminal n°2**

`sudo python3 nmap-detector.py`

You can change choose the right sniff():

```
    try:
        # MacOS
        sniff(iface="lo0", prn=detector.packet_callback, store=0)
        #sniff(iface="en1", prn=detector.packet_callback, store=0)
        # Linux
        #sniff(iface="lo", prn=detector.packet_callback, store=0)  # loopback
        #sniff(iface="eth0", prn=detector.packet_callback, store=0)  # Ethernet
        #sniff(iface="wlan0", prn=detector.packet_callback, store=0) # WiFi
    except Exception as e:
        print(f"Erreur: {e}")
        print("Essayez: sudo python3 script.py")
```

## nmap security

- :-1: Don't use

`nmap -sS -p- -T4 (or T5) <IP>`


- :+1: A more discreet option (but very slow)

`nmap -sS -p- -T2 <IP>`      # Polite mode

`nmap -sS -p- -T1 <IP>`      # Sneaky mode (more slowly)


- :timer_clock: Final deadline check

`nmap -sS -p- --scan-delay 500ms --max-rtt-timeout 1500ms <IP>`


- :fairy: Use port 80 (HTTP) as the source port—less conspicuous

`nmap -sS -p- --source-port 80 <IP>`


- :ballot_box_with_check: Maximum stealth: slow + shards + decoys + source port

`nmap -sS -p- -T2 -f -D RND:10 --source-port 80 --scan-delay 1s <IP>`

--scan-delay 1s

-D RND:10 

One-second delay => too long (24–36 hours)

Nmap randomly generates 10 IP addresses

One of these 10 will be your real IP address

The other 9 are random IP addresses that may or may not exist (Nmap does not verify them)

Warning: These decoy IPs will also receive responses from the target (side effect)

- :white_check_mark: Maximum discretion without generating invalid IP addresses

`nmap -sS -p- -T1 -f --scan-delay 2s --data-length 200 <IP>`

```
# Discretion + reasonable time (for a monitored network)
nmap -sS -p- -T2 --max-retries 1 --min-rate 10 <IP>
# --min-rate 10 = at least 10 packets per second (much faster but quiet)
```

Enjoy :koala: !