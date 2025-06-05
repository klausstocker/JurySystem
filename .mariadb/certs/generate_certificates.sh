#!/usr/bin/env sh
#########################################################################
#Name: generate-certs.sh
#Subscription: This Script generates ssl certs
##by A. Laub
#andreas[-at-]laub-home.de
#
#License:
#This program is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the
#Free Software Foundation, either version 3 of the License, or (at your option)
#any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#or FITNESS FOR A PARTICULAR PURPOSE.  i
#########################################################################
#Set the language
# export LANG="en_US.UTF-8"
#Load the Pathes
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# Just change to your belongings
ROOT="/mosquitto"
# IP="FQDN / IP ADRESS"
IP='127.0.0.1'
SUBJECT_CA="/C=AT/ST=Vienna/L=Vienna/O=htl/OU=CA/CN=$IP"
SUBJECT_SERVER="/C=AT/ST=Vienna/L=Vienna/O=htl/OU=Server/CN=$IP"
SUBJECT_CLIENT="/C=AT/ST=Vienna/L=Vienna/O=htl/OU=Client/CN=$IP"

echo "$SUBJECT_CA"
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -subj "$SUBJECT_CA" -days 365000 -key ca-key.pem -out ca-cert.pem

echo "$SUBJECT_SERVER"
openssl req -newkey rsa:2048 -nodes -subj "$SUBJECT_SERVER"  -days 365000 -keyout server-key.pem -out server-req.pem
openssl x509 -req -days 365000 -set_serial 01 -in server-req.pem -out server-cert.pem -CA ca-cert.pem  -CAkey ca-key.pem


