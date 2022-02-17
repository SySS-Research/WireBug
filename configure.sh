#!/bin/bash

getlib(){
    wget -P ./tools/DecryptSRTP/ https://github.com/cisco/libsrtp/archive/master.zip
    unzip -d ./tools/DecryptSRTP/ ./tools/DecryptSRTP/master.zip
    rm ./tools/DecryptSRTP/master.zip 
    cd ./tools/DecryptSRTP/libsrtp-master && ./configure
    make
    exit 1
}

echo -e "\033[1;34m[*]\033[0m Download and build libsrtp ..."
getlib
