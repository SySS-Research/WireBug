# WireBug

WireBug is a tool set for Voice-over-IP penetration testing. 
It is designed as a wizard which makes it easy to use. The tools are build for single using too, so every tool is its own python or bash program.

## Installation

Read the Installation Guide in the [wiki](https://github.com/SySS-Research/WireBug/wiki/Installation-Guide).

## Tools

- FullBridge: This is a simple bash script to set up a layer2 bridge with two defined interfaces.

- TimeShift: Tool for response to a NTP request in a man-in-the-middle position (also with FullBridge) with a timestamp in the past or future. You can easily check if the client (VoIP Phone) checks the validity of the server certificate (SIPS, H.323s, HTTPS, LDAPS etc.), or simply use it as a DOS Tool.  

- VlanEnum: This bash script creates 802.1Q virtual interfaces with VLAN tagging and waiting for possible DHCP responses. If it was possible to get an IP Address the interface will be staid alive otherwise it will be deleted. 

- SaCLaC: This includes two python programs. One for spoofing fake LLDP-MED packets to getting into VoIP VLAN or trigger a DoS by instruct the client to set a VLAN-Tag and one to analyze CDP Information of a PCAP File. 

- DecodeSRTP: This script makes it easy to use the [Cisco Systems' SRTP library](https://github.com/cisco/libsrtp) for decrypting a SRTP-SDES Stream if the AES-Key was extracted from the signalling part.

- CrackTheSIP: A simple brute force tool for cracking SIP digest authentication by using a word list.  

- ZRTPDowngrade: A Tool to drop ZRTP initiated Packets in a man-in-the-middle position.

- EvilSTUN: A simple tool for fake STUN responses.

- SIPFuzz: A tool for SIP fuzzing.

- SIPEnum: This tool enumerates SIP extensions by a given file.

- SIPBrute: A tool for online brute force attacks against SIP proxies.

- SIPDiscover: A tool to discover SIP services.

- RTPFuzz: A tool for fuzzing an injecting random RTP packets (noise) into running streams. 

- RTPAudioInjection: A tool for injecting a raw audio file into running streams. 


## Usage

Read the [wiki pages](https://github.com/SySS-Research/WireBug/wiki) for more information.

### Wizard
The goal of the WireBug tool set is the wizard with tab-completion. This makes it easy to use without knowledge of detailed information about the tool or options.
Additionally, you can use any tool from the command line.

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

by Moritz Abrell - SySS GmbH, 2019 - 2021



Follow the wizard to use WireBug.
Use TAB to show possible options.

wizard > 
```
#### help function
```
wizard > help

Documented commands (type help <topic>):
========================================
bridge      evilstun  lldpspoof       sipcrack     timeshift    
cdpanalyze  exit      rtpaudioinject  sipdiscover  vlanenum     
clear       help      rtpfuzz         sipenum      zrtpdowngrade
decodesrtp  lldpdos   sipbrute        sipfuzz
```

## Sample Usage Video

[![SySS Tool Tip WireBug](https://img.youtube.com/vi/3vg899vCksQ/0.jpg)](https://www.youtube.com/watch?v=3vg899vCksQ)

## References

* [Hacktivity 2020](https://hacktivity.com/index.php/presentations/)
* [Standoff 2020](https://standoff365.com/conferences/penetration-testing-communication-systems-nowadays)
* [SySS Pentest Blog](https://www.syss.de/pentest-blog/2020/penetrationstests-von-voip-und-ucc-das-neue-syss-tool-wirebug)

## Author
Moritz Abrell, SySS GmbH 2019-2021

## Disclaimer 
Use at your own risk. Do not use without full consent of everyone involved. For educational purposes only.

