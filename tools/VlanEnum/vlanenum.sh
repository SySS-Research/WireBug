#!/bin/bash

interface=$1
startID=$2
endID=$3 


if [ "$(id -u)" != "0" ];then 
	echo -e "\033[1;31m[!]\033[0m This script must be executed with root permissions"
	exit 1
fi


if [ -z "$interface" ]||[ -z "$startID" ]||[ -z "$endID" ];then 

	echo "Usage: ./vlanenum.sh <interface> <start VLAN ID> <end VLAN ID>"

else

	while [ $startID -le $endID ]
	do
		echo -e "\033[1;34m[*]\033[0m current testing ID = $startID"
		
		sed -i 's/interface\ \".*\"\;/\interface\ \"'$interface.$startID'\"\;/g' ./dhclient.conf

		ip link add link $interface name $interface.$startID type vlan id $startID
		ip link set $interface.$startID up

		dhoutput=$(dhclient $interface.$startID -v -cf ./dhclient.conf 2>&1)

		if [[ $dhoutput != *"bound"* ]] || [[ $dhoutput == *"169.254.0.1"* ]];
		then		 
			ip link delete $interface.$startID

		else 
			echo -e "\033[1;32m[+]\033[0mVLAN with ID $startID created"

		fi

		startID=$[$startID + 1]
	done

fi

