#!/bin/sh
# sh /mosquitto/config/set_permissions.sh
# kill -HUP $(cat /mosquitto/config/pid)
docker exec -it mosquitto sh -c '/mosquitto/config/set_permissions.sh'
docker exec -it mosquitto sh -c 'kill -HUP $(cat /mosquitto/config/pid)'
