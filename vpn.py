"""
    Ernar Kusdavletov, 2018
    Pick server and start connection with VPNGate (http://www.vpngate.net/en/)
"""

import requests
import subprocess
import base64
import time
import argparse


def vpn(country):
    try:
        vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r', '')
        serv = [line.split(',') for line in vpn_data.split('\n')]
        labels = serv[1]
        labels[0] = labels[0][1:]
        serv = [s for s in serv[2:] if len(s) > 1]
    except:
        print('Cannot get VPN servers data')
        exit(1)
    i = 5
    desired = [s for s in serv if (country.lower() in s[i].lower())]
    found = len(desired)
    print('Found ' + str(found) + ' servers for country ' + str(country))
    if found == 0:
        exit(1)
    supported = [s for s in desired if len(s[-1]) > 0]
    print(str(len(supported)) + ' of these servers support OpenVPN')
    # We pick the best servers by score
    winner = sorted(supported, key=lambda s: float(s[2].replace(',','.')), reverse=True)[0]
    print("\n== Best server ==")
    pairs = list(zip(labels, winner))[:-1]
    for (l, d) in pairs[:4]:
        print(l + ': ' + d)
    print(pairs[4][0] + ': ' + str(float(pairs[4][1]) / 10**6) + ' MBps')
    print("Country: " + pairs[5][1])
    print("\nLaunching VPN...")
    path = "C:\Program Files\OpenVPN\config\\temp.ovpn"
    f = open(path, 'wb')
    f.write(base64.b64decode(winner[-1]))
    f.close()
    x = subprocess.Popen(['openvpn-gui', '--connect', 'temp.ovpn'])
    try:
        # termination with Ctrl+C
        while True:
            time.sleep(600)
    except:
        x.kill()
        print('\nVPN terminated')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("country")
    args = parser.parse_args()
    vpn(country=args.country)
