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
export ROOT="/mosquitto"
# IP="FQDN / IP ADRESS"
export IP='127.0.0.1'
SUBJECT_CA="/C=AT/ST=Vienna/L=Vienna/O=htl/OU=CA/CN=$IP"
SUBJECT_SERVER="/C=AT/ST=Vienna/L=Vienna/O=htl/OU=Server/CN=$IP"
SUBJECT_CLIENT="/C=AT/ST=Vienna/L=Vienna/O=htl/OU=Client/CN=$IP"
echo
echo "+++ Generating self signed certificates +++"
echo
echo "Generate CA"
echo "$SUBJECT_CA"
openssl req -x509 -nodes -sha256 -newkey rsa:2048 -subj "$SUBJECT_CA"  -days 3650 -keyout $ROOT/certs/ca.key -out $ROOT/certs/ca.crt
echo
echo "Generate Server"
echo "$SUBJECT_SERVER"
openssl req -nodes -sha256 -new -subj "$SUBJECT_SERVER" -keyout $ROOT/certs/server.key -out $ROOT/certs/server.csr
openssl x509 -req -sha256 -in $ROOT/certs/server.csr -CA $ROOT/certs/ca.crt -CAkey $ROOT/certs/ca.key -CAcreateserial -out $ROOT/certs/server.crt -days 3650
echo
echo "Generate Client"
echo "$SUBJECT_CLIENT"
openssl req -new -nodes -sha256 -subj "$SUBJECT_CLIENT" -out $ROOT/certs/client.csr -keyout $ROOT/certs/client.key
openssl x509 -req -sha256 -in $ROOT/certs/client.csr -CA $ROOT/certs/ca.crt -CAkey $ROOT/certs/ca.key -CAcreateserial -out $ROOT/certs/client.crt -days 3650


