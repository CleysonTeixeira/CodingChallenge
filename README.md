﻿# CodingChallenge - Let's Code & Itaú
 
**FastAPI, PostgreSQL, Async SQLAlchemy, Pony/Orm**

## Dependencies
* Docker
* Docker-compose

## How to run

Start **apicriticas**, **postgres** database and **pgadmin**
```shell
$ docker-compose up -d --build
```
# Connect postgree with service:
* Access pgadmin:
```shell
localhost:5050
username: admin@gmail.com
password: admin
```
* In Quick Links, click on Add New Server button;
* Put any name;
* In Connection, insert 
```shell
Hostname/address: postgresql
Port: 5432
Username/Password: admin
```
and click to save.

#API Críticas (apicriticas):
You can access the apicriticas, test the features and view the documentaion about this projet in your browser as follows:
```shell
localhost:8080/docs
```

