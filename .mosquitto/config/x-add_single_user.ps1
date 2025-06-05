# docker exec -it mosquitto sh -c 'mosquitto_passwd -U passwd'
$Username = Read-Host "Enter username"
docker exec -it mosquitto mosquitto_passwd /mosquitto/config/passwd $Username
docker exec -it mosquitto sh -c 'kill -HUP $(cat /mosquitto/config/pid)'
