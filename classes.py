import os
import sys
import subprocess
from cmd import Cmd
from helper import logo


def run_tool(tool_folder, command):
    '''This function will spawn a safe subprocess'''
    cwd = os.getcwd()
    cmd = command.split()
    cmd[0] = ''.join((cwd, '/tools/', tool_folder, '/', cmd[0]))
    subprocess.run(cmd, shell=False, cwd=os.path.join(cwd, 'tools', tool_folder))




class Wizard(Cmd):
    prompt = '\033[0;32mwizard > \033[0m'
    intro = logo()


    def do_bridge(self, inp):
        '''The bridge tool is a full layer2 bridge with two defined interfaces'''
        tool_folder = "FullBridge"
        print("\nThe bridge tool is a full layer2 bridge with two defined interfaces\n")
        bridge_first_interface = input("Enter the first interface: ")
        bridge_second_interface = input("Enter the second Interface: ")
        bridge_bridgemode = input("Enter the bridge mode <on> <off>: ")
        run_tool(
            tool_folder, f"fullbridge.sh {bridge_first_interface} {bridge_second_interface} {bridge_bridgemode}")


    def do_vlanenum(self, inp):
        '''The vlanenum tool is a VLAN enumeration which creates virtual interfaces if VLAN's were found'''
        tool_folder = "VlanEnum"
        print("The vlanenum tool is a VLAN enumeration which creates virtual interfaces if VLAN's were found")
        print("\033[1;34m[*]\033[0m If you want to enumerate numerous VLAN ID's, you should better use the vlanenum.sh script with multiple tmux sessions and different start VLAN ID's")
        print("")
        vlanenum_interface = input("Enter the interface which will be used: ")
        vlanenum_start_vid = input("Enter the start VLAN ID [1]: ") or "1"
        vlanenum_last_vid = input("Enter the last VLAN ID [4096]: ") or "4096"
        run_tool(
            tool_folder, f'vlanenum.sh {vlanenum_interface} {vlanenum_start_vid} {vlanenum_last_vid}')


    def do_timeshift(self, inp):
        '''The timeshift tool is a simple NTP Responder which sets the date to the past or to the future'''
        tool_folder = "TimeShift"
        print("The timeshift tool is a simple NTP Responder which sets the date to the past or to the future")
        print("\033[1;34m[*]\033[0m You have to be in a man-in-the-middle position e.g. with the bridge tool or arp spoofing")
        timeshift_src_ip = input("Enter the target IP address: ")
        timeshift_mode = input(
            "Enter the mode <past> <future> [past]: ") or "past"
        run_tool(tool_folder,
                 f'timeshift.py -s {timeshift_src_ip} -m {timeshift_mode}')


    def do_doubleencap(self, inp):
        '''This tool is tagging a packet twice. If there is a native VLAN on the access port and on the trunk port configured, it is possible to hop into VLAN's'''
        tool_folder = "DoubleEncapsulation"
        print("This tool is tagging a packet twice. If there is a native VLAN on the access port and on the trunk port configured, it is possible to hop into VLAN's")
        doubleencap_interface = input("Enter the interface: ")
        doubleencap_src_ip = input("Enter the source ip address: ")
        doubleencap_dst_ip = input("Enter the destination ip address: ")
        doubleencap_native_vid = input("Enter the native VLAN ID: ")
        doubleencap_dst_vid = input("Enter the destination VLAN ID: ")
        doubleencap_count = input("Enter the amount of packets which will be sent [1]: ") or "1"
        run_tool(tool_folder, f'doubleencapsulation.py -i {doubleencap_interface} -s {doubleencap_src_ip} -d {doubleencap_dst_ip} --nvid {doubleencap_native_vid} --dvid {doubleencap_dst_vid} -c {doubleencap_count}')


    def do_lldpspoof(self, inp):
        '''This tool is for spoofing LLDP-MED packets with different vendor specific attributes. It is useful to jump into VoIP VLAN if LLDP-MED is configured'''
        tool_folder = "SaCLaC"
        print("This tool is for spoofing LLDP-MED packets with different vendor specific attributes. It is useful to jump into VoIP VLAN if LLDP-MED is configured")
        lldpspoof_interface = input("Enter the interface which will be used: ")
        lldpspoof_vendor = input("Enter the vendor <innovaphone> <unify> [innovaphone]: ") or "innovaphone"

        if lldpspoof_vendor == "innovaphone":
            lldpspoof_mac = input("Enter the MAC address of an innovaphone device <00:90:33:XX:XX:XX> [00:90:33:00:00:01]: ") or "00:90:33:00:00:01"
            lldpspoof_device = input("Enter a device model e.g. <IP222> [IP222]: ") or "IP222"
            lldpspoof_verbose = input("Verbose mode (will capture the possible response and open it in wireshark)? <y> or <n> [n]: ") or "n"

            cmd = f"lldpspoof.py -V {lldpspoof_vendor} -m {lldpspoof_mac} -D {lldpspoof_device} -i {lldpspoof_interface}"
            if lldpspoof_verbose == "y":
                cmd += " -v"
            run_tool(tool_folder, cmd)

        elif lldpspoof_vendor == "unify":
            lldpspoof_mac = input("Enter the MAC address of an unify device <00:1a:e8:XX:XX:XX> [00:1a:e8:00:00:01]: ") or "00:1a:e8:00:00:01"
            lldpspoof_verbose = input("Verbose mode (will capture the possible response and open it in wireshark)? <y> or <n> [n]: ") or "n"
            cmd = f"lldpspoof.py -V {lldpspoof_vendor} -m {lldpspoof_mac} -i {lldpspoof_interface}"
            if lldpspoof_verbose == "y":
                cmd += " -v"
            run_tool(tool_folder, cmd)

        else:
            print("Please set a valid vendor")


    def do_lldpdos(self, inp):
        '''This tool is for spoofing LLDP-MED packets with tagged or untagged VLAN ID which will be set by the device'''
        tool_folder = "SaCLaC"
        print("This tool is for spoofing LLDP-MED packets with tagged or untagged VLAN ID which will be set by the device")
        lldpdos_interface = input("Enter the interface which will be used: ")
        lldpdos_mode = input("Enter the mode <tag> <untag> [tag]: ") or "tag"
        lldpdos_mac = input("Enter the MAC address of the switch [78:d0:04:00:00:01]: ") or "78:d0:04:00:00:01"
        lldpdos_verbose = input("Verbose mode (will capture the possible response and open it in wireshark)? <y> or <n> [n]: ") or "n"

        cmd = f"lldpspoof.py --dos -m {lldpdos_mac} -i {lldpdos_interface}"
        if lldpdos_mode == "tag":
            if lldpdos_verbose == "y":
                cmd += " -v"
            run_tool(tool_folder, cmd)

        elif lldpdos_mode == "untag":
            if lldpdos_verbose == "y":
                cmd += " --untag -v"
            else:
                cmd += " --untag"
            run_tool(tool_folder, cmd)

        else:
            print("Please set a valid mode")


    def do_decodesrtp(self, inp):
        '''If you have the AES key from the SDP crypto attribute of the signaling part, you can decrypt the SRTP-SDES stream with this tool'''
        tool_folder = "DecodeSRTP"
        print("If you have the AES key from the SDP crypto attribute of the signaling part, you can decrypt the SRTP-SDES stream with this tool")
        print("Sniff the RTP Stream and extract only the RTP part in a separate PCAP file")
        decodesrtp_keysize = input("Enter the keysize <128> or <256> [128]: ") or "128"
        decodesrtp_key = input("Enter the AES key base64 encoded: ")
        decodesrtp_infile = input("Enter the infile containing the extracted RTP stream: ")
        decodesrtp_outfile = input("Enter the outfile (if nothing is set the file is stored under ./tools/DecodeSRTP/): ")
        run_tool(tool_folder, f"decodesrtp.sh {decodesrtp_keysize} {decodesrtp_key} {decodesrtp_infile} {decodesrtp_outfile}")


    def do_cdpanalyze(self, inp):
        '''A tool to analyze CDP packets in a PCAP file'''
        tool_folder = "SaCLaC"
        print("A tool to analyze CDP packets in a PCAP file")
        cdpanalyze_file = input("Enter the the PCAP file to analyze: ")
        cdpanalyze_verbose = input("Verbose mode will display all packet information <y> or <n> [n]: ")
        cmd = f"cdpanalyze.py -f {cdpanalyze_file}"
        if cdpanalyze_verbose == "y":
            cmd += " -v"
        run_tool(tool_folder, cmd)


    def do_sipcraft(self, inp):
        '''This tool is for crafting and spoofing SIP packets'''
        tool_folder="SIPCraft"
        print("This tool is for crafting and spoofing SIP Packets")
        sipcraft_protocol=input("Enter the protocol <udp> or <tcp> [udp]: ") or "udp"
        sipcraft_message=input("Enter the SIP message <option> <invite> <register> <200> <individual> [option]: ") or "option"
        if sipcraft_message == "individual":
            sipcraft_file=input("Enter the individual file for SIP payload [./tools/sipcraft/individual.txt]: ") or "individual.txt"

        sipcraft_srcip=input("Enter the source IP address [127.0.0.1]: ") or "127.0.0.1"
        sipcraft_dstip=input("Enter the destination IP address [127.0.0.1]: ") or "127.0.0.1"
        sipcraft_sport=input("Enter the source port [5060]: ") or "5060"
        sipcraft_dport=input("Enter the destination port [5060]: ") or "5060"
        cmd=f"sipcraft.py --proto {sipcraft_protocol} --src {sipcraft_srcip} --dst {sipcraft_dstip} --sport {sipcraft_sport} --dport {sipcraft_dport}"
        if sipcraft_message == "individual":
            cmd += f" --msg individual --file {sipcraft_file}"
        else:
            cmd += f" --msg {sipcraft_message}"
        run_tool(tool_folder, cmd)


    def do_sipcrack(self, inp):
        '''A tool for brute forcing SIP digest authentication'''
        tool_folder="CrackTheSIP"
        print("A tool for brute forcing SIP digest authentication")
        sipcrack_username=input("Enter the username: ")
        sipcrack_uri=input("Enter the URI: ")
        sipcrack_nonce=input("Enter the nonce: ")
        sipcrack_realm=input("Enter the given realm: ")
        sipcrack_cnonce=input("Enter cnonce (if exists): ")
        sipcrack_noncecount=input("Enter the nonce count (if exists): ")
        sipcrack_qop=input("Enter the QOP [auth]: ") or "auth"
        sipcrack_response=input("Enter the SIP client' response: ")
        sipcrack_message=input("Enter the message type [REGISTER]: ") or "REGISTER"
        sipcrack_wordlist=input("Enter the wordlist for brute force: ")
        cmd=f"sipcrack.py --username {sipcrack_username} --uri {sipcrack_uri} --nonce {sipcrack_nonce} --realm {sipcrack_realm} --response {sipcrack_response} --msg {sipcrack_message} --wordlist {sipcrack_wordlist}"
        if sipcrack_cnonce:
            cmd += f" --cnonce {sipcrack_cnonce} --noncecount {sipcrack_noncecount} --qop {sipcrack_qop}"
        run_tool(tool_folder, cmd)


    def do_zrtpdowngrade(self, inp):
        '''A tool to downgrade the ZRTP media stream'''
        tool_folder = "ZRTPDowngrade"
        print("A tool to downgrade the ZRTP media stream")
        zrtpdowngrade_interface=input("Enter the interface on which the tool will listen on [all]: ") or "all"
        zrtpdowngrade_verbose=input("Verbose mode?<y> <n> [y]: ") or "y"
        cmd = f"zrtpdowngrade.py"
        if zrtpdowngrade_interface == "all":
            if zrtpdowngrade_verbose == "y":
                cmd += " -v"
        else:
            if zrtpdowngrade_verbose == "y":
                cmd += f" -v -i {zrtpdowngrade_interface}"
            else:
                cmd += f" -i {zrtpdowngrade_interface}"
        run_tool(tool_folder, cmd)


    def do_evilstun(self, inp):
        '''A simple tool for fake STUN responses'''
        tool_folder="EvilSTUN"
        print("A simple tool for fake STUN responses")
        evilstun_stunip=input("Enter the listening ip address for STUN requests: ")
        evilstun_stunport=input("Enter the listening port for STUN requests [3478]: ") or "3478"
        evilstun_rtpip=input("Enter the fake ip address in the response: ")
        evilstun_rtpport=input("Enter the fake port in the response [16000]: ") or "16000"
        cmd=f"evilstun.py --stunip {evilstun_stunip} --stunport {evilstun_stunport} --rtpip {evilstun_rtpip} --rtpport {evilstun_rtpport}"
        run_tool(tool_folder, cmd)


    def do_sipfuzz(self, inp):
        '''A tool for SIP fuzzing'''
        tool_folder="SIPFuzz"
        print("A tool for SIP fuzzing ")
        sipfuzz_dstip=input("Enter the destination SIP server: ")
        sipfuzz_dstport=input("Enter the destination SIP port [5060]: ") or "5060"
        sipfuzz_proto=input("Enter the protocol <udp> or <tcp> [udp]: ") or "udp"
        sipfuzz_file=input("Enter the fuzz request file. Insert \"FUZZ\" at the point you want to fuzz: ")
        sipfuzz_startpoint=input("Enter the fuzzing start point [1]: ") or "1"
        sipfuzz_steps=input("Enter the fuzzing steps [1]: ") or "1"
        sipfuzz_size=input("Enter the fuzzing max. size [2000]: ") or "2000"
        sipfuzz_char=input("Enter the fuzzing char [A]: ") or "A"
        sipfuzz_time=input("Enter the delay between the fuzzing steps in seconds [0.5]: ") or "0.5"
        cmd=f"sipfuzz.py --dst {sipfuzz_dstip} --dport {sipfuzz_dstport} --proto {sipfuzz_proto} --file {sipfuzz_file} --start-point {sipfuzz_startpoint} --steps {sipfuzz_steps} --size {sipfuzz_size} --char {sipfuzz_char} --time {sipfuzz_time}"
        run_tool(tool_folder, cmd)


    def do_sipenum(self, inp):
        '''A tool for SIP extension enumeration'''
        tool_folder="SIPEnum"
        print("A tool for SIP extension enumeration")
        sipenum_dstip=input("Enter the destination SIP server: ")
        sipenum_dstport=input("Enter the destination SIP port [5060]: ") or "5060"
        sipenum_proto=input("Enter the protocol <udp>, <tcp> or <tls> [udp]: ") or "udp"
        if sipenum_proto == "tls":
            sipenum_crt=input("Enter the certificate file [crt.crt]: ") or "crt.crt"
            sipenum_key=input("Enter the private key file [key.key]: ") or "key.key"
        sipenum_srcip=input("Enter the source ip address: ")
        sipenum_domain=input("Enter the SIP domain: ")
        sipenum_wordlist=input("Enter the wordlist with user extensions for enumeration [users/10-99.txt]: ") or "users/10-99.txt"
        if sipenum_proto == "tls":        
            cmd=f"sipenum.py --dst {sipenum_dstip} --dport {sipenum_dstport} --proto {sipenum_proto} --wordlist {sipenum_wordlist} --src {sipenum_srcip} --domain {sipenum_domain} --key {sipenum_key} --crt {sipenum_crt}"
        else:
            cmd=f"sipenum.py --dst {sipenum_dstip} --dport {sipenum_dstport} --proto {sipenum_proto} --wordlist {sipenum_wordlist} --src {sipenum_srcip} --domain {sipenum_domain}"
        run_tool(tool_folder, cmd)


    def do_sipbrute(self, inp):
        '''A tool for SIP online brute force attacks'''
        tool_folder="SIPBrute"
        print("A tool for SIP online brute force attacks")
        sipbrute_dstip=input("Enter the destination SIP server: ")
        sipbrute_dstport=input("Enter the destination SIP port [5060]: ") or "5060"
        sipbrute_proto=input("Enter the protocol <udp>, <tcp> or <tls> [udp]: ") or "udp"
        if sipbrute_proto == "tls":
            sipbrute_crt=input("Enter the certificate file [crt.crt]: ") or "crt.crt"
            sipbrute_key=input("Enter the private key file [key.key]: ") or "key.key"
        sipbrute_srcip=input("Enter the source ip address: ")
        sipbrute_domain=input("Enter the SIP domain: ")
        sipbrute_user=input("Enter the SIP username: ")
        sipbrute_wordlist=input("Enter the wordlist with passwords for the brute force attack [passwords/1-999999.txt]: ") or "passwords/1-999999.txt"
        cmd=f"sipbrute.py --dst {sipbrute_dstip} --dport {sipbrute_dstport} --proto {sipbrute_proto} --wordlist {sipbrute_wordlist} --src {sipbrute_srcip} --domain {sipbrute_domain}"
        if sipbrute_proto == "tls":
            cmd=f"sipbrute.py --dst {sipbrute_dstip} --dport {sipbrute_dstport} --proto {sipbrute_proto} --user {sipbrute_user} --wordlist {sipbrute_wordlist} --src {sipbrute_srcip} --domain {sipbrute_domain} --key {sipbrute_key} --crt {sipbrute_crt}"
        else:
            cmd=f"sipbrute.py --dst {sipbrute_dstip} --dport {sipbrute_dstport} --proto {sipbrute_proto} --user {sipbrute_user} --wordlist {sipbrute_wordlist} --src {sipbrute_srcip} --domain {sipbrute_domain}"
        run_tool(tool_folder, cmd)


    def do_rtpfuzz(self, inp):
        '''A tool for fuzzing an injecting random RTP packets (noise) into running streams'''
        tool_folder="RTPFuzz"
        print("A tool for fuzzing an injecting random RTP packets (noise) into running streams")
        rtpfuzz_dstip=input("Enter RTP destination ip address: ")
        rtpfuzz_dstport=input("Enter RTP destination port: ")
        rtpfuzz_srcip=input("Enter RTP source ip address: ")
        rtpfuzz_srcport=input("Enter RTP source port: ")
        rtpfuzz_sseq=input("Enter start sequence number [0]: ") or "0"
        rtpfuzz_eseq=input("Enter end sequence number (amount of packets) [500]: ") or "500"
        rtpfuzz_ssrc=input("Enter the synchronization source identifier [208851373]: ") or "208851373"
        rtpfuzz_type=input("Enter payload type. Default is \"8\", which is PCMA [8]: ") or "8"
        rtpfuzz_time=input("Enter timestamp [2000000]: ") or "2000000"
       

        cmd=f"rtpfuzz.py --dst {rtpfuzz_dstip} --dport {rtpfuzz_dstport} --src {rtpfuzz_srcip} --sport {rtpfuzz_srcport} --startseq {rtpfuzz_sseq} --endseq {rtpfuzz_eseq} --ssrc {rtpfuzz_ssrc} --type {rtpfuzz_type} --time {rtpfuzz_time}"
        run_tool(tool_folder, cmd)


    def do_exit(self, inp):
        '''Exiting the tool'''
        print("Bye")
        sys.exit(0)


    def do_clear(self, inp):
        '''Clearing the screen'''
        subprocess.run("clear", shell=False)
        print(logo())

