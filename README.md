# Dollback

## Prerequisites
    Docker 20.10.5
    RabbitMQ 3.8.16
    Elasticsearch: 7.12.1
    MongoDB 4.4.5

## How to install Docker
### [Windows](https://docs.docker.com/docker-for-windows/install/) 
### [Mac](https://docs.docker.com/docker-for-mac/install/)

## RabbitMQ
    docker run -d -p 5672:5672 --name rabbitmq rabbitmq

## Celery Worker
    celery -A <project_name> worker --loglevel=INFO

## Elasticsearch
    docker network create elastic
    docker pull docker.elastic.co/elasticsearch/elasticsearch:7.12.1
    docker run --name es01-test --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.12.1

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