#!/usr/bin/env python3

import pyshark
import argparse
import os,subprocess

parser = argparse.ArgumentParser(
    description="CDP analyze"
)

parser.add_argument(
    '-f',
    dest="FILE",
    type=str,
    help="The infile"
)

parser.add_argument(
    '-v',
    action='store_true',
    help="Verbose mode. Shows all attributes"
)

args = parser.parse_args()


cap = pyshark.FileCapture(args.FILE, display_filter="cdp")
i = 1



if args.v:

    for pkt in cap:
        print("\033[1;34m[*]\033[0m Paket " + str(i) + " :")
        print("")
        print(pkt.cdp)
        print("")
        print("")
        print("")
        i += 1

else:
    
    for pkt in cap:
        print("\033[1;34m[*]\033[0m Paket " + str(i) + " :")
        print("")
    
        if "deviceid" in str(pkt.cdp.field_names):
            print("Device ID: " + pkt.cdp.deviceid)
    
        if "software_version" in str(pkt.cdp.field_names):
            print("Software Version: " + pkt.cdp.software_version)

        if "platform" in str(pkt.cdp.field_names):
    	    print("Platform: " + pkt.cdp.platform)

        if "nrgyz_ip_address" in str(pkt.cdp.field_names):
            print("IP-Address: " + pkt.cdp.nrgyz_ip_address)

        if "portid" in str(pkt.cdp.field_names):
            print("Port ID: " + pkt.cdp.portid)

        if "cluster_switch_mac" in str(pkt.cdp.field_names):
            print("Switch MAC: " + pkt.cdp.cluster_switch_mac)

        if "cluster_management_vlan" in str(pkt.cdp.field_names):
            print("Management VLAN: " + pkt.cdp.cluster_management_vlan)

        if "vtp_management_domain" in str(pkt.cdp.field_names):
            print("VTP Domain: " + pkt.cdp.vtp_management_domain)

        if "native_vlan" in str(pkt.cdp.field_names):
            print("Native VLAN: " + pkt.cdp.native_vlan)

        if "voice_vlan" in str(pkt.cdp.field_names):
            print("VoIP VLAN: " + pkt.cdp.voice_vlan)


        print("")
        print("")
        print("")
        i += 1

