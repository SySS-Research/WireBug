#!/bin/bash

keysize=$1
key=$2
infile=$3
outfile=$4



if [ -z "$keysize" ]||[ -z "$key" ]||[ -z "$infile" ];then

	echo "Usage: ./decryptsrtp.sh <key size> <key base64 encoded> <infile pcap> <(optional) outfile>"
	echo ""
	echo ""
	echo "key size	=	use encryption (use 128 or 256 for key size)"
	echo "key		=	sets the srtp master key given in base64"
	echo "infile		=	the pcap infile with one unique srtp-stream only"
	echo "outfile		=	the pcap outfile of the decrypted rtp-stream"
	exit 1
else

	decrypt(){	
		./libsrtp-master/test/rtp_decoder -e $keysize -b $key < $infile | text2pcap -t "%M:%S." -u 10000,10000 - - > $outfile
		exit 0
	}


	if [ -z "$outfile" ];then 
		dt=$(date '+%Y%m%d_%H-%M-%S');
		outfile=outfile_$dt.pcap
		decrypt

	else 

		decrypt
		exit 0

	fi
fi

