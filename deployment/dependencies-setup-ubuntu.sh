apt-get install python-setuptools libgdal-dev proj postgresql rabbitmq-server python-pip zlibc python-virtualenv python-dev python-numpy python-matplotlib python-gdal python-scipy
easy_install -U shapely geojson amqplib sqlalchemy psycopg2 pylons recaptcha-client python-cjson scipy gdal
# Move the networkplanner nginx config to sites-available and soft-link to it
sudo cp networkplanner.conf /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/networkplanner.conf /etc/nginx/sites-enabled/networkplanner.conf
# apt-get install python-setuptools python-setuptools-devel gdal gdal-python python-matplotlib zlib proj python-sphinx postgresql-server python-psycopg2 rabbitmq-server
# easy_install -U shapely geojson amqplib sqlalchemy psycopg2 pylons recaptcha-client python-cjson scipy
# updatedb
# LIBPROJ_PATH=`locate libproj | grep so.0$`
# LIBPROJ_PATH_LENGTH=${#LIBPROJ_PATH}
# ln -s $LIBPROJ_PATH ${LIBPROJ_PATH:0:$LIBPROJ_PATH_LENGTH-2}
# yum update -y
