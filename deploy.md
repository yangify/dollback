# Deployment guide

## Create Ubuntu EC2 instance
...

## SSH into Ubuntu
    $ ssh -i dollup.pem ubuntu@<Public DNS of ec2>

    if an error occur, run: $ chmod 400 dollup.pem

## Setup Docker
Install docker
```
$ sudo apt install docker.io
```
Install dependencies
```
$ sudo snap install docker
```

## Setup MongoDB
    $ docker run -d -p 27017:27017 --name mongodb mongo:4.4.5
    
    Note: $ sudo service docker start; sudo docker container start mongodb

## Setup Application
Update
```
$ sudo apt-get update
```
Install java
```
$ sudo apt install openjdk-8-jre-headless
```
Install Python virtualenv
```
$ sudo apt-get install python3-venv
```
Clone app
```
$ git clone https://github.com/hongyang-work/dollback.githttps://github.com/hongyang-work/dollback.git
```
Setup virtual environment
```
$ cd dollback
$ python3 -m venv venv
$ source venv/bin/activate
```
Install dependencies
```
$ pip install -r requirements.txt
```
Test run
```
$ python app.py
$ gunicorn -b 0.0.0.0:8000 app:app
Note: there should be no error running them; terminate when done
```

## Setup systemd
Create unit file
```
$ sudo vim /etc/systemd/system/helloworld.service
```
Copy the following in
```
[Unit]
Description=Gunicorn instance for Dollback
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/dollback
ExecStart=/home/ubuntu/dollback/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
Enable the service
```
$ sudo systemctl daemon-reload
$ sudo systemctl start dollback
$ sudo systemctl enable dollback
```

## Setup Nginx
Install Nginx
```
sudo apt-get nginx
```
Update config file to increase file upload size
```
$ sudo vim /etc/nginx/nginx.conf
```
Add the following to config file
```
http {
    client_max_body_size 100M;
    ...
}
```
Start Nginx
```
$ sudo systemctl start nginx
$ sudo systemctl enable nginx
Note: nginx landing should appear when access from public ip
```
Edit default file
```
$ sudo vim /etc/nginx/sites-available/default
```
Add ```proxy_pass``` at ```location /```
```
# Some code above
location / {
    proxy_pass http://127.0.0.1:8000;
}
# some code below
```
Restart Nginx
```
$ sudo systemctl restart nginx
```

# END

# Update code
```
$ sudo systemctl restart dollback
$ sudo systemctl restart nginx
```

# Check server logs
```
$ journalctl -u dollback
```

# Clear server logs
```
$ journalctl --vacuum-time=1s
```