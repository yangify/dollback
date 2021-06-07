# Dollback

## Prerequisites
    Docker 20.10.5
    RabbitMQ 3.8.16
    SourceGraph: 3.28.0
    MongoDB 4.4.5

### Docker
#### [Windows](https://docs.docker.com/docker-for-windows/install/) 
#### [Mac](https://docs.docker.com/docker-for-mac/install/)

    sudo service docker start

### MongoDB
    docker run -d -p 27017:27017 --name mongodb mongo:4.4.5
    https://www.thepolyglotdeveloper.com/2019/01/getting-started-mongodb-docker-container-deployment/

### RabbitMQ
    docker run -d -p 5672:5672 --name rabbitmq rabbitmq

### SourceGraph
    docker run --publish 7080:7080 --publish 127.0.0.1:3370:3370 --rm --volume ~/.sourcegraph/config:/etc/sourcegraph --volume ~/.sourcegraph/data:/var/opt/sourcegraph sourcegraph/server:3.28.0

## Running the app
Create virtual environment 
```
python -m venv venv
```
Activate virtual environment
```
.\venv\Scripts\activate
```
Install dependencies
```
pip install -r requirements.txt
```
Run
```
python -m app run
```
Start Celery Worker
```
celery -A <project_name> worker --loglevel=INFO
```

## Serving local repository
Install src-cli
```
https://github.com/sourcegraph/src-cli#installation-linux
```
Change directory into decompiled code folder and run the command
```
src serve-git
```
