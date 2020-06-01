#!/bin/bash

interface01=$1
interface02=$2
bridgemod=$3


if [ "$(id -u)" != "0" ];then
	echo -e "\033[1;31m[!]\033[0m This script must be executed with root permissions"
	exit 1
fi

if [ -z "$interface01" ]||[ -z "$interface02" ]||[ -z "$bridgemod" ];then

	echo "Usage: ./fullbridge.sh <interface 1> <interface 2> <on||off>"
	exit 0
else


	addbridge(){
		ip link set $interface01 up
		ip link set $interface02 up
		brctl addbr br0
		brctl addif br0 $interface01 $interface02
		ip link set br0 up 
		ip addr flush $interface01
		ip addr flush $interface02
		#brctl stp br0 on
		echo 65528 > /sys/class/net/br0/bridge/group_fwd_mask
		brctl show
		echo ""
		echo -e "\033[1;32m[+]\033[0m Bridge br0 is ready"
		echo ""
		echo -e "\033[1;34m[*]\033[0m If you want to suppress your own device traffic use \"ebtables -A OUTPUT -s <your-mac> -j DROP\""
		exit 0
	}


	delbridge(){
		ip link set br0 down
		brctl delbr br0
		ip link set $interface01 down
		ip link set $interface02 down
		ip link set $interface01 up
		ip link set $interface02 up
		echo ""
		echo -e "\033[1;32m[+]\033[0m Bridge is cleaned up"
		exit 0
	}


	case "$bridgemod" in

		"on") addbridge ;;

		"off") delbridge ;;
	
		*) echo "Please specify the bridge-mod. Possible values are <on> or <off>"
		exit 1
		;;

	esac

fi

