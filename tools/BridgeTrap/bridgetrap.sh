#!/bin/bash

monitor=$1
out=$2
mod=$3


if [ "$(id -u)" != "0" ];then
	echo -e "\033[1;31m[!]\033[0m This script must be executed with root permissions"
	exit 1
fi

if [ -z "$monitor" ]||[ -z "$out" ]||[ -z "$mod" ];then

	echo "Usage: ./bridgetrap.sh <interface to monitor> <out interface> <on||off>"
	exit 0
else


	addtrap(){
		tc qdisc add dev $monitor ingress 
		tc filter add dev $monitor parent ffff: protocol all prio 2 u32 match u32 0 0 flowid 1:1 action mirred egress mirror dev $out
		echo -e "\033[1;32m[+]\033[0m Trap is enabled"
		exit 0
	}

	
	deltrap(){
		tc qdisc del dev $monitor ingress
		echo -e "\033[1;32m[+]\033[0m Trap is disabled"
		exit 0
	}
	


	case "$mod" in

		"on") addtrap ;;

		"off") deltrap ;;

		*) echo "Please specify the mode. Possible values are <on> or <off>"
		exit 1
		;;

	esac

fi

