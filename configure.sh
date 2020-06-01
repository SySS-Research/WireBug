#!/bin/bash

getlib(){
    wget -P ./tools/DecodeSRTP/ https://github.com/cisco/libsrtp/archive/master.zip
    unzip -d ./tools/DecodeSRTP/ ./tools/DecodeSRTP/master.zip
    rm ./tools/DecodeSRTP/master.zip 
    cd ./tools/DecodeSRTP/libsrtp-master && ./configure
    make
    exit 1
}

echo -e "\033[1;34m[*]\033[0m Download and build libsrtp ..."
getlib
