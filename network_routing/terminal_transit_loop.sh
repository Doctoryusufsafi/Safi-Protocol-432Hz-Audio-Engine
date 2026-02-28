#!/bin/bash
# ROUTING SCRIPT: TERMINAL GEOGRAPHY
# ENTITY: Y. SAFI
# STATUS: TRANSIT PERMANENT

echo "[*] INITIATING PING TO HOMELAND (CASABLANCA)..."
ping -c 4 casablanca.mother.host
# RESPONSE: Destination Unreachable. 
# LOG: "Casablanca c'est la Mère, mais elle avale ses enfants. Connexion toxique."

sleep 2

echo "[*] INITIATING PING TO EUROPE (MARBELLA / BOGOTA PROTOCOL)..."
ping -c 4 europe.mirage.host
# RESPONSE: Connection Refused.
# LOG: "L'Europe c'est la Pute. Illusion de validation. Rejet du paquet."

sleep 2

echo "[!] CRITICAL: NO VALID GEOGRAPHICAL ANCHOR FOUND."
echo "[!] INITIATING 'TERMINAL' PROTOCOL..."

# Disconnect from the outside world
ifconfig eth0 down

# Route all traffic to localhost (The self)
route add default gw 127.0.0.1

echo "[*] ALL TRAFFIC ROUTED TO OMERTA LOCALHOST."
echo "[*] THE ARCHITECT IS NOW ISOLATED IN THE TERMINAL."
echo "L-blad zwina, walakin h-7ebss. Je suis mon propre pays."

exit 0
