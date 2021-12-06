# ------------------------------------------------
# setting up The website on digital ocean with and asgi and nginx
# ------------------------------------------------

## Installing the Packages from the Ubuntu Repositories
---
`sudo apt update`
`sudo apt install python3-pip python3-venv libpq-dev postgresql postgresql-contrib nginx curl`


## Creating the PostgreSQL Database and User
---
By default, Postgres uses an authentication scheme called “peer authentication” for local connections. This means that if the user’s operating system username matches a valid Postgres username, that user can log in with no further authentication.

-> Log into an interactive Postgres session by typing:
``sudo -u postgres psql``

first create a user for the database : 
``CREATE DATABASE myproject;``
Next, create a database user for the project. Make sure to select a secure password:
``CREATE USER myprojectuser WITH PASSWORD 'password';``


## Project folder and python/django requirements : 
we set up a python environene
the project exist in the folder 
`dhamet`
and the pyhton environement is ``dhametenv`` 

to activate the environemnt : 
``source dhametenv/bin/activate``

the git repository to clone after creating an ssh key in the droplet and then copying the pub key to the repository.

``git clone git@gitlab.com:rimsmarts/artificial-intelligence/dhamet.git``


### required python libraries intallations :
```bash
python -m pip install -U channels
pip install django-allauth
pip install django-debug-toolbar
pip3 install djangorestframework
pip install django-cors-headers
pip3 install django-crispy-forms
pip install django-filter
pip install numpy
pip install termcolor
```
### adding exceptions to the firewall:
- add 8000 to exception in the firewall:
    ``sudo ufw allow 8000``
- allow nginx for the tcp on port 80
    ``sudo ufw allow 'Nginx Full'``
    (if it doesnt work right away, it's ok wait till u install nginx and retry it)

### Some manual testing utils :
---
- link the gunicorn with uvicorn
``gunicorn --bind 0.0.0.0:8000 DhametFront.asgi -w 4 -k uvicorn.workers.UvicornWorker``

- to activate the server:  ssh to it with ur user
place yourself in the folder :
``~/dhamet$`` and activate the venv:
``source dhametenv/bin/activate``
then place yourself in the folder :
``~/dhamet/dhamet$``

- To link the gunicorn with uvicorn
``gunicorn --bind 0.0.0.0:8000 DhametFront.asgi -w 4 -k uvicorn.workers.UvicornWorker``

- To enable the project and run the command : 
``python manage.py runserver 0.0.0.0:8000``

## Most relevent tutorials :
- [https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04)
- [https://www.digitalocean.com/community/tutorials/how-to-set-up-an-asgi-django-app-with-postgres-nginx-and-uvicorn-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-asgi-django-app-with-postgres-nginx-and-uvicorn-on-ubuntu-20-04)

- [https://averyuslaner.com/setting-django-nginx-daphne-ubuntu-1804/](https://averyuslaner.com/setting-django-nginx-daphne-ubuntu-1804/)


---
## Required config files :
---
The **gunicorn.socket** configuration file  :
- it's path :
    `/etc/systemd/system/gunicorn.socket`

- it's content :
    ```conf
        [Unit]
        Description=gunicorn socket

        [Socket]
        ListenStream=/run/gunicorn.sock

        [Install]
        WantedBy=sockets.target
    ```

The **gunicorn.service** configuration file  :
- it's path :
    `/etc/systemd/system/gunicorn.service`

- it's content :
    ```conf
        [Unit]
        Description=gunicorn daemon
        Requires=gunicorn.socket
        After=network.target

        [Service]
        User=yehdih
        Group=www-data
        WorkingDirectory=/home/yehdih/dhamet
        ExecStart=/home/yehdih/dhamet/dhametenv/bin/gunicorn \
                --access-logfile - \
                -k uvicorn.workers.UvicornWorker \
                --workers 3 \
                --bind unix:/run/gunicorn.sock \
                DhametFront.asgi:application
        [Install]
        WantedBy=multi-user.target
    ```

The **Nginx** config file: 
- it's path : 
``/etc/nginx/sites-available/DhametFront``

- Nginx configuration file content : 
    *without wb this conf works fine :*

    ```conf 
    # this configuration works but doesnt connect sockets.S
    server {
        listen 80;
        server_name dhamet.com www.dhamet.com 165.22.85.224;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            alias /home/yehdih/dhamet/dhamet/DhametFront/static/;
        }
        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }
    ```

- *with websocket configuration (using daphne and redis):*
    ```conf
    #This configuration works for websockets by exploiting daphne assuming that django is properly 
    # configured to use redis_channels,
    upstream daphne-backend {
        server localhost:8000;
    }

    server {
        listen 80 default_server;
        listen [::]:80 default_server;


        location /static/ {
            alias /home/yehdih/dhamet/dhamet/DhametFront/static/;
        }

        location / {
            try_files $uri @proxy_to_app;
        }
        location @proxy_to_app {
            proxy_pass http://daphne-backend;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $server_name;
        }
    }
    ```

The **Supervisor** Configuration file :
- it's path :
    `/etc/supervisor/conf.d/DhametFront.conf`

- it's content : 
    ```conf 
        [fcgi-program:asgi]
        # Set Django environment variables
        environment=DJANGO_SETTINGS_MODULE="DhametFront.settings"
        # environment=DJANGO_SETTINGS_MODULE="DhametFront.settings.production",AVE_SECRET_KEY="087syhu3r8ef79u2h3jr89yihujr38yuhwef"

        # TCP socket used by Nginx backend upstream
        socket=tcp://localhost:8000

        # Directory where your site's project files are located
        directory=/home/yehdih/dhamet/dhamet

        # Each process needs to have a separate socket file, so we use process_num
        # Make sure to update "DhametFront.asgi" to match your project name
        command=/home/yehdih/dhamet/dhametenv/bin/daphne -u /run/daphne/daphne%(process_num)d.sock --fd 0 --access-log - --proxy-headers DhametFront.asgi:application

        # Number of processes to startup, roughly the number of CPUs you have
        numprocs=1

        # Give each process a unique name so they can be told apart
        process_name=asgi%(process_num)d

        # Automatically start and recover processes
        autostart=true
        autorestart=true

        # Choose where you want your log to go
        stdout_logfile=/var/log/asgi.log
        redirect_stderr=true
    ```

## Some helper commands in error correction :
- **Start and enable  gunicorn socket**: 
    
    -- ``sudo systemctl start gunicorn.socket``

    -- ``sudo systemctl enable gunicorn.socket``

- **To check if it did start correctly :**
`sudo systemctl status gunicorn.socket`

- if the gunicorn.service <span style="color:#e63946">trigger appears red</span>  aka it didn't start when enabling gunicorn.socket then force service reset with the command line:
    `systemctl reset-failed gunicorn.service`
- **To force reset any service :**
`systemctl reset-failed servicename.service`


- **To reset any service :**
    `systemctl reset-failed servicename.service`


- **To start the Nginx :** 

    -- ``sudo systemctl restart nginx``

    -- ``sudo systemctl reload nginx``
- **To reload Nginx after a conf change :** `sudo service nginx reload`
- If nginx service fail to reload  (<span style="color:#e63946">Job for nginx.service failed text</span>)
    then you have to :

    -- `sudo systemctl daemon-reload`

    -- `sudo systemctl restart gunicorn`
- **Allow nginx for the tcp on port 80**: ``sudo ufw allow 'Nginx Full'``

- **Daphne log shows :** <span style="color:#e63946"> **CRITICAL** Listen failure: [Errno 2] No such file or directory: '3392' -> b'/run/daphne/daphne0.sock.lock'</span>

    --> This is very common after a system reboot :you need to create the `/run/daphne` with `sudo mkdir /run/daphne` folder manually and it fixes it. A server restart caused the folder do be "erased".

---
<span style="color:#90be6d">**Don't forget to run collect static if there are any changes in the static files using `python manage.py collectstatic`**</span>

---


## Errors chasing with traces :
---
check the following files using `sudo vim <LogFilePath>` in order to detect find more detailed errors and correct configurations

**Nginx - /var/log/nginx/error.log**
```log
```

**Supervisord - /var/log/supervisor/supervisord.log**
```log
```


**Daphne process - /var/log/asgi.log**
```log
```
