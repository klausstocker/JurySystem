docker exec -it mosquitto sh -c 'mosquitto_passwd -U mosquitto/config/passwd'
docker exec -it mosquitto sh -c 'kill -HUP $(cat /mosquitto/config/pid)'
