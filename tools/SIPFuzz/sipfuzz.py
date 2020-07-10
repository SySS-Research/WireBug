#!/usr/bin/env python3

import sys
import os, subprocess
import argparse
import socket 
import time

parser = argparse.ArgumentParser(
    description="Simple SIP fuzzer"
)

parser.add_argument(
    '--proto',
    dest="PROTOCOL",
    type=str,
    default="udp",
    help="TCP or UDP <tcp> <udp>"
)

parser.add_argument(
    '--dport',
    dest="DPORT",
    type=int,
    default=5060,
    help="Destination port"
)

parser.add_argument(
    '--size',
    dest="SIZE",
    type=int,
    default=2000,
    help="The max. fuzz size"
)

parser.add_argument(
    '--sport',
    dest="SPORT",
    type=int,
    default=5060,
    help="Source port"
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
    default="fuzz.txt",
    help="The file which will be used for SIP message. Default is \"fuzz.txt\""
)

parser.add_argument(
    '--steps',
    dest="STEPS",
    type=int,
    default=1,
    help="Steps between the fuzzing size. Default is 1"
)

parser.add_argument(
    '--start-point',
    dest="STARTPOINT",
    type=int,
    default=1,
    help="Starting point for fuzzing size. Default is 1"
)

parser.add_argument(
    '--char',
    dest="CHAR",
    type=str,
    default="A",
    help="Fuzzing character. Default is \"A\""
)

parser.add_argument(
    '--time',
    dest="TIME",
    type=float,
    default=0.5,
    help="Time between fuzzing steps. Default is 0.5 seconds"
)

args = parser.parse_args()



def get_payload():

    f=open(args.FILE, "r", newline="")
    if f.mode == "r":
        payload = f.read()

        return payload 

    else:
        sys.exit(1)
        


def main():

    payload = get_payload()

    size = args.STARTPOINT

    while size < args.SIZE:
        try:
            print("\033[1;34m[*]\033[0m Sending buffer with " + str(size) + " bytes")
            
            inputBuffer = (args.CHAR * size)

            buf = payload.replace("FUZZ", inputBuffer)

            if args.PROTOCOL == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            try:
                sock.settimeout(3.0)
                sock.connect((args.DST, args.DPORT))
                sock.send(buf.encode())
                response = sock.recv(1024)
                if response:
                    print("\033[1;34m[*]\033[0m Response recived\r\n")
                else:
                    print("\033[1;34m[*]\033[0m No data recived\r\n")
            except:
                print("\033[1;32m[+]\033[0m No connection possible")
                sock.close()
                sys.exit()
            finally:
                sock.close()

            size += args.STEPS
            time.sleep(args.TIME)


        except:
            sys.exit("\033[1;34m[*]\033[0m System exit")



if __name__ == "__main__":
    main()


