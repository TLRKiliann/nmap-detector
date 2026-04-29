┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                 ┃
┃    ⚡  nmap-detector  v1.0      ┃
┃                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

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

**Activer**

`source my-appy/venv/bin/activate`

**Se rendre dedans my-appy**

`cd my-appy`

`pip install scapy`


**MAJ sélective**

`pip install --upgrade scapy pip freeze > requirements.txt`


**Update all versions**

`pip install -r requirements.txt`


**Update to the latest compatible versions**

`pip install --upgrade -r requirements.txt`


## Run app

:warning: It's not possible to read detection wit firewall !

**Terminal n°1**

`sudo nmap -sS -p 1-6000 -T3 127.0.0.1`

**Terminal n°2**

`sudo python3 nmap-detector.py`

You can change choose the right sniff():

```
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
```

## nmap security

- :-1: Option plus discrète (mais très lente)

`nmap -sS -p- -T2 <IP>`      # Polite mode

`nmap -sS -p- -T1 <IP>`      # Sneaky mode (encore plus lent)


- :timer_clock: Contrôle fin du délai

`nmap -sS -p- --scan-delay 500ms --max-rtt-timeout 1500ms <IP>`


- :fairy: Utilise le port 80 (HTTP) comme port source - plus anodin

`nmap -sS -p- --source-port 80 <IP>`


- :ballot_box_with_check: Discrétion maximale : lent + fragments + leurres + port source

`nmap -sS -p- -T2 -f -D RND:10 --source-port 80 --scan-delay 1s <IP>`

--scan-delay 1s

-D RND:10 

Delay d'une seconde => trop long (24-36 heures)

Nmap génère aléatoirement 10 adresses IP

Parmi ces 10, l'une d'elles sera votre vraie IP

Les 9 autres sont des IPs aléatoires qui existent probablement (ou pas - Nmap ne vérifie pas)

Attention : Ces IPs leurres recevront aussi les réponses de la cible (effet de bord)


- :white_check_mark: Discrétion maximale sans générer d'IPs invalides :

`nmap -sS -p- -T1 -f --scan-delay 2s --data-length 200 <IP>`

```
# Discrétion + temps raisonnable (pour un réseau surveillé)
nmap -sS -p- -T2 --max-retries 1 --min-rate 10 <IP>
# --min-rate 10 = minimum 10 paquets/seconde (bien plus rapide mais discret)
```

Enjoy :koala: !