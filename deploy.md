# Deployment guide
## Create Ubuntu EC2 instance
...

open port 3434

## SSH into Ubuntu
    $ ssh -i dollup.pem ubuntu@<Public DNS of ec2>

    if an error occur, run: $ chmod 400 dollup.pem
Update
```
$ sudo apt-get update
```
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
```
$ sudo docker run -d -p 27017:27017 --name mongodb mongo:4.4.5

Note: $ sudo service docker start; sudo docker container start mongodb
```

Mongo shell
```
docker exec -it mongodb mongo
use dollback
```

## Setup Application
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
$ git clone https://github.com/hongyang-work/dollback.git
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
Set Gunicorn timeout
```
$ cd venv/lib/python3.8/site-packages/gunicorn

class Timeout(Setting):
    ...
    default = 180

```

## Setup SourceGraph src-cli
Install src-cli
```
$ sudo curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o /usr/local/bin/src
$ sudo chmod +x /usr/local/bin/src
```
Create local repo folder
```
mkdir dollback/resouces/code
```
Create unit file
```
$ sudo vim /etc/systemd/system/localrepo.service
```
Copy the following in
```
[Unit]
Description=Local repository for sourcegraph
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/dollback/resources/code
ExecStart=src serve-git
Restart=always

[Install]
WantedBy=multi-user.target
```
Enable the service
```
$ sudo systemctl daemon-reload
$ sudo systemctl start localrepo
$ sudo systemctl enable localrepo
```

## Setup auto restart for DollBack
Create unit file
```
$ sudo vim /etc/systemd/system/dollback.service
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
sudo apt-get install nginx
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
// remove these
location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
    try_files $uri $uri/ =404;
 }

# with these
location / {
    proxy_pass http://127.0.0.1:8000;
}
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

# On startup
Start mongodb
```
$ sudo service docker start
$ sudo docker start mongodb
```

# Deployment (SourceGraph)
## Setup
* Launch ec instance: ```Amazon Linux 2 AMI (HVM), SSD Volume Type```
* Ensure the **Auto-assign** Public IP option is “Enable”.
* Add the following user data (as text) in the **Advanced Details** section:
```
#cloud-config
repo_update: true
repo_upgrade: all
runcmd:
# Create the directory structure for Sourcegraph data
- mkdir -p /home/ec2-user/.sourcegraph/config
- mkdir -p /home/ec2-user/.sourcegraph/data
# Install, configure, and enable Docker
- yum update -y
- amazon-linux-extras install docker
- systemctl enable --now --no-block docker
- sed -i -e 's/1024/10240/g' /etc/sysconfig/docker
- sed -i -e 's/4096/40960/g' /etc/sysconfig/docker
- usermod -a -G docker ec2-user
# Install and run Sourcegraph. Restart the container upon subsequent reboots
- [ sh, -c, 'docker run -d --publish 80:7080 --publish 443:7080 --publish 127.0.0.1:3370:3370 --restart unless-stopped --volume /home/ec2-user/.sourcegraph/config:/etc/sourcegraph --volume /home/ec2-user/.sourcegraph/data:/var/opt/sourcegraph sourcegraph/server:3.28.0' ]
```
* Select Next: … until you get to the Configure Security Group page. Then add the following rules:
```
Default HTTP rule: port range 80, source 0.0.0.0/0, ::/0
```
## Monitor logs
```
$ docker logs $(docker ps | grep sourcegraph/server | awk '{ print $1 }')
```

## Setup code host
* Navigate to user logo and click to reveal a drop-down
* Select **Site admin**
* Select **Manage code hosts** under **Repositories**
* Select **Sourcegraph CLI Serve-Git**
* Update URL
* Click Add repository
## End