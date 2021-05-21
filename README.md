# Dollback

## Prerequisites
    Docker 20.10.5
    RabbitMQ 3.8.16
    SourceGraph: 3.27.5
    MongoDB 4.4.5

## Docker
### [Windows](https://docs.docker.com/docker-for-windows/install/) 
### [Mac](https://docs.docker.com/docker-for-mac/install/)

    sudo service docker start

## RabbitMQ
    docker run -d -p 5672:5672 --name rabbitmq rabbitmq

## Celery Worker
    celery -A <project_name> worker --loglevel=INFO

## SourceGraph
    docker run --publish 7080:7080 --publish 127.0.0.1:3370:3370 --rm --volume ~/.sourcegraph/config:/etc/sourcegraph --volume ~/.sourcegraph/data:/var/opt/sourcegraph sourcegraph/server:3.27.5

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