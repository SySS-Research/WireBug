#!/usr/bin/env python3

import sys
import os, subprocess
import argparse
import socket 
import time
import random
import string

parser = argparse.ArgumentParser(
    description="SIP extension enumeration"
)

parser.add_argument(
    '--proto',
    dest="PROTOCOL",
    type=str,
    default="udp",
    help="TCP or UDP <tcp> <udp>. Default is UDP"
)

parser.add_argument(
    '--dport',
    dest="DPORT",
    type=int,
    default=5060,
    help="Destination port. Default is 5060"
)

parser.add_argument(
    '--dst',
    dest="DST",
    type=str,
    required=True,
    help="Destination IP address"
)

parser.add_argument(
    '--file',
    dest="FILE",
    type=str,
    default="register.txt",
    help="The register message to enumerate users. Default is \"register.txt\""
)

parser.add_argument(
    '--wordlist',
    dest="WORDLIST",
    type=str,
    default="users/10-99.txt",
    help="The word list for enumeration. Default is \"users/10-99.txt\""
)

parser.add_argument(
    '--src',
    dest="SRC",
    type=str,
    required=True,
    help="Source IP address"
)

parser.add_argument(
    '--domain',
    dest="DOMAIN",
    type=str,
    required=True,
    help="The SIP domain"
)
args = parser.parse_args()



def get_payload():

    f=open(args.FILE, "r", newline="")
    if f.mode == "r":
        payload = f.read()

        return payload 

    else:
        sys.exit(1)



def replace_payload(payload):
    
    payload = payload.replace("DOMAIN", args.DOMAIN)
    payload = payload.replace("SRC", args.SRC)

    if args.PROTOCOL == "tcp":
        payload = payload.replace("PROTO", "TCP")
    else:
        payload = payload.replace("PROTO", "UDP")

    return payload 



def main():

    payload = get_payload()
    payload = replace_payload(payload)

    lines = [line.rstrip('\n') for line in open(args.WORDLIST)]

    i = 0

    while i < len(lines):
        try:
            output=int(round((int(i)/int(len(lines)))*int(100)))
            print("\033[1;34m[*]\033[0m Progress: " + str(output) + "%", end="\r")

            req = payload.replace("USER", lines[i])
            
            letters = string.digits
            req = req.replace("CALLID", ( ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(32))))


            if args.PROTOCOL == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            try:
                sock.settimeout(2.0)
                sock.connect((args.DST, args.DPORT))
                sock.send(req.encode())
                response = sock.recv(1024)
                sock.close()

                if bytes('401 Unauthorized', 'utf-8') in response:
                    print("\033[1;32m[+]\033[0m Authentication for " + lines[i] + " required\r\n")

                elif bytes('407 Proxy Authentication Required', 'utf-8') in response: 
                    print("\033[1;32m[+]\033[0m Authentication for " + lines[i] + " required\r\n")

                elif bytes('200 OK', 'utf-8') in response: 
                    print("\033[1;32m[+]\033[0;32m No Authentication for " + lines[i] + " required\r\n")

                i += 1

            except (KeyboardInterrupt):
                print("\033[1;34m[*]\033[0m User interruption. Exiting ...")
                sys.exit(0)
            
            except:
                i += 1
                sock.close()

        except (KeyboardInterrupt):
            print("\033[1;34m[*]\033[0m User interruption. Exiting ...")
            sys.exit(0)



if __name__ == "__main__":
    main()



