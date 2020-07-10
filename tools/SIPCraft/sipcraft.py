#!/usr/bin/env python3

import sys
import os, subprocess
import argparse
import socket 
import time

parser = argparse.ArgumentParser(
    description="SIP Packet Crafting and Spoofing"
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
    '--sport',
    dest="SPORT",
    type=int,
    default=5060,
    help="Source port"
)

parser.add_argument(
    '--src',
    dest="SRC",
    type=str,
    default="1.1.1.1",
    help="Source IP address or CIDR"
)

parser.add_argument(
    '--dst',
    dest="DST",
    type=str,
    required=True,
    help="Destination IP address or CIDR"
)

parser.add_argument(
    '--msg',
    dest="MESSAGE",
    type=str,
    default="option",
    help="The SIP message (Payload) <option> <invite> <register> <individual> <200>. If \"individual\" is choose, the payload will be load from \"--file\""
)

parser.add_argument(
    '--file',
    dest="FILE",
    type=str,
    default="individual.txt",
    help="The file which will be used for individual SIP message. Default is \"individual.txt\""
)

parser.add_argument(
    '--domain',
    dest="DOMAIN",
    type=str,
    help="The target domain. If nothing is set the target domain equals the destination IP address"
)

args = parser.parse_args()


def payload_option():

    if args.PROTOCOL == "tcp":

        payload=('OPTIONS sip:' + args.DOMAIN + ' SIP/2.0\r\n'
            'Via: SIP/2.0/TCP ' + args.SRC + ':' + str(args.SPORT) + '\r\n'
            'To: <sip:' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: <sip:' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 1\r\n'
            'CSeq: 1 OPTIONS\r\n'
            'Contact: <sip:' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Accept: application/sdp\r\n'
            'Content-Length: 0\r\n\r\n')

        return payload


    else:

        payload=('OPTIONS sip:' + args.DOMAIN + ' SIP/2.0\r\n'
            'Via: SIP/2.0/UDP ' + args.SRC + ':' + str(args.SPORT) + '\r\n'
            'To: <sip:' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: <sip:' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 1\r\n'
            'CSeq: 1 OPTIONS\r\n'
            'Contact: <sip:' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Accept: application/sdp\r\n'
            'Content-Length: 0\r\n\r\n')

        return payload



def payload_invite():

    if args.PROTOCOL == "tcp":

        payload=('INVITE sip:100@' + args.DOMAIN + ' SIP/2.0\r\n'
            'Via: SIP/2.0/TCP ' + args.SRC + ':' + str(args.SPORT) + '\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 466\r\n'
            'To: 100 <sip:100@' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: SySS <sip:101@' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 38d41163-72f7-45d9-8fc1-f00000000001\r\n'
            'CSeq: 1 INVITE\r\n'
            'Supported: timer\r\n'
            'Allow: NOTIFY\r\n'
            'Allow: REFER\r\n'
            'Allow: OPTIONS\r\n'
            'Allow: INVITE\r\n'
            'Allow: ACK\r\n'
            'Allow: CANCEL\r\n'
            'Allow: BYE\r\n'
            'Content-Type: application/sdp\r\n'
            'Contact: <sip:' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Supported: replaces\r\n'
            'User-Agent: WireBug\r\n\r\n'
            'v=0\r\n'
            'o=SIP 0 639859198 IN IP4 ' + args.SRC + '\r\n'
            's=SIP Call\r\n'
            'c=IN IP4 ' + args.SRC + '\r\n'
            't=0 0\r\n'
            'm=audio 16388 RTP/AVP 0 18 101 102 107 104 105 106 4 8 103\r\n'
            'a=rtpmap:0 PCMU/8000\r\n'
            'a=rtpmap:18 G729/8000\r\n'
            'a=rtpmap:101 BV16/8000\r\n'
            'a=rtpmap:102 BV32/16000\r\n'
            'a=rtpmap:107 L16/16000\r\n'
            'a=rtpmap:104 PCMU/16000\r\n'
            'a=rtpmap:105 PCMA/16000\r\n'
            'a=rtpmap:106 L16/8000\r\n'
            'a=rtpmap:4 G723/8000\r\n'
            'a=rtpmap:8 PCMA/8000\r\n'
            'a=rtpmap:103 telephone-event/8000\r\n'
            'a=fmtp:103 0-15\r\n'
            'a=silenceSupp:off - - - -\r\n\r\n')

        return payload


    else:

        payload=('INVITE sip:100@' + args.DOMAIN + ' SIP/2.0\r\n'
            'Via: SIP/2.0/UDP ' + args.SRC + ':' + str(args.SPORT) + '\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 466\r\n'
            'To: 100 <sip:100@' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: SySS <sip:101@' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 38d41163-72f7-45d9-8fc1-f00000000001\r\n'
            'CSeq: 1 INVITE\r\n'
            'Supported: timer\r\n'
            'Allow: NOTIFY\r\n'
            'Allow: REFER\r\n'
            'Allow: OPTIONS\r\n'
            'Allow: INVITE\r\n'
            'Allow: ACK\r\n'
            'Allow: CANCEL\r\n'
            'Allow: BYE\r\n'
            'Content-Type: application/sdp\r\n'
            'Contact: <sip:' + args.SRC + ':' + str(args.SPORT) + '>\r\n'
            'Supported: replaces\r\n'
            'User-Agent: WireBug\r\n\r\n'
            'v=0\r\n'
            'o=SIP 0 639859198 IN IP4 ' + args.SRC + '\r\n'
            's=SIP Call\r\n'
            'c=IN IP4 ' + args.SRC + '\r\n'
            't=0 0\r\n'
            'm=audio 16388 RTP/AVP 0 18 101 102 107 104 105 106 4 8 103\r\n'
            'a=rtpmap:0 PCMU/8000\r\n'
            'a=rtpmap:18 G729/8000\r\n'
            'a=rtpmap:101 BV16/8000\r\n'
            'a=rtpmap:102 BV32/16000\r\n'
            'a=rtpmap:107 L16/16000\r\n'
            'a=rtpmap:104 PCMU/16000\r\n'
            'a=rtpmap:105 PCMA/16000\r\n'
            'a=rtpmap:106 L16/8000\r\n'
            'a=rtpmap:4 G723/8000\r\n'
            'a=rtpmap:8 PCMA/8000\r\n'
            'a=rtpmap:103 telephone-event/8000\r\n'
            'a=fmtp:103 0-15\r\n'
            'a=silenceSupp:off - - - -\r\n\r\n')

        return payload





def payload_register():

    if args.PROTOCOL == "tcp":

        payload=('REGISTER sip:' + args.DOMAIN + ' SIP/2.0\r\n'
            'Via: SIP/2.0/TCP ' + args.DOMAIN + ':' + str(args.SPORT) + '\r\n'
            'To: <sip:100@' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: SySS <sip:100@' + args.SRC  + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 38d41163-72f7-45d9-8fc1-f00000000001\r\n'
            'CSeq: 1 REGISTER\r\n'
            'User-agent: WireBug\r\n'
            'Content-Length: 0\r\n\r\n')

        return payload


    else:

        payload=('REGISTER sip:' + args.DOMAIN + ' SIP/2.0\r\n'
            'Via: SIP/2.0/UDP ' + args.DOMAIN + ':' + str(args.SPORT) + '\r\n'
            'To: <sip:100@' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: SySS <sip:100@' + args.SRC  + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 38d41163-72f7-45d9-8fc1-f00000000001\r\n'
            'CSeq: 1 REGISTER\r\n'
            'User-agent: WireBug\r\n'
            'Content-Length: 0\r\n\r\n')


        return payload





def payload_200():
    
    if args.PROTOCOL == "tcp":

        payload=('SIP/2.0 200 OK\r\n'
            'Via: SIP/2.0/TCP ' + args.DOMAIN + ':' + str(args.SPORT) + '\r\n'
            'To: <sip:100@' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: SySS <sip:100@' + args.SRC  + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 38d41163-72f7-45d9-8fc1-f00000000001\r\n'
            'CSeq: 1 INVITE\r\n'
            'User-agent: WireBug\r\n'
            'Content-Length: 0\r\n\r\n')

        return payload


    else:

        payload=('SIP/2.0 200 OK\r\n'
            'Via: SIP/2.0/UDP ' + args.DOMAIN + ':' + str(args.SPORT) + '\r\n'
            'To: <sip:100@' + args.DOMAIN + ':' + str(args.DPORT) + '>\r\n'
            'From: SySS <sip:100@' + args.SRC  + ':' + str(args.SPORT) + '>\r\n'
            'Call-ID: 38d41163-72f7-45d9-8fc1-f00000000001\r\n'
            'CSeq: 1 INVITE\r\n'
            'User-agent: WireBug\r\n'
            'Content-Length: 0\r\n\r\n')

        return payload





def payload_individual():

    f=open(args.FILE, "r", newline="")
    if f.mode == "r":
        payload = f.read()

        return payload 

    else:
        sys.exit(1)
        



def tcp(payload):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_sock.settimeout(2.0)
        tcp_sock.connect((args.DST, args.DPORT))
        tcp_sock.send(payload.encode())
        response = tcp_sock.recv(1024)
        if response:
            print("\033[1;32m[+]\033[0m Response recived:\r\n")
            print(str(response, 'utf-8'))
    except:
        print("\033[1;34m[*]\033[0m No data recived")
    finally:
        tcp_sock.close()


def udp(payload):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        udp_sock.settimeout(2.0)
        udp_sock.connect((args.DST, args.DPORT))
        udp_sock.send(payload.encode())
        response = udp_sock.recv(1024)
        if response:
            print("\033[1;32m[+]\033[0m Response recived:\r\n")
            print(str(response, 'utf-8'))
    except:
        print("\033[1;34m[*]\033[0m No data recived")
    finally:
        udp_sock.close()






if not args.DOMAIN:
    args.DOMAIN = args.DST


if args.MESSAGE == "option":
    payload = payload_option()

elif args.MESSAGE == "invite":
    payload = payload_invite()

elif args.MESSAGE == "register":
    payload = payload_register()

elif args.MESSAGE == "individual":
    payload = payload_individual()

elif args.MESSAGE == "200":
    payload = payload_200()

else:
    payload = payload_option()



if args.PROTOCOL == "tcp":
    tcp(payload)

else:
    udp(payload)

