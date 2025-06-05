docker exec -it mosquitto sh -c '/mosquitto/config/set_permissions.sh'
docker exec -it mosquitto sh -c 'kill -HUP $(cat /mosquitto/config/pid)'
