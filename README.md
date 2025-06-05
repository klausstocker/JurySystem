# 🐳 Dockerized Web-Framework for IoT 🐳
Requires Docker compose **> 2.27**   
Preconfigured services can be selected in file docker-compose.yml
##  🐧🐧🚀 Quickstart - Linux ( production environment )🚀️🐧🐧
⭐ Navigate to folder where you want to install.  
It will create a new folder: Dockerized-Web-Framework-for-IoT  
⭐ Install wget and unzip (if not already installed)
```shell
    apt update \
    && apt install -y wget \
    && apt install -y unzip \
    && rm -rf /var/lib/apt/lists/* \ 
```
⭐ Download master and unzip
```shell
    wget https://github.com/fkrenn12/Dockerized-Web-Framework-for-IoT/archive/master.zip \
    && unzip master.zip \
    && rm -rf master.zip \
    && mv Dockerized-Web-Framework-for-IoT-master Dockerized-Web-Framework-for-IoT
```
⭐ Edit .env and docker-composer.yml  
⭐ x-rebuild_and_start.production.sh

## 🔳 🔳 🚀 Quickstart - Windows ( developing environment )🚀️🔳 🔳   
In **Windows Powershell** ( not cmd !! )  use following commands.   
It will create a new folder: Dockerized-Web-Framework-for-IoT  
```powershell
    Remove-Item -Path ./master.zip
    Invoke-WebRequest  https://github.com/fkrenn12/Dockerized-Web-Framework-for-IoT/archive/master.zip -OutFile ./master.zip
    Expand-Archive -Path ./master.zip -DestinationPath ./master
    Remove-Item -Path ./master.zip
    Copy-Item -Path ./master/Dockerized-Web-Framework-for-IoT-master ./Dockerized-Web-Framework-for-IoT -Recurse -Force
    Remove-Item -Path ./master -Recurse -Force
```
⭐ Edit .env and docker-composer.yml  
⭐ x-rebuild_and_start.local.development.ps1

## *Applications and Web*
### 👉 APP (Running python scripts in container)
### 👉 Flet (Framework for web application in pure Python)
### 👉 API (FastAPI)
### 👉 Node-Red  
Access @development environment: https://nodered.localhost  
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
Access @development environment: https://web.localhost/index.php
## *Database*
### 👉 MariaDB + Adminer + Phpmyadmin 
Access @development environment: https://phpmyadmin.localhost , https://adminer.localhost 

| Target access | Subdomain  | Username | Password | Database |
|---------------|------------|----------|----------|----------|
| mariadb       | phpmyadmin | root     | example  | ALL      |
| mariadb       | phpmyadmin | foo      | foo      | foo      |
| mariadb       | adminer    | root     | example  | ALL      |
| mariadb       | adminer    | foo      | foo      | foo      |

At first login update the default password.  
### 👉 InfluxDB  + Telegraf + Grafana
Access @development environment: https://influxdb.localhost , https://grafana.localhost  

| Target access | Subdomain | Username | Password | Database |
|---------------|-----------|----------|----------|----------|
| grafana       | grafana   | admin    | admin    | ALL      |  

At first start, **InfluxDB** will request to set up an initial user.  
## *Manage Docker*
### 👉 Portainer (Manage and administrate Docker)
Access @development environment: https://portainer.localhost  
At first start, **Portainer** will request to set up an initial administrator.   
## *Tools*
### 👉 Traefik (HTTP-Reverse Proxy and LoadBalancer)
Access @development environment: https://traefik.localhost  

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


### 👉 API-MQTT Gateway

### System requirements  
Requires Docker compose > 2.27 (check in terminal: docker compose version)

### /mariadb/certs/./generate_certificates.sh

