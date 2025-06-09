#!/bin/sh
docker exec -it mosquitto sh -c 'kill -HUP $(cat /mosquitto/config/pid)'
