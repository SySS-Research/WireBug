# WireBug

WireBug is a tool set for Voice-over-IP penetration testing. 
It is designed as a wizard which makes it easy to use. The tools are build for single using too, so every tool is its own python or bash program.

## Installation

Install the dependencies in requirements.txt and the python dependencies in requirements_python.txt. 
If you have problems with installation of netfilterqueue, you can build it from source:
```
pip install -U git+https://github.com/kti/python-netfilterqueue.git
```

Use the configure.sh script to download and build [Cisco Systems' SRTP library](https://github.com/cisco/libsrtp).


## Tools

- FullBridge: This is a simple bash script to set up a layer2 bridge with two defined interfaces.

- BridgeTrap: This script is useful in combination of the FullBridge tool. It will mirror the traffic of the bridge to a defined interface e.g. a raspberry pi with two interfaces for bridging and one as monitoring. 

- DoubleEncapsulation: This python program will craft a double encapsulated ICMP packet and send it to the destination - possible VLAN Hopping.

- TimeShift: Tool for response to a NTP request in a man-in-the-middle position (also with FullBridge) with a timestamp in the past or future. You can easily check if the client (VoIP Phone) checks the validity of the server certificate (SIPS, H.323s, HTTPS, LDAPS etc.), or simply use it as a DOS Tool.  

- VlanEnum: This bash script creates 802.1Q virtual interfaces with VLAN tagging and waiting for possible DHCP responses. If it was possible to get an IP Address the interface will be staid alive otherwise it will be deleted. 

- SaCLaC: This includes two python programs. One for spoofing fake LLDP-MED packets to getting into VoIP VLAN or trigger a DoS by instruct the client to set a VLAN-Tag and one to analyze CDP Information of a PCAP File. 

- DecodeSRTP: This script makes it easy to use the [Cisco Systems' SRTP library](https://github.com/cisco/libsrtp) for decrypting a SRTP-SDES Stream if the AES-Key was extracted from the signalling part.

- SIPCraft: This tool is delivered with some basic SIP messages (REGISTER, OPTIONS, INVITE, BYE) but it is also for crafting your own SIP message by using the option "--individual". With this option it is possible to store your SIP content in a simple text file and then spoof it with the sip craft tool. The script supports TCP and UDP. 

- CrackTheSIP: A simple brute force tool for cracking SIP digest authentication by using a word list.  

- ZRTPDowngrade: A Tool to drop ZRTP initiated Packets in a man-in-the-middle position.

- EvilSTUN: A simple tool for fake STUN responses.

- SIPFuzz: A tool for SIP fuzzing.

- SIPEnum: This tool enumerates SIP extensions by a given file.

- SIPBrute: A tool for online brute force attacks against SIP proxies.

- RTPFuzz: A tool for fuzzing an injecting random RTP packets (noise) into running streams. 

### Wizard
The goal of the WireBug tool set is the wizard with tab-completion. This makes it easy to use without knowledge of detailed information about the tool or options. It is recommended to use the tools with the wizard.

#### Start the Wizard
```
python wirebug.py
```

#### Output
```bash

     __      __.__              __________              
    /  \    /  \__|______   ____\______   \__ __  ____  
    \   \/\/   /  \_  __ \_/ __ \|    |  _/  |  \/ ___\ 
>>>>>\>>>>>>>>/|>>||>>|>\/\>>>>>/|>>>>|>>>\>>|>>/>/>/>>>>>>>
      \__/\  / |__||__|    \___  .______  /____/\___  / 
           \/                  \/       \/     /_____/  

by Moritz Abrell - SySS GmbH, 2019 - 2020



Follow the wizard to use WireTap.
Use TAB to show possible options.

wizard > 
```
#### help function
```
wizard > help

Documented commands (type help <topic>):
========================================
bridge      clear       doubleencap  help       timeshift
cdpanalyze  decodesrtp  exit         lldpspoof  vlanenum 
```
#### Sample usage
```

     __      __.__              __________              
    /  \    /  \__|______   ____\______   \__ __  ____  
    \   \/\/   /  \_  __ \_/ __ \|    |  _/  |  \/ ___\ 
>>>>>\>>>>>>>>/|>>||>>|>\/\>>>>>/|>>>>|>>>\>>|>>/>/>/>>>>>>>
      \__/\  / |__||__|    \___  .______  /____/\___  / 
           \/                  \/       \/     /_____/  

by Moritz Abrell - SySS GmbH, 2019



Follow the wizard to use WireTap.
Use TAB to show possible options.

wizard > lldpspoof

This tool is for spoofing LLDP-MED packets with different vendor specific attributes. It is useful to jump into VoIP VLAN if LLDP-MED is configured

Enter the interface which will be used: enp0s31f6

Enter the vendor <innovaphone> <unify>: innovaphone

Enter the MAC address of a innovaphone device <00:90:33:XX:XX:XX>: 00:90:33:00:00:01

Enter a device model e.g. <IP222>: IP811

Verbose mode (will capture the possible response and open it in wireshark)? <y> or <n>: y

.
Sent 1 packets.
[+] Packetspoofing success.
[*] Waiting for possible response.
[+] Response recived!
```


## Usage Video

[![SySS Tool Tip WireBug](https://img.youtube.com/vi/3vg899vCksQ/0.jpg)](https://www.youtube.com/watch?v=3vg899vCksQ)


## Author
Moritz Abrell, SySS GmbH 2019-2021

## Disclaimer 
Use at your own risk. Do not use without full consent of everyone involved. For educational purposes only.

