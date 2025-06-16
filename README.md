# 🐳 Dockerized Web-Framework for IoT 🐳
Requires Docker compose **> 2.27**   
Select preconfigured services in docker-compose.yml by comment or uncomment includes.
##  🐧🐧🚀 Installing - Linux ( production environment )🚀️🐧🐧
⭐ Install git,wget and unzip (can be skip if already installed)
```shell
    sudo apt update 
    sudo apt install -y git
    sudo apt install -y wget 
    sudo apt install -y unzip 
    sudo rm -rf /var/lib/apt/lists/*  
```
⭐ Choose directory or make a new one with appropriate permissions for writing and executing.      
Clone repository adds folder **Dockerized-Web-Framework-for-IoT**.      
⭐ Clone repository
```shell
    git clone https://github.com/fkrenn12/Dockerized-Web-Framework-for-IoT.git  
    chmod +x ./Dockerized-Web-Framework-for-IoT/*.sh  
    rm -rf ./Dockerized-Web-Framework-for-IoT/*.ps1  
```

## 🔳 🔳 🚀 Installing - Windows ( developing environment )🚀️🔳 🔳   
  
⭐ Open prefered IDE (pycharm, vscode) and clone https://github.com/fkrenn12/Dockerized-Web-Framework-for-IoT.git  
⭐ or manual downloading the code or using the commands in Powershell    
In **Windows Powershell** ( not cmd !! )  use following commands.   
```powershell
    Remove-Item -Path ./master.zip
    Invoke-WebRequest  https://github.com/fkrenn12/Dockerized-Web-Framework-for-IoT/archive/master.zip -OutFile ./master.zip
    Expand-Archive -Path ./master.zip -DestinationPath ./master
    Remove-Item -Path ./master.zip
    Copy-Item -Path ./master/Dockerized-Web-Framework-for-IoT-master ./Dockerized-Web-Framework-for-IoT -Recurse -Force
    Remove-Item -Path ./master -Recurse -Force
```  
It will create a new folder: Dockerized-Web-Framework-for-IoT  
## Editing defaults  
⭐ Edit .env and docker-composer.yml  
⭐ Execute x-rebuild_and_start.local.development.ps1
# Selectable Services
## *Applications and Web*
### 👉 APP (Running python scripts in container)
### 👉 Flet (Framework for web application in pure Python)
<!---
### 👉 API-FASTAPI-PURE-SQL
-->
### 👉 API-FASTAPI-SQLMODEL  
### 👉 Node-Red  
https://nodered.localhost  
The default credentials for login into Editor & Admin API are **admin/admin**.  
The default credentials for Dashboard are **user/user**.  
To set new password edit in Security section in file settings.json 
```
adminAuth: {
        type: "credentials",
        users: [{
            username: "admin",
            password: "$2a$12$lozyn8x8FZGzho/ZyvNS5OmzTfWySUAruqYSFv.btCEuMfJW0iu3K",
            permissions: "*"
        }]
    }
httpNodeAuth: {user:"user",pass:"$2a$12$B4eUfhmTowaDVnB9qLeEU.uofryi75w.FMmaXit788ngGsNN3Cw0W"},
httpStaticAuth: {user:"user",pass:"$2a$12$B4eUfhmTowaDVnB9qLeEU.uofryi75w.FMmaXit788ngGsNN3Cw0W"},
```
Generating new hashes (https://bcrypt-generator.com/). Replace it with copy and paste.     
More about securing node-red: https://nodered.org/docs/user-guide/runtime/securing-node-red  

### 👉 NGINX-PHP (HTML and PHP Webserver)
https://web.localhost/index.php
## *Database*
### 👉 MariaDB + Adminer + Phpmyadmin 
https://phpmyadmin.localhost , https://adminer.localhost 

| Target access | Subdomain  | Username | Password | Database |
|---------------|------------|----------|----------|----------|
| mariadb       | phpmyadmin | root     | example  | ALL      |
| mariadb       | phpmyadmin | foo      | foo      | foo      |
| mariadb       | adminer    | root     | example  | ALL      |
| mariadb       | adminer    | foo      | foo      | foo      |

At first login update the default password.  
### 👉 InfluxDB  + Telegraf + Grafana
https://influxdb.localhost , https://grafana.localhost  

| Target access | Subdomain | Username | Password | Database |
|---------------|-----------|----------|----------|----------|
| grafana       | grafana   | admin    | admin    | ALL      |  

At first start, **InfluxDB** will request to set up an initial user.
<!---
### 👉 RESTful API for mysql/mariadb
https://github.com/krink-code/db-api?tab=readme-ov-file  
http://127.0.0.1:8980/api/<db>/<table>/  
GET    /     # Show status  
GET    /api                          # Show databases  
GET    /api/<db>                     # Show database tables  
GET    /api/<db>/<table>             # Show database table fields    
GET    /api/<db>/<table>?query=true  # List rows of table  
POST   /api/<db>/<table>             # Create a new row  
PUT    /api/<db>/<table>             # Replace existing row with new row  

GET    /api/<db>/<table>/:id         # Retrieve a row by primary key
PATCH  /api/<db>/<table>/:id         # Update row element by primary key
DELETE /api/<db>/<table>/:id         # Delete a row by primary key

GET    /api/<db>/<table>/count       # Count number of rows in a table

POST   /api                          # Content-Type: text/sql
-->
## *Manage Docker*
### 👉 Portainer (Manage and administrate Docker)
https://portainer.localhost  
At first start, **Portainer** will request to set up an initial administrator.   
## *Tools*
### 👉 Traefik (HTTP-Reverse Proxy and LoadBalancer)
https://traefik.localhost  

| Target access | Subdomain | Username | Password |
|---------------|-----------|----------|----------|
| traefik       | traefik   | admin    | admin    |

You will find instructions in file .env to change user and password.    
### 👉 Mosquitto MQTT  
| Protocol  | Binding   | Port | Username | Password | Encryption(tls) |
|-----------|-----------|------|----------|----------|-----------------|
| mqtt      | localhost | 1883 |          |          |        No       |
| mqtt      | 0.0.0.0   | 8883 | admin    | admin    |       Yes       |
| websocket | localhost | 8083 |          |          |        No       |
| websocket | 0.0.0.0   | 8091 | admin    | admin    |       Yes       |

Here
[Mosquitto config readme](https://github.com/fkrenn12/Dockerized-Web-Framework-for-IoT/blob/36d962b5b0966c86f58121a170970d2ba95da774/.mosquitto/config/readme.md)
you find to add, delete users.   
[TEst]([An Internal Link](.mosquitto/config/readme.md))
### 👉 API-MQTT Gateway

### System requirements  
Requires Docker compose > 2.27 (check in terminal: docker compose version)

### /mariadb/certs/./generate_certificates.sh

