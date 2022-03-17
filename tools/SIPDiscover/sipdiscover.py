#!/usr/bin/env python3

import sys
import os, subprocess
import argparse
import socket 
import time
import random
import string
import ssl
import re
from os import walk

parser = argparse.ArgumentParser(
    description="SIP discover tool"
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

parser.add_argument(
    '--user',
    dest="USER",
    type=str,
    default="100",
    help="The SIP destination user"
)

parser.add_argument(
    '--key',
    dest="KEY",
    type=str,
    default="key.key",
    help="Private key file for tls connection. Default is \"key.key\""
)

parser.add_argument(
    '--crt',
    dest="CRT",
    type=str,
    default="crt.crt",
    help="Certificate for tls connection. Default is \"crt.crt\""
)

args = parser.parse_args()



def get_payload(request):
    
    f=open(("requests/" + request), "r", newline="")
    if f.mode == "r":
        payload = f.read()

        return payload 

    else:
        sys.exit(1)



def replace_payload(payload):
    
    payload = payload.replace("DOMAIN", args.DOMAIN)
    payload = payload.replace("SRC", args.SRC)
    payload = payload.replace("USER", args.USER)
    payload = payload.replace("CALLID", ( ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(32))))
    payload = payload.replace("BRANCH", ( ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))))
    
    if "TAG" in payload:
        payload = payload.replace("TAG", ( ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8))))

    if args.PROTOCOL == "tcp":
        payload = payload.replace("PROTO", "TCP")
    elif args.PROTOCOL == "tls":
        payload = payload.replace("PROTO", "TLS")
    else:
        payload = payload.replace("PROTO", "UDP")

    return payload 



def main():

    requests = []
    for (dirpath, dirnames, filenames) in walk('./requests'):
        requests.extend(filenames)
        break

    for i in requests:
        payload = get_payload(i)
        payload = replace_payload(payload)
        
        try:
            if args.PROTOCOL == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            elif args.PROTOCOL == "tls": 
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2, keyfile=args.KEY, certfile=args.CRT)
            
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            try:
                sock.settimeout(2.0)
                sock.connect((args.DST, args.DPORT))
                lip, lport = sock.getsockname()
                payload = payload.replace("LPORT", str(lport))
                sock.send(payload.encode())
                print("\033[1;34m[*]\033[0m " + i + " sent")
                response = sock.recv(1024)

                if response:
                    response = response.decode("utf-8")
                    response_lines = str(response).split("\r\n")

                    regex_rl = re.compile("^SIP/2.0", re.IGNORECASE)
                    idx_rl = [i for i, item in enumerate(response_lines) if re.search(regex_rl, item)]
                    if len(idx_rl) > 0:
                        rl_line = response_lines[idx_rl[0]]
                        print("\033[1;32m[+]\033[0m Response-Line: \033[0;32m" + rl_line + "\033[0m")

                    regex_server = re.compile("^Server", re.IGNORECASE)
                    idx_server = [i for i, item in enumerate(response_lines) if re.search(regex_server, item)]
                    if len(idx_server) > 0:
                        server_line = response_lines[idx_server[0]]
                        print("\033[1;32m[+]\033[0m " + server_line)

                    regex_ua = re.compile("^User-Agent", re.IGNORECASE)
                    idx_ua = [i for i, item in enumerate(response_lines) if re.search(regex_ua, item)]
                    if len(idx_ua) > 0:
                        ua_line = response_lines[idx_ua[0]]
                        print("\033[1;32m[+]\033[0m " + ua_line)

                    regex_allow = re.compile("^Allow", re.IGNORECASE)
                    idx_allow = [i for i, item in enumerate(response_lines) if re.search(regex_allow, item)]
                    if len(idx_allow) > 0:
                        allow_line = response_lines[idx_allow[0]]
                        print("\033[1;32m[+]\033[0m " + allow_line)

                    regex_warning = re.compile("^Warning", re.IGNORECASE)
                    idx_warning = [i for i, item in enumerate(response_lines) if re.search(regex_warning, item)]
                    if len(idx_warning) > 0:
                        warning_line = response_lines[idx_warning[0]]
                        print("\033[1;32m[+]\033[0m " + warning_line)

                    regex_reason = re.compile("^Reason", re.IGNORECASE)
                    idx_reason = [i for i, item in enumerate(response_lines) if re.search(regex_reason, item)]
                    if len(idx_reason) > 0:
                        reason_line = response_lines[idx_reason[0]]
                        print("\033[1;32m[+]\033[0m " + reason_line)

                    print("\n")
                else:
                    print("\033[1;31m[!]\033[0m No response received")

                sock.close()

            except (KeyboardInterrupt):
                print("\033[1;34m[*]\033[0m User interruption. Exiting ...")
                sys.exit(0)

            except:
                print("\033[1;31m[!]\033[0m No response received")
                print("\n")
                sock.close()


        except (KeyboardInterrupt):
            print("\033[1;34m[*]\033[0m User interruption. Exiting ...")
            sock.close()
            sys.exit(0)

        except:
            sock.close()
 

if __name__ == "__main__":
    main()



