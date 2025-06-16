# ➕ Add single user 🧞
Running on localhost at Windows run script: x-add_single_user.ps1  
Running on remote Linux Host run script: x-add_single_user.sh  

# ➖ Delete single user 🧞
⭐ Delete the complete line with the user:password in passwd  
⭐ On localhost run script: x-reload_user_password_configuration.ps1    
⭐ On remote Linux Host run script: x-reload_user_password_configuration.sh  

# ➕➕➕➕ Generate passwd file for multiple users  🧞🧞🧞🧞
⭐Write username:password in each line (plain text password) into passwd  
👀 <b>Inspect passwd_example</b> to see how it should look like  
⭐On localhost run script: x-generate_passwd.ps1  
⭐On remote Linux Host run script: x-generate_passwd.sh   

Mosquitto configuration manual: https://mosquitto.org/man/mosquitto-conf-5.html

## ✔️ Example executing a command in the container terminal ✔️
docker exec -it mosquitto sh -c 'cd /mosquitto/conf'
