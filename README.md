# todo-web

# Tech Stack
python3 Flask, HTML, CSS, JS, Materialize(Framework), Nginx, uWSGI, AWS EC2, ubuntu

# Setting 
## Installation
```
sudo su
apt install python3
apt install python3-pip
pip3 install flask pytz pygeoip uwsgi
apt-get install nginx
```
## uWSGI Setting
Your current path must be the path where app.py is.  
현재 경로는 반드시 app.py가 있는 경로여야한다.  
Let's say the app.py is in /home/ubuntu.  
app.py가 /home/ubuntu에 존재한다고 하자.


```
cd /home/ubuntu

vim uwsgi.ini

[uwsgi]
chdir = /home/ubuntu
module = app
socket = /home/ubuntu/todo.sock
chmod-socket = 666
daemonize = /home/ubuntu/uwsgi.log
callable = app

uwsgi uwsgi.ini
```

## Nginx Setting
```
vim /etc/nginx/sites-available/default

server{
    listen 5000;
    server_name ec2-13-209-6-162.ap-northeast-2.compute.amazonaws.com;
    location /{
        include uwsgi_params;
        uwsgi_pass unix:/home/ubuntu/todo.sock;
    }

}

service nginx start
```

# URL
http://ec2-13-209-6-162.ap-northeast-2.compute.amazonaws.com:5000/
