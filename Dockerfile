FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade && apt -y autoremove
RUN         apt-get update
RUN         apt-get install -yq curl git nano yarn nodejs apt-utils
RUN         apt-get install -yq npm

RUN         npm install -g npm@latest
RUN         npm install create-react-app -g
RUN         npm install -g serve
RUN         apt-get install -y procps
RUN         apt -y install vim
RUN         apt -y install nginx

RUN         apt-get -y install binutils
RUN         apt-get -y install libproj-dev
RUN         apt-get -y install gdal-bin
RUN         npm install -g create-react-app
COPY		./requirements.txt /tmp/
RUN			pip install -r /tmp/requirements.txt

COPY		. /srv/smart-store-project
WORKDIR		/srv/smart-store-project/app

RUN         rm /etc/nginx/sites-enabled/default
RUN         cp /srv/smart-store-project/.config/local_dev/smart-store-project.nginx /etc/nginx/sites-enabled/

RUN         mkdir   /var/log/gunicorn

CMD         /bin/bash
