# to fix - commands do not work on starting container , container will always restart
chmod u=rw-,g=r--,o=--- /mosquitto/config/passwd
chown root:root /mosquitto/config/passwd
