# todo-web

# Tech Stack
python3 Flask, HTML, CSS, JS, Materialize(Framework), Nginx, uWSGI, AWS EC2, ubuntu

# Setting 
Your current path must be the path where app.py is.  
현재 경로는 반드시 app.py가 있는 경로여야한다.  
Let's say the app.py is in /home/todo.  
app.py가 /home/todo 존재한다고 하자.

## Installation
```
sudo su
cd /home/todo
apt install python3
apt install python3-pip
pip3 install flask pytz pygeoip uwsgi
apt-get install nginx
wget -N http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
gunzip GeoLiteCity.dat.gz

```
## uWSGI Setting
```
1. vim uwsgi.ini

[uwsgi]
chdir = /home/todo
module = app
socket = /home/todo/todo.sock
chmod-socket = 666
daemonize = /home/todo/uwsgi.log
callable = app

2. vim wsgi.py

from app import app as application
if __name__ == "__main__":
    application.run()

3. uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi

4. uwsgi uwsgi.ini
```

## Nginx Setting
```
1. vim /etc/nginx/sites-available/default

server{
    listen 5000;
    server_name 172.31.21.107;
    location /{
        include uwsgi_params;
        uwsgi_pass unix:/home/todo/todo.sock;
    }

}

2. service nginx start
```
